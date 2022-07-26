import React from 'react';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import Card from '@secureailabs/web-ui/components/Card';

import { TDownloadSuccessProps } from './Download.types';
import { FiExternalLink } from "react-icons/fi";

const DownloadSuccess: React.FC<TDownloadSuccessProps> = ({ getDownloadData }) => {

  const FieldValue: React.FC<{field: string; value: string; fullRow: boolean; url?: string}> = ({field, value, fullRow, url}) => {
    const className = fullRow ? "downloads-card__description" : "downloads-card__key-value"
    return (
      <div className={className}>
        <p className="downloads-card__key">{field}</p>
        {
          url
          ? <a href={getDownloadData.documentationUrl} className="downloads-card__url">Lorem ipsum <FiExternalLink/></a>
          : <p className="downloads-card__value">{value}</p>
        }
      </div>
    )
  };

  return (
    <StandardContent title=''>
      <Card primaryText=''>
        <div className="downloads-card">
          <div className="downloads-card__title">
            <getDownloadData.icon className="downloads-card__icon"/>
            <p>
              {getDownloadData.primaryText}
            </p>
          </div>
          <FieldValue field="Version" value={getDownloadData.version} fullRow={false}/>
          <FieldValue field="Release Date" value={getDownloadData.publish_date} fullRow={false}/>
          <FieldValue field="Description" value={getDownloadData.secondaryText} fullRow={true}/>
          <FieldValue field="Systems Requirement" value={getDownloadData.systemRequirements} fullRow={false}/>
          <FieldValue field="File Size" value={getDownloadData.fileSize} fullRow={false}/>
          <FieldValue field="Documentation Link" value="Lorem ipsum" fullRow={false} url={getDownloadData.documentationUrl}/>
        </div>
      </Card>
    </StandardContent>
  );
};

export default DownloadSuccess;
