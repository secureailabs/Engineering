import React, { useEffect, useState } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TUpdateOrganizationProps } from './UpdateOrganization.types';

import UpdateOrganizationForm from './UpdateOrganization.form';
import UpdateOrganizationSuccess from './UpdateOrganization.success';
import UpdateOrganizationFailure from './UpdateOrganization.failure';

const UpdateOrganization: React.FC<TUpdateOrganizationProps> = ({
  putOrganizationReset,
  putOrganizationStart,
  putOrganizationState,
  organizationData,
  getOrganizationStart,
  userData,
}) => {
  const [success, updateSuccess] = useState(false);
  useEffect(() => {
    putOrganizationReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={putOrganizationState}
      success={() => (
        <UpdateOrganizationSuccess
          updateSuccess={updateSuccess}
          getOrganizationStart={getOrganizationStart}
          putOrganizationStart={putOrganizationStart}
          putOrganizationState={putOrganizationState}
        />
      )}
      failure={UpdateOrganizationFailure}
    >
      <UpdateOrganizationForm
        userData={userData}
        organizationData={organizationData}
        putOrganizationReset={putOrganizationReset}
        putOrganizationStart={putOrganizationStart}
      />
    </ConditionalRender>
  );
};

export default UpdateOrganization;
