import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TAzureTemplatesManagerProps } from './SelectAzureTemplate.types';
import AccountManagerSuccess from './SelectAzureTemplate.success';
import AccountManagerFailure from './SelectAzureTemplate.failure';
import { useEffect, useState } from 'react';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { CSSTransition } from 'react-transition-group';
import Form from '@components/Form';

const AzureTemplatesManager: React.FC<TAzureTemplatesManagerProps> = ({
  listAzureTemplatesStart,
  listAzureTemplatesReset,
  listAzureTemplatesData,
  listAzureTemplatesState,
  onClick,
}) => {
  useEffect(() => {
    listAzureTemplatesReset();
    listAzureTemplatesStart();
    console.log('azure templates updated');
  }, []);

  const [azureTemplateID, setAzureTemplateID] = useState<null | string>(null);
  const [modalIsOpen, setIsOpen] = React.useState(false);
  console.log('rendering here');
  return (
    <ConditionalRender
      //@ts-ignore
      state={listAzureTemplatesState}
      success={() => (
        <CSSTransition
          in={!!azureTemplateID}
          timeout={200}
          classNames="my-node"
        >
        <Form actualForm={false}>
        <>
          <div className="dcforminfo">
            <div className="dcforminfo__title">Select Azure Template</div>
          </div>
          <AccountManagerSuccess
              setAzureTemplateID={setAzureTemplateID}
              listAzureTemplatesData={listAzureTemplatesData}
              onClick={onClick}
            />
        </>
      </Form>
        </CSSTransition>
      )}
      failure={AccountManagerFailure}
      Loading={
        <>
          <Spinner />
        </>
      }
    >
      <></>
    </ConditionalRender>
  );
};

export default AzureTemplatesManager;
