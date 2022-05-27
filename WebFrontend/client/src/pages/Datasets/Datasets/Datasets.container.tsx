import { useQuery } from 'react-query';
import { AxiosError } from 'axios';

import { TGetAllDatasetsSuccess } from '@APIs/dataset/dataset.typeDefs';
import { getAllDatasetsAPI } from '@APIs/dataset/dataset.apis';

import demo_data from '@APIs/dataset/dataset.data';

import Datasets from './Datasets.component';

const DatasetsContainer: React.FC = () => {
  const { data, isLoading, status, error, refetch} =
    // @ts-ignore
    useQuery<TGetAllDatasetsSuccess['datasets'], AxiosError>(['datasets'], getAllDatasetsAPI, { refetchOnMount: 'always' });
  //@ts-ignore
  return localStorage.getItem('mode') == 'demo' ? Datasets({ status: 'success', getAllDatasetsData: demo_data, error: null }) : Datasets({ status: status, getAllDatasetsData: data, error: error })
  
}

export default DatasetsContainer;
