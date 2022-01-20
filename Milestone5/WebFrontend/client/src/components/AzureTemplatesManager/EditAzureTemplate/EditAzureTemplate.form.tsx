import React, { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import EditAzureTemplateScheme from './EditAzureTemplate.scheme';
import SelectAzureTemplate from '@components/AzureTemplatesManager/SelectAzureTemplate';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';
import Modal from 'react-modal';

import { TEditAzureTemplateForm } from './EditAzureTemplate.types';
import { TPatchAssociateAzureStart } from '@redux/digitalContract/digitalContract.typeDefs';

import { formData } from './EditAzureTemplate.data';

import Button from '@components/Button';
import { AiFillCloseCircle } from 'react-icons/ai';

const EditAzureTemplateForm: React.FC<TEditAzureTemplateForm> = ({
  patchAssociateAzureStart,
  digitalContractID,
}) => {
  const [modalAzureIsOpen, setAzureIsOpen] = React.useState(false);
  const { register, handleSubmit, formState, trigger } = useForm({
    resolver: yupResolver(EditAzureTemplateScheme),
    mode: 'onSubmit',
  });

  const onSubmit: SubmitHandler<{
    AzureTemplateGuid: TPatchAssociateAzureStart['AzureTemplateGuid'];
  }> = ({ AzureTemplateGuid }) => {
    patchAssociateAzureStart({
      AzureTemplateGuid,
      ListOfDigitalContracts: [digitalContractID],
    });
  };
  return (
    <>
      <div className="digitalcontractinfo__button">
        <Button onClick={() => setAzureIsOpen(true)}>
          Select Azure Template
        </Button>
      </div>
      <Modal isOpen={modalAzureIsOpen} contentLabel="Modal">
        <div className="modal-container">
          <AiFillCloseCircle
            onClick={() => setAzureIsOpen(false)}
            className="modal-close"
          />
          <SelectAzureTemplate
            onClick={(key) => {
              onSubmit({ AzureTemplateGuid: key });
            }}
          />
        </div>
      </Modal>
    </>
  );
};

export default EditAzureTemplateForm;
