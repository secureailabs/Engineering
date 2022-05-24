import React from 'react';

import { TDigitalContractsProps } from './DigitalContracts.types';

import { useQuery } from 'react-query';


import DigitalContractsSuccess from './DigitalContracts.success';
import DigitalContractsFailure from './DigitalContracts.failure';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import axios, { AxiosError } from 'axios';


import {
  TGetAllDigitalContractsSuccess,

} from '@app/redux/digitalContract/digitalContract.typeDefs';

import { axiosProxy } from '@app/redux/utils';


const fetch = async (): Promise<TGetAllDigitalContractsSuccess['DigitalContracts']> => {
  const res = await axios.get<TGetAllDigitalContractsSuccess>(
    `${axiosProxy()}/api/v1/DigitalContractManager/DigitalContracts`, 
    {
    withCredentials: true,
  });
  return res.data.DigitalContracts;
}

const DigitalContracts: React.FC<TDigitalContractsProps> = ({
  userData,
}) => {

  const { data, isLoading, status, error } = useQuery<TGetAllDigitalContractsSuccess['DigitalContracts'], AxiosError>(['digital-contracts'], fetch);
  if(isLoading){
      return <><Spinner/></>
  }
  if(status === 'success' && data){
      return (
          <StandardContent title="Digital Contracts">
            <DigitalContractsSuccess
              getAllDigitalContractsData={data}
              userData={userData}
          />
          </StandardContent>
      )
  }
  return <DigitalContractsFailure error={error} />

};

export default DigitalContracts;
