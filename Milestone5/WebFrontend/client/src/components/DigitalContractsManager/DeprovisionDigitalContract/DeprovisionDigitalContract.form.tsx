import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TDeprovisionDigitalContactFormProps } from './DeprovisionDigitalContract.types';
import { TDeprovisionDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

import { formData } from './DeprovisionDigitalContract.data';

import Button from '@components/Button';

const DeprovisionDigitalContract: React.FC<TDeprovisionDigitalContactFormProps> = ({
  deprovisionDigitalContractStart,
  DigitalContractGuid,
}) => {
  const { register, handleSubmit, formState } = useForm({
    mode: 'onSubmit',
  });
  const onSubmit: SubmitHandler<TDeprovisionDigitalContractStart> = (
    data
  ) => {
    const newData = {
      DigitalContractGuid,
    };
    console.log(newData);
    deprovisionDigitalContractStart(newData);
  };
  return (
    <div className="activatedigitalcontract">
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
        <div className='dcforminfo'>
          <div className='dcforminfo__title'>Deprovision Digital Contract</div>
          <div className='dcforminfo__description'>
              Before deprovisioning this digital contract, make sure that all of its information is correct.
          </div>
        </div>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button type="submit">Deprovision Digital Contract</Button>
        </>
      </Form>
    </div>
  );
};

export default DeprovisionDigitalContract;
