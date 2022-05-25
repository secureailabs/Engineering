import { useQuery } from 'react-query';
import { AxiosError } from 'axios';

import { TGetAllDatasetsSuccess } from '@APIs/dataset/dataset.typeDefs';
import { getAllDatasetsAPI } from '@APIs/dataset/dataset.apis';

import Datasets from './Datasets.component';

const DatasetsDashboard: React.FC = () => {
  const { data, isLoading, status, error, refetch} =
    // @ts-ignore
    useQuery<TGetAllDatasetsSuccess['datasets'], AxiosError>(['datasets'], getAllDatasetsAPI);
  //@ts-ignore
  return Datasets({ status: status, getAllDatasetsData: data, refetch: refetch, error: error})
}

export default DatasetsDashboard
