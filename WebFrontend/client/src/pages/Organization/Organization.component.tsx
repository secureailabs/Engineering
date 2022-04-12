import React, { useEffect, useState } from 'react';

import { ConditionalRender } from '@components/ConditionalRender';

import { TOrganizationProps } from './Organization.types';

import OrganizationSuccess from './Organization.success';
import OrganizationFailure from './Organization.failure';

import Title from '@components/Title';

//@ts-ignore
const Organization: React.FC<TOrganizationProps> = ({
  getOrganizationState,
  getOrganizationStart,
  getOrganizationReset,
  getOrganizationData,
  userData,
}) => {
  useEffect(() => {
    getOrganizationReset();
    getOrganizationStart();
  }, []);
  return (
    <>
      <Title>Organization</Title>
      <ConditionalRender
        //@ts-ignore
        state={getOrganizationState}
        success={() => (
          <OrganizationSuccess organizationData={getOrganizationData} />
        )}
        failure={OrganizationFailure}
      >
        <></>
      </ConditionalRender>
      );
    </>
  );
};

export default Organization;
