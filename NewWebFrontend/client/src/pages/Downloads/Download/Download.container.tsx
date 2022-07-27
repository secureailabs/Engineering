import React from 'react';
import { useQuery, useQueryClient } from 'react-query';
import { AxiosError } from 'axios';
import { useParams } from 'react-router';

import { TGetDownloadSuccess } from '@APIs/download/download.typeDefs';
import { getDownloadAPIDemo } from '@APIs/download/download.apis';

import Download from './Download.component';

const DownloadContainer: React.FC = () => {
  const { id } = useParams() || ''
  const queryClient = useQueryClient()
  const { data, isLoading, status, error, refetch } =
    // @ts-ignore
    useQuery<TGetDownloadSuccess, AxiosError>(['download'], () => getDownloadAPIDemo({ id: id }), { refetchOnMount: 'always' });

  //@ts-ignore
  return Download({ status: status, getDownloadData: data, refetch: refetch, error: error, userData: queryClient.getQueryData('userData') })
}

export default DownloadContainer;
