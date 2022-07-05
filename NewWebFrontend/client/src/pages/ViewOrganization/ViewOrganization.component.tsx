import { TViewOrganizationProps } from './ViewOrganization.types';

import ViewOrganizationSuccess from './ViewOrganization.success';
import ViewOrganizationFailure from './ViewOrganization.failure';

import axios, { AxiosError } from 'axios';

import { useParams } from 'react-router';

import Spinner from '@components/Spinner/SpinnerOnly.component';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import demo_data from '@APIs/organization/organization.data';
import { TGetOrganizationSuccess } from '@APIs/organization/organization.typeDefs';

import { axiosProxy } from '@APIs/utils';
import { useQuery } from 'react-query';

const mode = localStorage.getItem("mode")

const ViewOrganization: React.FC<TViewOrganizationProps> = () => {
  const { id } = useParams();


  const fetch = (): TGetOrganizationSuccess => {
    //@ts-nocheck
    // if(mode == "demo"){
    console.log(demo_data)
    // @ts-ignore
    return demo_data.organizations[parseInt(id?.slice(-1) - 1 || '0')]
    // }
  //   const res = axios.get<TGetViewOrganizationSuccess>
  //   (`${axiosProxy()}/api/v1/DatasetManager/PullDataset?DatasetGuid=${id}`, 
  //   {
  //     withCredentials: true,
  //   });
  //   return res.data.ViewOrganization;
  }

  const { data, isLoading, status, error } =
    useQuery<TGetOrganizationSuccess, AxiosError>(['organization'], () => fetch());


  if (isLoading) {
    return <><Spinner /></>
  }
  if (status === 'success' && data) {
    return (
      <StandardContent title="Organization">
        <ViewOrganizationSuccess
          getOrganizationData={data}
        />
      </StandardContent>
    )
  }
  return <ViewOrganizationFailure error={error} />

};
export default ViewOrganization;
