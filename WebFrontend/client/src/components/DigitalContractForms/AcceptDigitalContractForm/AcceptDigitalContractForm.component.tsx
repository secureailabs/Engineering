import React from 'react';

import axios, { AxiosError } from 'axios';
import { useForm } from 'react-hook-form';

import Spinner from '@components/Spinner/SpinnerOnly.component';
import { TAcceptDigitalContractFormProps } from './AcceptDigitalContractForm.types';

import AcceptDigitalContractFormSuccess from './AcceptDigitalContractForm.success';
import AcceptDigitalContractFormFailure from "./AcceptDigitalContractForm.failure";
import { TPatchAcceptDigitalContractStart, TPatchAcceptDigitalContractSuccess } from '@APIs/digitalContract/digitalContract.typeDefs';
import Modal from '@secureailabs/web-ui/components/Modal';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';

import { axiosProxy } from '@APIs/utils';
import { useMutation } from 'react-query';

import { demo_data } from "@APIs/dataset/dataset.data";


const acceptContract = async (digitalContractInfo: TPatchAcceptDigitalContractStart): Promise<any> => {
  // return demo_data?.Datasets?.[id];
  const res = await axios.patch<TPatchAcceptDigitalContractSuccess>
    (`${axiosProxy()}/api/v1/DigitalContractManager/DataOwner/Accept`,
      digitalContractInfo,
      {
        withCredentials: true,
      });
  return res
}


const AcceptDigitalContractForm: React.FC<TAcceptDigitalContractFormProps> = ({ setIsOpen, DigitalContractGuid, UrlOnSuccess = '/dashboard/digital-contracts' }) => {

  // @ts-ignore
  const mutation = useMutation<TPatchAcceptDigitalContractStart, AxiosError>((formData) => acceptContract(formData));

  const { register, handleSubmit, formState, trigger } = useForm<{
    RetentionTime: number, LegalAgreement: string
  }>({ mode: 'onSubmit' });

  const onSubmit = (data: {
    RetentionTime: number, LegalAgreement: string
    // @ts-ignore
  }) => mutation.mutate({ ...data, DigitalContractGuid: DigitalContractGuid, Description: '', HostForVirtualMachines: 'Secure AI Labs', NumberOfVirtualMachines: 1, NumberOfVCPU: 4, HostRegion: 'east-us' })

  if (mutation.isLoading) {
    return <Modal title='Accept Digital Contract' description='Loading...' close={() => setIsOpen(false)}><Spinner /></Modal>
  }
  if (mutation.isSuccess && mutation.data) {
    return (
      <AcceptDigitalContractFormSuccess UrlOnSuccess={UrlOnSuccess} />
    )
  }
  if (mutation.error) {
    console.log('failure')
    return <AcceptDigitalContractFormFailure setIsOpen={setIsOpen} error={mutation.error} />
  }

  return (
    <Modal
      title='Accept Digital Contract'
      description="To accept this digital contract, enter the amount of days you want its logs to be kept in the SAIL database and the legal agreement you previously negotiated with the researcher organization."
      close={() => setIsOpen(false)}
    >
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <FormFieldsRenderer
          register={register}
          button_text="Accept Digital Contract"
          formState={formState}
          fields={{
            RetentionTime: {
              label: 'Data Retention Time',
              placeholder: 'Data Retention Time',
              type: 'number',
            },
            LegalAgreement: {
              label: 'Legal Agreement',
              placeholder: 'Legal Agreement',
              type: 'textarea',
            },
          }}
        />
      </form>
    </Modal>
  )

};

export default AcceptDigitalContractForm;
