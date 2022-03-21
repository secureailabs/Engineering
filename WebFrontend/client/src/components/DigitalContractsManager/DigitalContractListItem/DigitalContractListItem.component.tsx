import React from 'react';

import { TDigitalContractListItem } from './TDigitalContractListItem.types';
import getPartnerOrg from '@utils/getPartnerOrg';

const DigitalContractListItem: React.FC<TDigitalContractListItem> = ({
  onClick,
  index,
  title,
  datasetName,
  lastActivity,
  dataOwnerOrganization,
  DOOName,
  researcherOrganization,
  ROName,
  userData,
}) => {
  return (
    <div
      className={
        'digitalcontractlist__item' + (index % 2 == 0 ? ' darkbg' : '')
      }
    >
      <div className="digitalcontractlist__container" onClick={onClick}>
        <div className="digitalcontractlist__item__base">
          <div className="digitalcontractlist__item__base__title">{title}</div>
          <div className="digitalcontractlist__item__base__datasetguid">
            {datasetName}
          </div>
          <div className="digitalcontractlist__item__base__partner">{getPartnerOrg(userData, dataOwnerOrganization, DOOName, ROName)}</div>
          <div className="digitalcontractlist__item__base__contractDuration">
          {new Date(lastActivity * 1000).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DigitalContractListItem;
