import { useQuery, useQueryClient } from 'react-query';
import { AxiosError } from 'axios';
import { useParams } from 'react-router';

import { TGetDatasetSuccess } from '@APIs/dataset/dataset.typeDefs';
import { getDatasetAPI } from '@APIs/dataset/dataset.apis';

import { getDatasetAPIdemo } from '@APIs/dataset/dataset.demo-apis';

import Dataset from './Dataset.component';

const DatasetContainer: React.FC = () => {
  const apiFunction = localStorage.getItem('mode') == 'demo' ? getDatasetAPIdemo : getDatasetAPI;

  const { id } = useParams() || ''

  const queryClient = useQueryClient()

  const { data, isLoading, status, error, refetch } =
    // @ts-ignore
    useQuery<TGetDatasetSuccess, AxiosError>([`dataset-${id}`], () => apiFunction({ dataset_id: id }), { refetchOnMount: 'always' });
  //@ts-ignore
  return Dataset({ status: status, getDatasetData: data, refetch: refetch, error: error, userData: queryClient.getQueryData('userData') })
}

export default DatasetContainer;
