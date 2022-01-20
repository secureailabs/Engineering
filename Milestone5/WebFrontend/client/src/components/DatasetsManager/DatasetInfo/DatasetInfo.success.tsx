import React, { useState } from 'react';
import { TDatasetInfoSuccess } from './DatasetInfo.types';
import RegisterDigitalContract from '@components/DigitalContractsManager/RegisterDigitalContract';
import Modal from 'react-modal';
import Button from '@components/Button';

import { AiFillCloseCircle } from 'react-icons/ai';

import InfoDisplay from '@components/InfoDisplay';
import { TInfoDisplay } from '@components/InfoDisplay/InfoDisplay.types';

const DatasetInfo: React.FC<TDatasetInfoSuccess> = ({
  getDatasetData,
  userData,
}) => {
  const [modalIsOpen, setIsOpen] = React.useState(false);

  if (getDatasetData) {
    const {
      DatasetName,
      Keywords,
      Description,
      DataOwnerGuid,
      JurisdictionalLimitations,
      OrganizationName,
      PublishDate,
      DatasetGuid,
    } = getDatasetData.Dataset;
    const info_display: TInfoDisplay['data'] = [
      {
        section_title: 'Keywords',
        section_data: Keywords,
      },
      {
        section_title: 'Description',
        section_data: Description,
      },
      {
        section_title: 'Data Owner',
        section_data: OrganizationName,
      },
      {
        section_title: 'Jurisdictional Limitations',
        section_data: JurisdictionalLimitations,
      },
      {
        section_title: 'Publish Date',
        section_data: PublishDate,
        to_locale_date_string: true,
      },
    ];
    return (
      <>
        <InfoDisplay data={info_display} />
        {DataOwnerGuid != userData?.OrganizationGuid && (
          <div className="datasetinfo__button">
            <Button onClick={() => setIsOpen(true)}>Request Access</Button>
          </div>
        )}
        <Modal isOpen={modalIsOpen} contentLabel="Example Modal">
          <div className="modal-container">
            <AiFillCloseCircle
              onClick={() => setIsOpen(false)}
              className="modal-close"
            />
            <RegisterDigitalContract
              closeModal={() => setIsOpen(false)}
              DatasetName={DatasetName}
              JurisdictionalLimitations={JurisdictionalLimitations}
              DatasetGuid={DatasetGuid}
              DataOwnerOrganization={DataOwnerGuid}
            />
          </div>
        </Modal>
      </>
    );
  }
  return <></>;
};

export default DatasetInfo;
