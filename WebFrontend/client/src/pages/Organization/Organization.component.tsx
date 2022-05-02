import React, { useEffect, useState } from 'react';

import { ConditionalRender } from '@components/ConditionalRender';

import { TOrganizationProps } from './Organization.types';

import OrganizationSuccess from './Organization.success';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import OrganizationFailure from './Organization.failure';

import { useQuery } from 'react-query';

import Title from '@components/Title';

import axios from 'axios';

import { axiosProxy, tokenConfig } from '@redux/utils';

import Spinner, { SpinnerOnly } from '@components/Spinner';


//@ts-ignore
const Organization: React.FC<TOrganizationProps> = () => {
  console.log(localStorage.getItem('token'));
  const { data, status } = useQuery('my-organization', () => axios.get(`${axiosProxy()}/api/v1/AccountManager/Organization/Information`, {
    withCredentials: true,
  }).then((res) => res.data.OrganizationInformation));
  if(status === 'loading'){
      return <Spinner />;
  }
  console.log("DATA", data);
  return (
    <>
     <StandardContent title="Organization">
        <OrganizationSuccess organizationData={data} />
      </StandardContent>
    </>
  );
};

export default Organization;
