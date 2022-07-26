import React from 'react';
import { useNavigate } from 'react-router';
import { TDownloadsSuccessProps } from './Downloads.types';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import Resource from '@secureailabs/web-ui/components/Resource'
import Text from '@secureailabs/web-ui/components/Text'

const Downloadsuccess: React.FC<TDownloadsSuccessProps> = ({
    getAllDownloadsData,
}) => {
  const navigate = useNavigate();
  // Get all the downloads using the download information api and create a list of Resource component
  const download_list = getAllDownloadsData.map((download) => {
    return (
      <>
        <Resource
          key={download.id}
          Icon={download.icon}
          primaryText={download.primaryText}
          secondaryText={download.secondaryText}
          buttonText={download.buttonText}
          buttonOnClick={() => location.href=download.buttonUrl}
          titleOnClick={() => navigate(`/dashboard/downloads/${download.id}`)}
        />
      </>
    );
  });

  return (
    <StandardContent  title="Downloads">
          <>
            <Text
              fontStyle="normal"
              lineHeight={5}
              textAlign="left"
              fontWeight={600}
              fontSize="16px"
            >
              For Data Owners:
            </Text>
          <div className='downloads-list'>
            {download_list}
          </div>
          </>
    </StandardContent>
  );
};

export default Downloadsuccess;
