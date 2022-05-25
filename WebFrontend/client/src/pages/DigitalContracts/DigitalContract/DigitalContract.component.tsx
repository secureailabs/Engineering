import React, { useEffect } from 'react';

import axios, { AxiosError, AxiosResponse } from 'axios';

import { useParams } from 'react-router';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import { ConditionalRender } from '@components/ConditionalRender';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';
import { axiosProxy, tokenConfig } from '@APIs/utils';
import type { IDefaults } from '@APIs/typedefs';

import Spinner from '@components/Spinner/SpinnerOnly.component';

import { useQuery } from 'react-query';

import { TDigitalContractProps } from './DigitalContract.types';

import DigitalContractFailure from './DigitalContract.failure';

import DigitalContractSuccess from './DigitalContract.success';

import {

  TGetDigitalContractSuccess,

} from '@APIs/digitalContract/digitalContract.typeDefs';
import _ from 'lodash';

const fetch = async ({ id }: { id: string }): Promise<TGetDigitalContractSuccess> => {
  const res = await axios.get<TGetDigitalContractSuccess>(
    `${axiosProxy()}/api/v1/DigitalContractManager/PullDigitalContract?DigitalContractGuid=${id}`,
    {
      withCredentials: true,
    });
  return res.data;
}


const DigitalContract: React.FC<TDigitalContractProps> = ({ userData }) => {
  const { id } = useParams();
  const { data, isLoading, status, error } = useQuery<TGetDigitalContractSuccess, AxiosError>
    (['digital-contract', id], () => fetch({ id: id || "" }));


  if (isLoading) {
    return (
      <>
        <Spinner />
      </>
    )
  }
  if (status === 'success' && data && !_.isEmpty(data)) {
    return <>
      <StandardContent title="Digital Contract">
        <DigitalContractSuccess getDigitalContractData={data} userData={userData} />
      </StandardContent>
    </>
  }

  return <DigitalContractFailure error={error} />;


};

export default DigitalContract;
