import { useQuery } from 'react-query';
import { AxiosError } from 'axios';

import { TGetAllDatasetsSuccess } from '@APIs/dataset/dataset.typeDefs';
import { getAllDatasetsAPI } from '@APIs/dataset/dataset.apis';

import { getAllDatasetsAPIdemo } from '@APIs/dataset/dataset.demo-apis';

import Datasets from './Datasets.component';

const DatasetsContainer: React.FC = () => {
  const apiFunction = localStorage.getItem('mode') == 'demo' ? getAllDatasetsAPIdemo : getAllDatasetsAPI;

  const { data, isLoading, status, error, refetch} =
    // @ts-ignore
    useQuery<TGetAllDatasetsSuccess['datasets'], AxiosError>(['datasets'], apiFunction, { refetchOnMount: 'always' });
  //@ts-ignore
  return Datasets({ status: status, getAllDatasetsData: data, error: error })
  
}

export default DatasetsContainer;
