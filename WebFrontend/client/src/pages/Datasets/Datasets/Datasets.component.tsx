import React from 'react';

import axios, {AxiosError} from 'axios';

import { axiosProxy } from '@app/redux/utils';
import { useQuery } from 'react-query';

import { TDatasetsProps } from './Datasets.types';

import DatasetsSuccess from './Datasets.success';
import DatasetsFailure from './Datasets.failure';
import Spinner from '@components/Spinner/SpinnerOnly.component';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import { TGetAllDatasetsSuccess } from '@app/redux/dataset/dataset.typeDefs';

import { demo_data } from "@app/redux/dataset/dataset.data";

const fetch = async (): Promise<TGetAllDatasetsSuccess['Datasets']> => {
  // return demo_data.Datasets;
  const res = await axios.get<TGetAllDatasetsSuccess>
  (`${axiosProxy()}/api/v1/DatasetManager/ListDatasets`, 
  {
    withCredentials: true,
  });
  return res.data.Datasets;
}


const Datasets: React.FC<TDatasetsProps> = () => {

  
  const { data, isLoading, status, error } = 
    useQuery<TGetAllDatasetsSuccess['Datasets'], AxiosError>(['datasets'], fetch);
  if(isLoading){
      return <><Spinner/></>
  }
  if(status === 'success' && data){
      return (
          <StandardContent title="Datasets">
            <DatasetsSuccess
              getAllDatasetsData={data}
          />
          </StandardContent>
      )
  }
  return <DatasetsFailure error={error} />


};

export default Datasets;
