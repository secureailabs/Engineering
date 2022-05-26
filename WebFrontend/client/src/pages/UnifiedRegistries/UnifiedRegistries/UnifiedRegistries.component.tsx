import React, { useEffect, useState } from 'react';
import axios from 'axios'
import ConditionalRender  from '@components/ConditionalRender2';

import { TUnifiedRegistriesProps } from './UnifiedRegistries.types';
import { CSSTransition } from 'react-transition-group';

import UnifiedRegistriesSuccess from './UnifiedRegistries.success';
import UnifiedRegistriesFailure from './UnifiedRegistries.failure';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { HiArrowLeft } from 'react-icons/hi';
import VirtualMachineInfo from '@components/VirtualMachineInfo';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import { demo_data } from "@APIs/unifiedRegistry/unifiedRegistry.data";

import { useQuery } from 'react-query';
import { TGetAllUnifiedRegistriesSuccess } from '@APIs/unifiedRegistry/unifiedRegistry.types';
import { AxiosError } from 'axios';
import { axiosProxy } from '@redux/utils';


const mode = localStorage.getItem("mode")



const UnifiedRegistries: React.FC<TUnifiedRegistriesProps> = () => {

  const fetch = async (): TGetAllUnifiedRegistriesSuccess['UnifiedRegistries'] => {
    if(mode == "demo"){
      return demo_data.UnifiedRegistries;

    }
    
    const res = await axios.get<TGetAllUnifiedRegistriesSuccess>
    (`${axiosProxy()}/api/v1/DatasetManager/PullDataset?DatasetGuid`, 
    {
      withCredentials: true,
    });
    return res.data.UnifiedRegistries;
  }

  // eslint-disable-next-line max-len
  const { data, status, isLoading, error } = useQuery<TGetAllUnifiedRegistriesSuccess, AxiosError>(["organizations"], () => demo_data);

  if (isLoading) {
    return <><Spinner /></>
  }
  if (status === 'success' && data) {
    return (
      <StandardContent title="Unified Registries">
        <UnifiedRegistriesSuccess
          getAllUnifiedRegistriesData={data}
        />
      </StandardContent>
    )
  }
  return <UnifiedRegistriesFailure error={error} />
};

export default UnifiedRegistries;
