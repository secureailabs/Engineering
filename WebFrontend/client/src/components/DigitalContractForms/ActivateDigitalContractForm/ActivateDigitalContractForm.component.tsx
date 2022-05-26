import React from 'react';

import axios, { AxiosError } from 'axios';
import { useForm } from 'react-hook-form';

import Spinner from '@components/Spinner/SpinnerOnly.component';
import { TActivateDigitalContractFormProps } from './ActivateDigitalContractForm.types';

import ActivateDigitalContractFormSuccess from './ActivateDigitalContractForm.success';
import ActivateDigitalContractFormFailure from "./ActivateDigitalContractForm.failure";
import { TPatchActivateDigitalContractStart, TPatchActivateDigitalContractSuccess } from '@APIs/digitalContract/digitalContract.typeDefs';
import Modal from '@secureailabs/web-ui/components/Modal';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';

import { axiosProxy } from '@APIs/utils';
import { useMutation } from 'react-query';

import { demo_data } from "@APIs/dataset/dataset.data";


const activateContract = async (digitalContractInfo: TPatchActivateDigitalContractStart): Promise<any> => {
  // return demo_data?.Datasets?.[id];
  const res = await axios.patch<TPatchActivateDigitalContractSuccess>
    (`${axiosProxy()}/api/v1/DigitalContractManager/Researcher/Activate`,
      digitalContractInfo,
      {
        withCredentials: true,
      });
  return res
}


const ActivateDigitalContractForm: React.FC<TActivateDigitalContractFormProps> = ({ setIsOpen, DigitalContractGuid, UrlOnSuccess = '/dashboard/digital-contracts' }) => {

  // @ts-ignore
  const mutation = useMutation<TPatchActivateDigitalContractStart, AxiosError>((formData) => activateContract(formData));

  const { register, handleSubmit, formState, trigger } = useForm<{}>({ mode: 'onSubmit' });

  const onSubmit = (
    // @ts-ignore
  ) => mutation.mutate({ DigitalContractGuid: DigitalContractGuid })

  if (mutation.isLoading) {
    return <Modal title='Activate Digital Contract' description='Loading...' close={() => setIsOpen(false)}><Spinner /></Modal>
  }
  if (mutation.isSuccess && mutation.data) {
    return (
      <ActivateDigitalContractFormSuccess UrlOnSuccess={UrlOnSuccess} />
    )
  }
  if (mutation.error) {
    console.log('failure')
    return <ActivateDigitalContractFormFailure setIsOpen={setIsOpen} error={mutation.error} />
  }

  return (
    <Modal
      title='Activate Digital Contract'
      description="Before activating this digital contract, make sure that all of its information is correct."
      close={() => setIsOpen(false)}
    >
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <FormFieldsRenderer
          register={register}
          button_text="Activate Digital Contract"
          formState={formState}
          fields={{}}
        />
      </form>
    </Modal>
  )

};

export default ActivateDigitalContractForm;
