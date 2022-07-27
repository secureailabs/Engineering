import { useQuery } from 'react-query';
import { AxiosError } from 'axios';

import { TGetAllDocumentationSuccess } from '@APIs/documentation/documentation.typeDefs';
import { getAllDocumentationAPIDemo } from '@APIs/documentation/documentation.apis';

import Documentation from './Documentation.component';

const DocumentationContainer: React.FC = () => {
    const { data, isLoading, status, error, refetch} =
    // @ts-ignore
    useQuery<TGetAllDocumentationSuccess['documentation'], AxiosError>(['documentation'], getAllDocumentationAPIDemo, { refetchOnMount: 'always' });
    //@ts-ignore
    return Documentation({ status: status, getAllDocumentationData: data, error: error })
}

export default DocumentationContainer;
