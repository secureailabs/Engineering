import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

// import { TLoginFormProps } from './Login.types';
import { TPatchAcceptDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

import { formData } from './AcceptDigitalContract.data';

import Button from '@components/Button';

import { TAcceptDigitalContactFormProps } from './AcceptDigitalContract.types';
import AcceptDigitalContractScheme from './AcceptDigitalContract.scheme';

const AcceptDigitalContract: React.FC<TAcceptDigitalContactFormProps> = ({
  patchAcceptDigitalContractReset,
  patchAcceptDigitalContractStart,
  DigitalContractGuid,
}) => {
  const { register, handleSubmit, formState } = useForm({
    resolver: yupResolver(AcceptDigitalContractScheme),
    mode: 'onSubmit',
  });
  const onSubmit: SubmitHandler<TPatchAcceptDigitalContractStart> = (data) => {
    console.log(data)
    const newData = {
      ...data,
      DigitalContractGuid: DigitalContractGuid,
    };
    console.log(newData);

    patchAcceptDigitalContractStart(newData);
  };
  return (
    <div className="acceptdigitalcontract">
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
        <div className='dcforminfo'>
          <div className='dcforminfo__title'>Accept Digital Contract</div>
          <div className='dcforminfo__description'>
              To accept this digital contract, enter the amount of days you want its logs to be kept in the SAIL database and the legal agreement you previously negotiated with the researcher organization.
          </div>
        </div>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button type="submit">Accept Digital Contract</Button>
        </>
      </Form>
    </div>
  );
};

export default AcceptDigitalContract;
