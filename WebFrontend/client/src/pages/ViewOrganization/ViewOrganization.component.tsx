import React from 'react';
import _ from 'lodash';
import { useParams } from 'react-router';

import { useQuery } from 'react-query';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import OrganizationData from "./Organization.data";

import Card from "@secureailabs/web-ui/components/Card";
import Text from "@secureailabs/web-ui/components/Text";

import Avatar from 'react-avatar';

const ViewOrganization: React.FC = () => {
    const {id} = useParams();
    const { data, isLoading } = useQuery(['organization', {id}], 
    () =>  _.find(OrganizationData, { OrganizationID: id })
    );
    if(isLoading){
        return <p>Loading...</p>
    }
    if(data === undefined){
        return (
            <StandardContent title="Organization">
                <Text>This organization does not exist</Text>
            </StandardContent>
        )
    }
    return (
        <StandardContent title="Organization">
            <Card primaryText={data?.OrganizationName || ""}>
                <div style={{
                    display: "grid",
                    gridTemplateColumns: "max-content 1fr",
                    columnGap: "15px"
                }}>
                {data.Logo ? <img style={{
                    width: "150px",
                    height: "150px",
                    borderRadius: "5px",
                    objectFit: "cover"

                }} src={data.Logo} /> : <Avatar name={data.OrganizationName} />}
                <Text>{data.OrganizationDescription}</Text>
                </div>
            </Card>
        </StandardContent>
    )
}

export default ViewOrganization;