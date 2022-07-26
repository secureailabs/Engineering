import useBreadcrumbs from 'use-react-router-breadcrumbs';
import { QueryClient, useQueryClient } from 'react-query';
import React, { useState } from 'react';

import Breadcrumbs from '@secureailabs/web-ui/components/Breadcrumbs';


const updateBreadcrumb = (queryKey: string, nameKey: string, setBreadcrumb: React.Dispatch<React.SetStateAction<string>>, queryClient: QueryClient, self: () => {}) => {
    const queryState = queryClient.getQueryState(queryKey)

    if (queryState) {
        // @ts-ignore
        setBreadcrumb(queryState.data[nameKey])
    }

    if (!queryState || new Date().getTime() - queryState.dataUpdatedAt >= 100) {
        setTimeout(self, 15)
    }
}

const BreadcrumbRoutes: React.FC = () => {
    const [datasetName, setDatasetName] = useState('')
    const [registryName, setRegistryName] = useState('')
    const [organizationName, setOrganizationName] = useState('')
    const [downloadName, setDownloadName] = useState('')


    const queryClient = useQueryClient()


    const updateDatasetName      = () => updateBreadcrumb('dataset', 'name', setDatasetName, queryClient, updateDatasetName)
    const updateRegistryName     = () => updateBreadcrumb('unified', 'Name', setRegistryName, queryClient, updateRegistryName)
    const updateOrganizationName = () => updateBreadcrumb('organization', 'name', setOrganizationName, queryClient, updateOrganizationName)
    const updateDownloadName = () => updateBreadcrumb('download', 'primaryText', setDownloadName, queryClient, updateDownloadName)



    const routes = [
        {
            path: '/', breadcrumb: null
        },
        {
            path: '/dashboard', breadcrumb: 'Home'
        },
        {
            path: '/dashboard/datasets/:id', breadcrumb: () => {
                updateDatasetName();
            return datasetName}
        },
        {
            path: '/dashboard/computational-resources', breadcrumb: 'Computational Resources'
        },
        {
            path: '/dashboard/downloads/:id', breadcrumb: () => {
                updateDownloadName();
            return downloadName}
        },
        {
            path: '/dashboard/registries', breadcrumb: 'Unified Registries'
        },
        {
            path: '/dashboard/registries/:id', breadcrumb: () => {
                updateRegistryName();
                return registryName
            }
        },
        {
            path: '/dashboard/organizations/:id', breadcrumb: () => {
                updateOrganizationName();
                return organizationName
            }
        },
        {
            path: '/dashboard/my-organization', breadcrumb: 'My Organization'
        }
    ]
    // @ts-ignore
    return <Breadcrumbs breadcrumbsData={useBreadcrumbs(routes)} />
}


export default BreadcrumbRoutes