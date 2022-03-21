import React from 'react';
import { TDigitalContractInfoSuccess } from './DigitalContractInfo.types';
import stageNumberToString from '@utils/stageNumberToString';
import AcceptDigitalContract from '@components/DigitalContractsManager/AcceptDigitalContract';
import ActivateDigitalContract from '../ActivateDigitalContract';
import downloadFileText from '@utils/downloadFileText';
import allowedDCActions from '@utils/allowedDCActions';
import getPartnerOrg from '@utils/getPartnerOrg';
import Button from '@components/Button';
import Modal from 'react-modal';
import { AiFillCloseCircle } from 'react-icons/ai';
import EditAzureTemplate from '@components/AzureTemplatesManager/EditAzureTemplate';
import ProvisionDigitalContract from '@components/DigitalContractsManager/ProvisionDigitalContract';
import DeprovisionDigitalContract from '@components/DigitalContractsManager/DeprovisionDigitalContract';

import InfoDisplay from '@components/InfoDisplay';
import { TInfoDisplay } from '@components/InfoDisplay/InfoDisplay.types';

const DigitalContractInfo: React.FC<TDigitalContractInfoSuccess> = ({
  getDigitalContractData,
  userData,
  digitalContractID,
}) => {
  const [modalIsOpen, setIsOpen] = React.useState(false);

  if (getDigitalContractData) {
    const data = getDigitalContractData.DigitalContract;
    const [
      canAcceptDigitalContract,
      canActivateDigitalContract,
      canSelectAzureTemplate,
      canProvisionDigitalContract,
      canDeprovisionDigitalContract,
    ] = allowedDCActions(getDigitalContractData, userData);
    let color;
    let provisioning_status;
    switch (data.ProvisioningStatus) {
      case 1:
        color = 'yellow';
        provisioning_status = '🟡 Provisioning';
        break;
      case 2:
        color = 'green';
        provisioning_status = '🟢 Ready';
        break;
      case 3:
        color = 'grey';
        provisioning_status = '🟠 Not Provisioned';
        break;
      case 4:
        color = 'red';
        provisioning_status = '🔴 Provisioning Failed'
      default:
        color = 'grey';
        provisioning_status = '🟠 Not Provisioned';

        break;
    }

    const info_display: TInfoDisplay['data'] = [
      {
        section_title: 'Title',
        section_data: data.Title,
      },
      {
        section_title: 'Dataset',
        section_data: data.DatasetName,
      },
      {
        section_title: 'Status',
        section_data: stageNumberToString(data.ContractStage, [canProvisionDigitalContract, canDeprovisionDigitalContract, getDigitalContractData.DigitalContract.HostForVirtualMachines]),
      },
      {
        section_title: 'Description',
        section_data: data.Description,
      },
      {
        section_title: 'Partner Organization',
        section_data: getPartnerOrg(
          userData,
          //@ts-ignore
          getDigitalContractData.DataOwnerOrganization,
          //@ts-ignore
          getDigitalContractData.DOOName,
          //@ts-ignore
          getDigitalContractData.ROName
        ),
      },
      {
        section_title: 'Data Owner',
        //@ts-ignore
        section_data: getDigitalContractData.DOOName,
      },
      {
        section_title: 'Virtual Machine Host',
        section_data: data.HostForVirtualMachines,
        conditional: data.ContractStage >= 2,
      },
      {
        section_title: 'Host Region',
        //@ts-ignore
        section_data: data.HostRegion,
        conditional: data.ContractStage >= 2,
      },
      {
        section_title: 'Number of Virtual Machines',
        section_data: data.NumberOfVirtualMachines,
        conditional: data.ContractStage >= 2,
      },
      {
        section_title: 'Number of Virtual CPUs',
        section_data: data.NumberOfVCPU,
        conditional: data.ContractStage >= 2,
      },
      {
        section_title: 'Activation Time',
        section_data: data.ActivationTime,
        conditional: data.ContractStage >= 3,
        to_locale_date_string: true,
      },
      {
        section_title: 'Expiration Time',
        section_data: data.ExpirationTime,
        conditional: data.ContractStage >= 3,
        to_locale_date_string: true,
      },
      {
        section_title: 'Azure Template',
        section_data: data.AzureTemplateGuid || 'n/a',
      },
      {
        section_title: 'Contract Duration',
        section_data: `${data.SubscriptionDays} days`,
      },
      {
        section_title: 'EULA',
        section_data: data.Eula,
      },
      {
        section_title: 'Legal Agreement',
        section_data: (
          <>
            {data.LegalAgreement}{' '}
            <div
              onClick={() =>
                downloadFileText(data.LegalAgreement, 'LegalAgreement.txt')
              }
            >
              Download
            </div>
          </>
        ),
      },
      {
        section_title: 'Provisioning Status',
        section_data: provisioning_status,
        // color,
      },
      {
        section_title: 'Note',
        section_data: data.Note,
      },
    ];
    const title = `Digital Contract - ${data.Title}`;
    return (
      <>
        <InfoDisplay data={info_display} />
        <>
        <div style={{
          display: 'grid', 
          justifyContent: 'space-around',
          gridTemplateColumns: 
            (canSelectAzureTemplate && 
              (canProvisionDigitalContract || canDeprovisionDigitalContract)) 
            ? '10rem auto':'auto',
          gridTemplateRows: '2.75rem'
          }}>
        {(canAcceptDigitalContract || canActivateDigitalContract) && (
            <div className="digitalcontractinfo__button">
              <Button onClick={() => setIsOpen(true)}>
                {canAcceptDigitalContract
                  ? 'Accept Digital Contract'
                  : 'Activate Digital Contract'}
              </Button>
            </div>
          )}
          {canSelectAzureTemplate && (
            <EditAzureTemplate
              digitalContractID={digitalContractID}
            />
          )}
          {(canProvisionDigitalContract || canDeprovisionDigitalContract) && (
            <div className="digitalcontractinfo__button">
              <Button onClick={() => setIsOpen(true)}>
              {canProvisionDigitalContract
                  ? 'Provision Digital Contract'
                  : 'Deprovision Digital Contract'}
              </Button>
            </div>
          )}
        </div>
          <Modal isOpen={modalIsOpen} contentLabel="Example Modal">
            <div className="modal-container">
              <AiFillCloseCircle
                onClick={() => setIsOpen(false)}
                className="modal-close"
              />
              {canAcceptDigitalContract && (
                <AcceptDigitalContract
                  DigitalContractGuid={digitalContractID}
                />
              )}
              {canActivateDigitalContract && (
                <ActivateDigitalContract
                  DigitalContractGuid={digitalContractID}
                />
              )}
              {canProvisionDigitalContract && (
                <ProvisionDigitalContract
                  DigitalContractGuid={digitalContractID}
                />
              )}
              {canDeprovisionDigitalContract && (
                <DeprovisionDigitalContract 
                  DigitalContractGuid={digitalContractID}
                />
              )}
            </div>
          </Modal>
          {!(
            canAcceptDigitalContract ||
            canActivateDigitalContract ||
            canSelectAzureTemplate ||
            canProvisionDigitalContract ||
            canDeprovisionDigitalContract
          ) && (
            <div className="digitalcontractinfo__noactionsmessage">
              No actions available at the moment.
            </div>
          )}
        </>
      </>
    );
  }
  return <></>;
};

export default DigitalContractInfo;
