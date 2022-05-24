import React from 'react';

import axios, { AxiosError } from 'axios';
import { useForm } from 'react-hook-form';
import { useParams } from 'react-router';


import Spinner from '@components/Spinner/SpinnerOnly.component';
import { TRequestDataAccessFormProps } from './RequestDataAccessForm.types';

import RequestDataAccessFormSuccess from './RequestDataAccessForm.success';
import RequestDataAccessFormFailure from "./RequestDataAccessForm.failure";
import { TGetDatasetSuccess } from '@app/redux/dataset/dataset.typeDefs';
import { TPostDigitalContractStart, TPostDigitalContractSuccess } from '@app/redux/digitalContract/digitalContract.typeDefs';
import Modal from '@secureailabs/web-ui/components/Modal';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';

import { axiosProxy } from '@app/redux/utils';
import { useMutation } from 'react-query';

import { demo_data } from "@app/redux/dataset/dataset.data";


const postContract = async (digitalContractInfo: TPostDigitalContractStart): Promise<any> => {
  // return demo_data?.Datasets?.[id];
  const res = await axios.post<TPostDigitalContractSuccess>
    (`${axiosProxy()}/api/v1/DigitalContractManager/Applications`,
    digitalContractInfo,
  {
    withCredentials: true,
      });
  return res
}


const RequestDataAccessForm: React.FC<TRequestDataAccessFormProps> = ({ setIsOpen, DataOwnerOrganization, DatasetGuid, UrlOnSuccess = '/dashboard/datasets' }) => {

  // @ts-ignore
  const mutation = useMutation<TPostDigitalContractStart, AxiosError>((formData) => postContract(formData));
  
  const { register, handleSubmit, formState, trigger } = useForm<{Title: string, Description: string, SubscriptionDays: number}>({ mode: 'onSubmit' });

  const onSubmit = (data : {
    Title: string, SubscriptionDays: number, Description: string
    // @ts-ignore
  }) => mutation.mutate({ ...data, DatasetGuid: DatasetGuid, DataOwnerOrganization: DataOwnerOrganization, VersionNumber: '', LegalAgreement: '', DatasetDRMMetadataSize: 0, DatasetDRMMetadata: {}})
  
  if (mutation.isLoading) {
    return <Modal title='Request Dataset Access' description='Loading...' close={() => setIsOpen(false)}><Spinner/></Modal>
  }
  if (mutation.isSuccess && mutation.data) {
      return (
          <RequestDataAccessFormSuccess UrlOnSuccess={UrlOnSuccess} />
      )
  }
  if (mutation.error) {
    console.log('failure')
    return <RequestDataAccessFormFailure setIsOpen={setIsOpen} error={mutation.error} />
  }

  return (
    <Modal
      title='Request Dataset Access'
      description="To request access to this dataset, enter the title of your research, for how long you' ll need access to the data, and any comments regarding your request."
      close={() => setIsOpen(false)}
    >
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <FormFieldsRenderer
          register={register}
          button_text="Request Data Access"
          formState={formState}
          fields={{
            Title: {
              label: 'Title',
              placeholder: 'Title',
              type: 'text',
            },
            SubscriptionDays: {
              label: 'Access Duration (days)',
              placeholder: 'Access Duration (days)',
              type: 'text',
            },
            Description: {
              label: 'Request Comments',
              placeholder: 'Comments',
              type: 'textarea',
            },
          }}
        />
      </form>
    </Modal>
  )

};

export default RequestDataAccessForm;
