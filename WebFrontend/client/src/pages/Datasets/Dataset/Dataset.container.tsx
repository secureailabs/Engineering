import { useQuery, useQueryClient } from 'react-query';
import { AxiosError } from 'axios';
import { useParams } from 'react-router';

import { TGetDatasetSuccess } from '@APIs/dataset/dataset.typeDefs';
import { getDatasetAPI } from '@APIs/dataset/dataset.apis';

import Dataset from './Dataset.component';

const DatasetContainer: React.FC = () => {
  const { id } = useParams() || ''

  const queryClient = useQueryClient()

  const { data, isLoading, status, error, refetch } =
    // @ts-ignore
    useQuery<TGetDatasetSuccess, AxiosError>(['dataset'], () => { console.log(id); return getDatasetAPI({ dataset_id: id }) }, { refetch: 'always' });
  //@ts-ignore
  return Dataset({ status: status, getDatasetData: data, refetch: refetch, error: error, userData: queryClient.getQueryData('userData') })
}

export default DatasetContainer;
