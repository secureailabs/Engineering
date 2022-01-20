import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TActivateDigitalContactFormProps } from './ActivateDigitalContract.types';
import { TPatchActivateDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

import { formData } from './ActivateDigitalContract.data';

import Button from '@components/Button';

const ActivateDigitalContract: React.FC<TActivateDigitalContactFormProps> = ({
  patchActivateDigitalContractReset,
  patchActivateDigitalContractStart,
  getDigitalContractData,
  DigitalContractGuid,
}) => {
  // useEffect(() => {
  //   patchActivateDigitalContractReset();
  // }, []);
  const { register, handleSubmit, formState } = useForm({
    // resolver: yupResolver(ActivateDigitalContractScheme),
    mode: 'onSubmit',
    // defaultValues: {
    //   LegalAgreement: getDigitalContractData?.DigitalContract.LegalAgreement,
    //   EULA: getDigitalContractData?.DigitalContract.Eula,
    // },
  });
  const onSubmit: SubmitHandler<TPatchActivateDigitalContractStart> = (
    data
  ) => {
    const newData = {
      ...data,
      DigitalContractGuid,
      LegalAgreement: getDigitalContractData?.DigitalContract.LegalAgreement || '',
      EULA: getDigitalContractData?.DigitalContract.Eula || '',
    };
    console.log(newData);
    patchActivateDigitalContractStart(newData);
  };
  return (
    <div className="activatedigitalcontract">
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
        <div className='dcforminfo'>
          <div className='dcforminfo__title'>Accept Digital Contract</div>
          <div className='dcforminfo__description'>
              Before activating this digital contract, make sure that all of its information is correct.
          </div>
        </div>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button type="submit">Activate Digital Contract</Button>
        </>
      </Form>
    </div>
  );
};

export default ActivateDigitalContract;
