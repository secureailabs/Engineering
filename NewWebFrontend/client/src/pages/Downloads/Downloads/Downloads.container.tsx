import { useQuery } from 'react-query';
import { AxiosError } from 'axios';

import { TGetAllDownloadsSuccess } from '@APIs/download/download.typeDefs';
import { getAllDownloadsAPI } from '@APIs/download/download.apis';

import Downloads from './Downloads.component';

const DownloadsContainer: React.FC = () => {
    const { data, isLoading, status, error, refetch} =
    // @ts-ignore
    useQuery<TGetAllDownloadsSuccess['downloads'], AxiosError>(['downloads'], getAllDownloadsAPI, { refetchOnMount: 'always' });
    //@ts-ignore
    return Downloads({ status: status, getAllDownloadsData: data, error: error })
}

export default DownloadsContainer;
