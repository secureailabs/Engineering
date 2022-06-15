import useBreadcrumbs from 'use-react-router-breadcrumbs';
import { useQueryClient } from 'react-query';
import React, { useEffect, useState } from 'react';
import { useLocation } from "react-router-dom";

import Breadcrumbs from '@secureailabs/web-ui/components/Breadcrumbs';


const BreadcrumbRoutes: React.FC = () => {
    const location = useLocation()

    const [datasetName, setDatasetName] = useState('')
    
    const queryClient = useQueryClient()


    const updateDatasetName = () => {
        const datasetQueryState = queryClient.getQueryState('dataset')

        if (datasetQueryState && new Date().getTime() - datasetQueryState.dataUpdatedAt <= 100) {
            // @ts-ignore
            setDatasetName(datasetQueryState.data.name)
        }
        else {
            setTimeout(updateDatasetName, 50)
        }
    }


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
            path: '/dashboard/virtual-machines', breadcrumb: 'Virtual Machines'
        },
        {
            path: '/dashboard/registries', breadcrumb: 'Unified Registries'
        },
        {
            path: '/dashboard/registries/:id', breadcrumb: 'KCA Research Consortium'
        },
        {
            path: '/dashboard/my-organization', breadcrumb: 'My Organization'
        }
    ]
    // @ts-ignore
    return <Breadcrumbs breadcrumbsData={useBreadcrumbs(routes)} />
}


export default BreadcrumbRoutes