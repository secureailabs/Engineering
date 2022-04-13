//@ts-nocheck
import React, { useEffect } from 'react';

import { TUnifiedRegistryProps } from './UnifiedRegistry.types';

import UnifiedRegistrySuccess from './UnifiedRegistry.success';
import UnifiedRegistryFailure from './UnifiedRegistry.failure';

import axios, { AxiosError } from 'axios';

import { useParams } from 'react-router';

import { ConditionalRender } from '@components/ConditionalRender';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import { demo_data } from "@redux/unifiedRegistry/unifiedRegistry.data";
import { TGetUnifiedRegistrySuccess } from '@redux/unifiedRegistry/unifiedRegistry.types';

import { axiosProxy } from '@redux/utils';
import { useQuery } from 'react-query';


const UnifiedRegistry: React.FC<TUnifiedRegistryProps> = () => {
  const { id } = useParams();


  const fetch = (): TGetUnifiedRegistrySuccess['UnifiedRegistry'] => {
    //@ts-nocheck
    return demo_data?.UnifiedRegistries?.[id || ""];
    // const res = await axios.get<TGetUnifiedRegistrySuccess>
    // (`${axiosProxy()}/api/v1/DatasetManager/PullDataset?DatasetGuid=${id}`, 
    // {
    //   withCredentials: true,
    // });
    // return res.data.UnifiedRegistry;
  }

  const { data, isLoading, status, error } = 
  useQuery<TGetUnifiedRegistrySuccess['UnifiedRegistry'], AxiosError>(['unified', id], () => fetch());
  

  if(isLoading){
    return <><Spinner/></>
  }
  if(status === 'success' && data){
    return (
        <StandardContent title="Organization">
          <UnifiedRegistrySuccess
            getUnifiedRegistryData={data}
        />
        </StandardContent>
    )
  }
  return <UnifiedRegistryFailure error={error} />

};
export default UnifiedRegistry;
