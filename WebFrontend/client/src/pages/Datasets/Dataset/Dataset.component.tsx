//@ts-nocheck
import React from 'react';

import _ from 'lodash';

import axios, { AxiosError } from 'axios';

import { useParams } from 'react-router';


import Spinner from '@components/Spinner/SpinnerOnly.component';
import { TDatasetProps } from './Dataset.types';

import DatasetSuccess from './Dataset.success';
import DatasetFailure from "./Dataset.failure";
import { TGetDatasetSuccess } from '@app/redux/dataset/dataset.typeDefs';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import { axiosProxy } from '@app/redux/utils';
import { useQuery } from 'react-query';

import { demo_data } from "@app/redux/dataset/dataset.data";


const fetch = async ({ id }: { id: string }): Promise<TGetDatasetSuccess['Dataset']> => {
  // return demo_data?.Datasets?.[id];
  const res = await axios.get<TGetDatasetSuccess>
  (`${axiosProxy()}/api/v1/DatasetManager/PullDataset?DatasetGuid=${id}`, 
  {
    withCredentials: true,
  });
  return res.data.Dataset;
}


const Dataset: React.FC<TDatasetProps> = ({ userData }) => {

  const { id } = useParams();

  
  const { data, isLoading, status, error } = 
    useQuery<TGetDatasetSuccess['Dataset'], AxiosError>(['dataset', id], () => fetch({ id: id || "" }));
  if(isLoading){
      return <><Spinner/></>
  }
  if(status === 'success' && data){
      return (
          <StandardContent title="Dataset">
            <DatasetSuccess
            getDatasetData={data}
            userData={userData}
          />
          </StandardContent>
      )
  }
  return <DatasetFailure error={error} />

};

export default Dataset;
