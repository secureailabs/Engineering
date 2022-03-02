import React from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';
import stageNumberToString from '@utils/stageNumberToString';

import { TDigitalContractSuccessProps } from './DigitalContract.types';
import getPartnerOrg from '@utils/getPartnerOrg';

const DigitalContractSuccess: React.FC<TDigitalContractSuccessProps> = ({
  getDigitalContractData,
  //@ts-ignore
  userData,
}) => {
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
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {
      ...getDigitalContractData.DigitalContract,
      Status: stageNumberToString(
        getDigitalContractData.DigitalContract.ContractStage
      ),
      PartnerOrg: getPartnerOrg(
        userData,
        //@ts-ignore
        getDigitalContractData.DataOwnerOrganization,
        //@ts-ignore
        getDigitalContractData.DOOName,
        //@ts-ignore
        getDigitalContractData.ROName
      ),
      ProvisioningStatus: provisioning_status,
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
                label: 'Start Time',
                placeholder: 'Start Time',
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
                label: 'ProvisioningStatus',
                placeholder: 'ProvisioningStatus',
                type: 'text',
              },
            }}
          />
        </div>
      </Card>
    </>
  );
};

export default DigitalContractSuccess;
