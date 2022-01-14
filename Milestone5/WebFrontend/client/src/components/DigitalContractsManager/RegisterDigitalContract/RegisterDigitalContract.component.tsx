import React, { useEffect } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TRegisterDigitalContractProps } from './RegisterDigitalContract.types';

import RegisterDigitalContractForm from './RegisterDigitalContract.form';
import RegisterDigitalContractSuccess from './RegisterDigitalContract.success';
import RegisterDigitalContractFailure from './RegisterDigitalContract.failure';

const RegisterDigitalContract: React.FC<TRegisterDigitalContractProps> = ({
  postDigitalContractStart,
  postDigitalContractReset,
  postDigitalContractState,
  userData,
  JurisdictionalLimitations,
  DatasetName,
  DatasetGuid,
  closeModal,
  DataOwnerOrganization,
}) => {
  // console.log(DatasetName);
  // console.log(JurisdictionalLimitations);
  useEffect(() => {
    postDigitalContractReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={postDigitalContractState}
      success={() => <RegisterDigitalContractSuccess closeModal={closeModal} />}
      failure={() => <RegisterDigitalContractFailure />}
    >
      <RegisterDigitalContractForm
        postDigitalContractReset={postDigitalContractReset}
        postDigitalContractStart={postDigitalContractStart}
        userData={userData}
        DatasetGuid={DatasetGuid}
        JurisdictionalLimitations={JurisdictionalLimitations}
        DatasetName={DatasetName}
        DataOwnerOrganization={DataOwnerOrganization}
      />
    </ConditionalRender>
  );
};

export default RegisterDigitalContract;
