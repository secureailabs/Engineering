import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TUpdateAzureTemplateStart } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';

import { formData } from './UpdateAzureSecret.data';

import Button from '@components/Button';

import { TUpdateAzureSecretFormProps } from './UpdateAzureSecret.types';
import AcceptDigitalContractScheme from './UpdateAzureSecret.scheme';

const AcceptDigitalContract: React.FC<TUpdateAzureSecretFormProps> = ({
  updateAzureSecretStart,
  pullAzureTemplateData,
}) => {
  const { register, handleSubmit, formState } = useForm({
    resolver: yupResolver(AcceptDigitalContractScheme),
    mode: 'onChange',
  });
  const onSubmit: SubmitHandler<{ Secret: string }> = (data) => {
    const newData: TUpdateAzureTemplateStart = {
      TemplateGuid: pullAzureTemplateData.Template.TemplateGuid,
      TemplateData: {
        ...pullAzureTemplateData.Template,
        Secret: data.Secret
      }
    }
    console.log(data.Secret)
    console.log(newData)

    updateAzureSecretStart(newData);
  };
  return (
    <div className="acceptdigitalcontract">
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
        <div className='dcforminfo'>
          <div className='dcforminfo__title'>Update Azure Secret</div>
          <div className='dcforminfo__description'>
              {/* To accept this digital contract, enter the amount of days you want its logs to be kept in the SAIL database and the legal agreement you previously negotiated with the researcher organization. */}
          </div>
        </div>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button disabled={!formState.isValid} type="submit">Update Azure Secret</Button>
        </>
      </Form>
    </div>
  );
};

export default AcceptDigitalContract;
