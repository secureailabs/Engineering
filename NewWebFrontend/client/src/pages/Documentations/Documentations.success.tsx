import React from 'react';
import { TDocumentationsSuccessProps } from './Documentations.types';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import Resource from '@secureailabs/web-ui/components/Resource'
import Text from '@secureailabs/web-ui/components/Text'

const Documentationuccess: React.FC<TDocumentationsSuccessProps> = ({
    getAllDocumentationsData,
}) => {
  // Get all the documentations using the documentation information api and create a list of Resource components
  const documentation_list = getAllDocumentationsData.map((documentation) => {
    return (
      <>
        <Resource
          key={documentation.id}
          Icon={documentation.icon}
          primaryText={documentation.primaryText}
          secondaryText={documentation.secondaryText}
        />
      </>
    );
  });

  return (
    <StandardContent title="Documentation">
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
            {documentation_list}
          </div>
          </>
    </StandardContent>
  );
};

export default Documentationuccess;
