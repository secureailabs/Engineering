import React, { useState } from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';

import Button from '@secureailabs/web-ui/components/Button';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';
import stageNumberToString from '@utils/stageNumberToString';

import { TDigitalContractSuccessProps } from './DigitalContract.types';
import AcceptDigitalContractForm from '@components/DigitalContractForms/AcceptDigitalContractForm';
import getPartnerOrg from '@utils/getPartnerOrg';
import { unix } from 'dayjs'

const DigitalContractSuccess: React.FC<TDigitalContractSuccessProps> = ({
  getDigitalContractData,
  userData,
}) => {
  const [modalIsOpen, setIsOpen] = useState(false)

  let provisioning_status;
  switch (getDigitalContractData.DigitalContract.ProvisioningStatus) {
    case 1:
      provisioning_status = '🟡 Provisioning';
      break;
    case 2:
      provisioning_status = '🟢 Ready';
      break;
    case 3:
      provisioning_status = '🟠 Not Provisioned';
      break;
    case 4:
      provisioning_status = '🔴 Provisioning Failed';
      break;
    default:
      provisioning_status = '🟠 Not Provisioned';
      break;
  }
  const { register, formState } = useForm({
    mode: 'onSubmit',
    defaultValues: {
      ...getDigitalContractData,
      Status: stageNumberToString(
        getDigitalContractData.DigitalContract.ContractStage
      ),
      PartnerOrg: getPartnerOrg(
        userData,
        getDigitalContractData.DataOwnerOrganization,
        getDigitalContractData.DOOName,
        getDigitalContractData.ROName
      ),
      ProvisioningStatus: provisioning_status,
      ActivationTime: unix(getDigitalContractData.DigitalContract.ActivationTime),
      ExpirationTime: unix(getDigitalContractData.DigitalContract.ExpirationTime),
    },
  });
  return (
    <>
      <Card primaryText="">
        <div className="form-double">
          <FormFieldsRenderer
            register={register}
            formState={formState}
            fields={{
              Title: {
                label: 'Title',
                placeholder: 'Title',
                type: 'text',
              },
              DatasetName: {
                label: 'Data Federation',
                placeholder: 'Data Federation',
                type: 'text',
              },
              Status: {
                label: 'Status',
                placeholder: 'Status',
                type: 'text',
              },
              Description: {
                label: 'Description',
                placeholder: 'Description',
                type: 'text',
              },
              PartnerOrg: {
                label: 'Partner Organizatoin',
                placeholder: 'Partner Organization',
                type: 'text',
              },
              DOOName: {
                label: 'Data Owner',
                placeholder: 'Data Owner',
                type: 'text',
              },

              HostRegion: {
                label: 'Allowable Host Regions',
                placeholder: 'Allowable Host Regions',
                type: 'text',
              },
              NumberOfVCPU: {
                label: 'Number of Virtual CPUs',
                placeholder: 'Number of Virtual CPUs',
                type: 'text',
              },
              ActivationTime: {
                label: 'Start Date',
                placeholder: 'Start Date',
                type: 'text',
              },
              ExpirationTime: {
                label: 'Data Retention Time',
                placeholder: 'Data Retention Time',
                type: 'text',
                
              },

              ContractDuration: {
                label: 'Contract Duration',
                placeholder: 'Contract Duration',
                type: 'text',
              },
              EULA: {
                label: 'EULA',
                placeholder: 'EULA',
                type: 'text',
              },
              LegalAgreement: {
                label: 'Legal Agreement',
                placeholder: 'Legal Agreement',
                type: 'text',
              },
              ProvisioningStatus: {
                label: 'Provisioning Status',
                placeholder: 'Provisioning Status',
                type: 'text',
              },
            }}
          />
          <div
            style={{
              width: '20rem',
              // marginLeft: '5rem',
            }}
          >
            {
              (getDigitalContractData.DigitalContract.ContractStage == 1 && getDigitalContractData.DataOwnerOrganization == userData?.OrganizationGuid) && <Button full={false} button_type="primary" onClick={() => { setIsOpen(true) }}>
                Accept Digital Contract
              </Button>
            }
          </div>
          {modalIsOpen &&
            <AcceptDigitalContractForm setIsOpen={setIsOpen} DigitalContractGuid={getDigitalContractData.DigitalContract.DigitalContractGuid} />
          }
        </div>
      </Card>
    </>
  );
};

export default DigitalContractSuccess;
