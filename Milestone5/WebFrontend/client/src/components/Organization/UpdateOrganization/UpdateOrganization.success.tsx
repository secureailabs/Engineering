import React, { useEffect } from 'react';

import { TUpdateOrganizationSuccessProps } from './UpdateOrganization.types';

const UpdateOrganizationSuccess = ({
  updateSuccess,
  getOrganizationStart,
  putOrganizationState,
}: TUpdateOrganizationSuccessProps) => {
  useEffect(() => {
    if (putOrganizationState === 'success') {
      updateSuccess(true);
      getOrganizationStart();
    }
  }, [putOrganizationState]);
  return <>Form Updated Successfuly</>;
};

export default UpdateOrganizationSuccess;
