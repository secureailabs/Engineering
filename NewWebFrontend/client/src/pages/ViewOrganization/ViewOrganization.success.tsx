import React from 'react';
import Card from '@secureailabs/web-ui/components/Card';

import Margin from '@secureailabs/web-ui/components/Margin';

import type { TViewOrganizationSuccessProps } from './ViewOrganization.types';

const ViewOrganizationSuccess: React.FC<TViewOrganizationSuccessProps> = ({
  getOrganizationData,
}) => {
  return (
    <>
      <Card primaryText="">
        <div className="unified-registry-card">
          <div className="unified-registry-card__header">
            <img src={getOrganizationData.avatar} />
          </div>
          <p className="unified-registry-card__title">Organization Name</p>
          <Margin size={5} />
          <p className="unified-registry-card__description">
            {getOrganizationData.name}
          </p>
          <Margin size={5} />
          <p className="unified-registry-card__title">Organization Name</p>
          <Margin size={5} />
          <p className="unified-registry-card__description">
            {getOrganizationData.description}
          </p>
        </div>
      </Card>
    </>
  );
};

export default ViewOrganizationSuccess;
