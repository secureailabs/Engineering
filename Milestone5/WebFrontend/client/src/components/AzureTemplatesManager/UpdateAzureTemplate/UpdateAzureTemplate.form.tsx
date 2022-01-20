import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import Modal from 'react-modal';
import { AiFillCloseCircle } from 'react-icons/ai';

import UpdateOrganizationScheme from './UpdateAzureTemplate.scheme';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TUpdateAzureTemplateFormProps } from './UpdateAzureTemplate.types';
import {
  TUpdateAzureTemplateStart,
  TPullAzureTemplateSuccess,
} from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';
import UpdateAzureSecret from '../UpdateAzureSecret';
import DeleteAzureTemplate from '../DeleteAzureTemplate';

import { formData } from './UpdateAzureTemplate.data';

import Button from '@components/Button';

const UpdateAzureTemplate: React.FC<TUpdateAzureTemplateFormProps> = ({
  updateAzureTemplateReset,
  updateAzureTemplateStart,
  pullAzureTemplateData,
  slideToPrev,
}) => {
  const [secretModalIsOpen, setSecretIsOpen] = React.useState(false);
  const [deleteModalIsOpen, setDeleteIsOpen] = React.useState(false);

  const { register, handleSubmit, formState, trigger } = useForm({
    resolver: yupResolver(UpdateOrganizationScheme),
    mode: 'onChange',
    defaultValues: {
      ...pullAzureTemplateData.Template,
    },
  });

  const onSubmit: SubmitHandler<TUpdateAzureTemplateStart['TemplateData']> = (data) => {
    updateAzureTemplateStart({
      TemplateGuid:
        pullAzureTemplateData.Template.TemplateGuid,
      TemplateData: {
        ...data,
        State: pullAzureTemplateData.Template.State
      },
    });
  };
  console.log(formState)
  console.log(formState.isValid)
  console.log(formState.errors)
  return (
    <>
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <div id='buttoninput' className='text-input'>
            <label id='buttonlabel' className='text-input__label'>Secret</label>
            <div>
              <Button type='button' onClick={() => setSecretIsOpen(true)}>Update Azure Secret</Button>
            </div>
          </div>
          <div className='bottombuttondiv'>
            <Button type='button' onClick={() => setDeleteIsOpen(true)}>Delete Azure Template</Button>
          </div>
          <div className='bottombuttondiv'>
           <Button type='submit' disabled={!(formState.isValid && formState.isDirty)}>
              Update Azure Template
            </Button>
          </div>
          <div className='text-input__label'>
            Note: {pullAzureTemplateData.Template.Note}
          </div>
        </>
      </Form>
      <Modal isOpen={secretModalIsOpen} contentLabel="Example Modal">
            <div className="modal-container">
              <AiFillCloseCircle
                onClick={() => setSecretIsOpen(false)}
                className="modal-close"
              />
              <UpdateAzureSecret
                closeModal={() => setSecretIsOpen(false)}
              />
            </div>
          </Modal>
          <Modal isOpen={deleteModalIsOpen} contentLabel="Example Modal">
            <div className="modal-container">
              <AiFillCloseCircle
                onClick={() => setDeleteIsOpen(false)}
                className="modal-close"
              />
              <DeleteAzureTemplate
                TemplateGuid={pullAzureTemplateData.Template.TemplateGuid}
                closeModal={() => {
                  setDeleteIsOpen(false);
                  slideToPrev();
                }}
              />
            </div>
          </Modal>
      </>
  );
};

export default UpdateAzureTemplate;
