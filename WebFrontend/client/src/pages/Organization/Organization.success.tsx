import React from 'react';

import UpdateOrganization from '@components/Organization/UpdateOrganization2';

import { TOrganizationSuccessProps } from './Organization.types';

const OrganizationSuccess: React.FC<TOrganizationSuccessProps> = ({
  organizationData,
}) => {
  return (
    <>
      <UpdateOrganization organizationData={organizationData} />
    </>
  );
};

export default OrganizationSuccess;
