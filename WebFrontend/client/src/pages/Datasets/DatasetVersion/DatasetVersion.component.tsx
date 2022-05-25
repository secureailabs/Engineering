//@ts-nocheck
import React from 'react';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import { AxiosError } from 'axios';

import { useParams } from 'react-router-dom';


import Spinner from '@components/Spinner/SpinnerOnly.component';
import { TDatasetVersionProps } from './DatasetVersion.types';

import DatasetVersionSuccess from './DatasetVersion.success';
import { TGetDatasetVersionSuccess, TGetDatasetSuccess } from '@APIs/dataset/dataset.typeDefs';
import DatasetVersionFailure from "./DatasetVersion.failure";
import { useQuery } from 'react-query';
import { demo_data } from "@APIs/dataset/dataset.data";



const DatasetVersion: React.FC<TDatasetVersionProps> = () => {
  const { version, id } = useParams();

  const fetch = (): TGetDatasetVersionSuccess['Dataset'] => {
    //@ts-ignore
    return demo_data?.Datasets[id]?.Versions[version];
    // const res = await axios.get<TGetDatasetVersionSuccess>
    // (`${axiosProxy()}/api/v1/DatasetManager/PullDataset?DatasetGuid=${id}`, 
    // {
    //   withCredentials: true,
    // });
    // return res.data.Dataset;
  }

  const fetch2 = (): TGetDatasetSuccess['Dataset'] => {
    //@ts-ignore
    return demo_data?.Datasets[id];
    // const res = await axios.get<TGetDatasetSuccess>
    // (`${axiosProxy()}/api/v1/DatasetManager/PullDataset?DatasetGuid=${id}`, 
    // {
    //   withCredentials: true,
    // });
    // return res.data.Dataset;
  }

  const { data, isLoading, status, error } =
    useQuery<TGetDatasetVersionSuccess['Dataset'], AxiosError>(['dataset', id], () => fetch());

  const { data: dataset_data, isLoading: dataset_is_loading, status: datasets_status, error: dataset_error } =
    useQuery<TGetDatasetSuccess['Dataset'], AxiosError>(['dataset', id], () => fetch2());
  if (isLoading || dataset_is_loading) {
    return <><Spinner /></>
  }
  if (status === 'success' && data && datasets_status === 'success' && dataset_data) {
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
