import React, { useEffect } from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import axios, { AxiosError } from 'axios';

import { useParams } from 'react-router-dom';

import { ConditionalRender } from '@components/ConditionalRender';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';

import Spinner from '@components/Spinner/SpinnerOnly.component';
import { TDatasetVersionProps } from './DatasetVersion.types';

import DatasetVersionSuccess from './DatasetVersion.success';
import { TGetDatasetVersionSuccess, TGetDatasetSuccess } from '@redux/dataset/dataset.typeDefs';
import DatasetVersionFailure from "./DatasetVersion.failure";
import { axiosProxy } from '@redux/utils';
import { useQuery } from 'react-query';
import { demo_data } from "@redux/dataset/dataset.data";


const fetch = async ({ id, version }: { id: string, version: string }): Promise<TGetDatasetVersionSuccess['Dataset']> => {
  return demo_data.Datasets[id].Versions[version];
  const res = await axios.get<TGetDatasetVersionSuccess>
  (`${axiosProxy()}/api/v1/DatasetManager/PullDataset?DatasetGuid=${id}`, 
  {
    withCredentials: true,
  });
  return res.data.Dataset;
}

const fetch2 = async ({ id }: { id: string }): Promise<TGetDatasetSuccess['Dataset']> => {
  return demo_data.Datasets[id];
  const res = await axios.get<TGetDatasetSuccess>
  (`${axiosProxy()}/api/v1/DatasetManager/PullDataset?DatasetGuid=${id}`, 
  {
    withCredentials: true,
  });
  return res.data.Dataset;
}

const DatasetVersion: React.FC<TDatasetVersionProps> = () => {
  const  { version, id } = useParams();

   
  const { data, isLoading, status, error } = 
    useQuery<TGetDatasetVersionSuccess['Dataset'], AxiosError>(['dataset', id], () => fetch({ id: id || "", version: version || "" }));

    const { data: dataset_data, isLoading: dataset_is_loading, status: datasets_status, error: dataset_error } = 
    useQuery<TGetDatasetSuccess['Dataset'], AxiosError>(['dataset', id], () => fetch2({ id: id || "" }));
  if(isLoading || dataset_is_loading){
      return <><Spinner/></>
  }
  if(status === 'success' && data && datasets_status ==='success' && dataset_data){
      return (
          <StandardContent title="Organization">
            <DatasetVersionSuccess
              getDatasetVersionData={data}
              getDatasetData={dataset_data}
          />
          </StandardContent>
      )
  }
  return <DatasetVersionFailure error={error} />


};

export default DatasetVersion;
