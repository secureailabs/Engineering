import React, { useEffect } from 'react';
import { useState } from 'react';

import { TDigitalContractsSuccessProps } from './DigitalContracts.types';

import DigitalContractList from '@components/DigitalContractsManager/DigitalContractList';
import _ from 'lodash';
import getDCStage from '@utils/getDCStage';

import getPartnerOrg from '@utils/getPartnerOrg';

const DigitalContractsSuccess: React.FC<TDigitalContractsSuccessProps> = ({
  getAllDigitalContractsData,
  userData,
  stageView,
  setDigitalContractID,
}) => {
  const parsedData = Object.entries(getAllDigitalContractsData.DigitalContracts)
    .filter(
      (contract) =>
        getDCStage(contract[1].ContractStage, contract[1].ExpirationTime) ==
        stageView
    )
    .map(([key, value]) => {
      return {
        key,
        ...value,
        PartnerOrg: getPartnerOrg(
          userData,
          value.DataOwnerOrganization,
          value.DOOName,
          value.ROName
        ),
      };
    })
  .sort((elem1, elem2) => - (elem1.LastActivity - elem2.LastActivity));
    
  return (
    <DigitalContractList
      setDigitalContractID={setDigitalContractID}
      data={parsedData}
      stage={stageView}
    />
  );
};

export default DigitalContractsSuccess;
