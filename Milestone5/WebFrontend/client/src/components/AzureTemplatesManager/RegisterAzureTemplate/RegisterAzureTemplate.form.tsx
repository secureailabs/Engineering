import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TRegisterAzureTemplateStart } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';

import { formData } from './RegisterAzureTemplate.data';

import Button from '@components/Button';

import { TRegisterAzureTemplateFormProps } from './RegisterAzureTemplate.types';

import RegisterAzureTemplateScheme from './RegisterAzureTemplate.scheme';

const RegisterAzureTemplateForm: React.FC<TRegisterAzureTemplateFormProps> = ({
  registerAzureTemplateStart,
  registerAzureTemplateReset,
}) => {
  useEffect(() => {
    registerAzureTemplateReset();
  }, []);
  const { register, handleSubmit, formState, trigger, watch } = useForm({
    resolver: yupResolver(RegisterAzureTemplateScheme),
    mode: 'onChange',
    // defaultValues: {
    //   Email: '',
    //   Password: '',
    //   PasswordConfirmation: '',
    //   // AccessRights: '',
    //   Name: '',
    //   Title: '',
    //   PhoneNumber: '',
    // }
  });
  const onSubmit: SubmitHandler<TRegisterAzureTemplateStart['TemplateData']> = (data) => {
    const newData: TRegisterAzureTemplateStart = {
      TemplateData: {
        ...data,
      }
    };

    console.log(newData);
    registerAzureTemplateStart(newData);
  };

  return (
    <div className="registertemplate">
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
          <div className="dcforminfo">
            <div className="dcforminfo__title">Create New Azure Template</div>
            <div className="dcforminfo__description">
              {/* To create a new Azure template, enter their credentials, their permissions
              and relevant information about them. */}
            </div>
          </div>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState, trigger)}
          />
          <Button disabled={!formState.isValid} type="submit">Create New Azure Template</Button>
          {console.log(formState)}
        </>
      </Form>
    </div>
  );
};

export default RegisterAzureTemplateForm;
