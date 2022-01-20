import React from 'react';
import { useState } from 'react';
import { CSSTransition } from 'react-transition-group';

import { TDatasetListItem } from './TDatasetListItem.types';


const DatasetListItem: React.FC<TDatasetListItem> = ({
  onClick,
  index,
  DatasetName,
  Keywords,
  PublishDate,
  OrganizationName,
}) => {
  return (
    <div className={'datasetlist__item' + (index % 2 == 0 ? ' darkbg' : '')}>
      <div className="datasetlist__container">
        <div className="datasetlist__item__base" onClick={onClick}>
          <div className="datasetlist__item__base__title">{DatasetName}</div>
          <div className="datasetlist__item__base__stage">
            {new Date(PublishDate * 1000).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </div>
          <div className="datasetlist__item__base__keywords">
            {Keywords}
          </div>
          <div className="datasetlist__item__base__organizationname">
            {OrganizationName}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DatasetListItem;
