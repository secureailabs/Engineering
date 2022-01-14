import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TProvisionDigitalContactFormProps } from './ProvisionDigitalContract.types';
import { TPatchActivateDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

import { formData } from './ProvisionDigitalContract.data';

import Button from '@components/Button';

const ProvisionDigitalContract: React.FC<TProvisionDigitalContactFormProps> = ({
  provisionDigitalContractStart,
  DigitalContractGuid,
}) => {
  const { register, handleSubmit, formState } = useForm({
    mode: 'onSubmit',
  });
  const onSubmit: SubmitHandler<TPatchActivateDigitalContractStart> = (
    data
  ) => {
    const newData = {
      DigitalContractGuid,
    };
    console.log(newData);
    provisionDigitalContractStart(newData);
  };
  return (
    <div className="activatedigitalcontract">
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
        <div className='dcforminfo'>
          <div className='dcforminfo__title'>Provision Digital Contract</div>
          <div className='dcforminfo__description'>
              Before provisioning this digital contract, make sure that all of its information is correct.
          </div>
        </div>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button type="submit">Provision Digital Contract</Button>
        </>
      </Form>
    </div>
  );
};

export default ProvisionDigitalContract;
