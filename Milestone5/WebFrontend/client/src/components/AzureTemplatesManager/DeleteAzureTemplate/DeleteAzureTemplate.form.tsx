import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TDeleteAzureTemplateFormProps } from './DeleteAzureTemplate.types';
import { TDeleteAzureTemplateStart } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';

import { formData } from './DeleteAzureTemplate.data';

import Button from '@components/Button';

const DeleteAzureTemplate: React.FC<TDeleteAzureTemplateFormProps> = ({
  deleteAzureTemplateReset,
  deleteAzureTemplateStart,
  TemplateGuid
}) => {
  useEffect(() => {
    deleteAzureTemplateReset();
  }, []);
  const { register, handleSubmit, formState } = useForm({
    mode: 'onSubmit',
  });
  const onSubmit: SubmitHandler<TDeleteAzureTemplateStart> = (
    data
  ) => {
    const newData = {
      TemplateGuid: TemplateGuid
    };
    deleteAzureTemplateStart(newData);
  };
  return (
    <div className="deleteaccount">
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
        <div className='dcforminfo'>
          <div className='dcforminfo__title'>Delete Azure Template</div>
          <div className='dcforminfo__description'>
              Please confirm you want to delete this template.
          </div>
        </div>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button type="submit">Delete Template</Button>
        </>
      </Form>
    </div>
  );
};

export default DeleteAzureTemplate;
