import { useQuery } from 'react-query';
import { AxiosError } from 'axios';

import { TGetAllDocumentationsSuccess } from '@APIs/documentation/documentation.typeDefs';
import { getAllDocumentationsAPIDemo } from '@APIs/documentation/documentation.apis';

import Documentations from './Documentations.component';

const DocumentationsContainer: React.FC = () => {
    const { data, isLoading, status, error, refetch} =
    // @ts-ignore
    useQuery<TGetAllDocumentationsSuccess['documentations'], AxiosError>(['documentations'], getAllDocumentationsAPIDemo, { refetchOnMount: 'always' });
    //@ts-ignore
    return Documentations({ status: status, getAllDocumentationsData: data, error: error })
}

export default DocumentationsContainer;
