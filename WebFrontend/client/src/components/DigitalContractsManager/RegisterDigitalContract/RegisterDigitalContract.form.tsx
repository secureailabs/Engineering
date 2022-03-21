import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TPostDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

import { formData } from './RegisterDigitalContract.data';

import Button from '@components/Button';

import { TRegisterDigitalContractFormProps } from './RegisterDigitalContract.types';

import RegisterDigitalContractScheme from './RegisterDigitalContract.scheme';

const RegisterDigitalContract: React.FC<TRegisterDigitalContractFormProps> = ({
  postDigitalContractReset,
  postDigitalContractStart,
  userData,
  DatasetGuid,
  JurisdictionalLimitations,
  DatasetName,
  DataOwnerOrganization
}) => {
  useEffect(() => {
    postDigitalContractReset();
  }, []);
  const { register, handleSubmit, formState } = useForm({
    resolver: yupResolver(RegisterDigitalContractScheme),
    mode: 'onSubmit',
  });
  const onSubmit: SubmitHandler<TPostDigitalContractStart> = (data) => {
    const newData = {
      ...data,
      //@ts-ignore
      Description: data['Request Comments'],
      Title: data['Title'],
      LegalAgreement: 'To be determined...',
      SubscriptionDays: data['SubscriptionDays'],
      DatasetGuid,
      DataOwnerOrganization: DataOwnerOrganization,
      VersionNumber: '1.0.0',
      DatasetDRMMetadataSize: 0,
      DatasetDRMMetadata: {},
    };
    //@ts-ignore
    delete newData['Request Comments'];

    console.log(newData);
    postDigitalContractStart(newData);
  };
  return (
    <div className="registerdigitalcontract">
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
      <>
        <div className='dcforminfo'>
          <div className='dcforminfo__title'>Request Dataset Access</div>
          <div className='dcforminfo__description'>
              To request access to this dataset, enter the title of your research, for how long you'll need access to the data, and any comments regarding your request.
          </div>
        </div>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button type="submit">Request Dataset Access</Button>
        </>
      </Form>
    </div>
  );
};

export default RegisterDigitalContract;
