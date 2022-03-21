import React, { useEffect } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TUpdateAccessRightsProps } from './UpdateAccessRights.types';

import UpdateAccessRightsForm from './UpdateAccessRights.form';
import UpdateAccessRightsSuccess from './UpdateAccessRights.success';
import UpdateAccessRightsFailure from './UpdateAccessRights.failure';

const UpdateAccessRights: React.FC<TUpdateAccessRightsProps> = ({
  putUpdateAccessRightsReset,
  putUpdateAccessRightsStart,
  putUpdateAccessRightsState,
  UserGuid,
  userData,
}) => {
  useEffect(() => {
    putUpdateAccessRightsReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={putUpdateAccessRightsState}
      success={UpdateAccessRightsSuccess}
      failure={UpdateAccessRightsFailure}
    >
      <UpdateAccessRightsForm
        UserGuid={UserGuid}
        userData={userData}
        putUpdateAccessRightsReset={putUpdateAccessRightsReset}
        putUpdateAccessRightsStart={putUpdateAccessRightsStart}
      />
    </ConditionalRender>
  );
};

export default UpdateAccessRights;
