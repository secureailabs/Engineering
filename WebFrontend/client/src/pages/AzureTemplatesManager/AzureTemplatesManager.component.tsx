import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TAzureTemplatesManagerProps } from './AzureTemplatesManager.types';
import AccountManagerSuccess from './AzureTemplatesManager.success';
import AccountManagerFailure from './AzureTemplatesManager.failure';
import AzureTemplateInfo from '@components/AzureTemplatesManager/AzureTemplateInfo';
import RegisterAzureTemplate from '@components/AzureTemplatesManager/RegisterAzureTemplate';
import { useEffect, useState } from 'react';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { CSSTransition } from 'react-transition-group';
import Modal from 'react-modal';
import { AiFillCloseCircle } from 'react-icons/ai';
import { HiArrowLeft } from 'react-icons/hi';

const AzureTemplatesManager: React.FC<TAzureTemplatesManagerProps> = ({
  listAzureTemplatesStart,
  listAzureTemplatesReset,
  listAzureTemplatesData,
  listAzureTemplatesState
}) => {
  useEffect(() => {
    listAzureTemplatesReset();
    listAzureTemplatesStart();
    console.log('azure templates updated')
  }, []);

  const [azureTemplateID, setAzureTemplateID] = useState<null | string>(null);
  const [modalIsOpen, setIsOpen] = React.useState(false);

  return (
    <div className={`accountmanager ${azureTemplateID ? `accountmanager--active` : ''}`}>
      <div className="getallaccounts">
        <div className="getallaccounts__listtitle">
          <div className='getallaccounts__listtitle__titlewbutton'>
            Azure Templates Manager
            <button onClick={() => setIsOpen(true)}>Create New Azure Template</button>
          </div>
        </div>
        <ConditionalRender
          //@ts-ignore
          state={listAzureTemplatesState}
          success={() => (
            <CSSTransition
              in={!!azureTemplateID}
              timeout={200}
              classNames="my-node"
            >
              <AccountManagerSuccess
                setAzureTemplateID={setAzureTemplateID}
                listAzureTemplatesData={listAzureTemplatesData}
              />
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
      </div>
      <Modal isOpen={modalIsOpen} contentLabel="Register Azure Template">
            <div className="modal-container">
              <AiFillCloseCircle
                onClick={() => {
                  setIsOpen(false)
                  listAzureTemplatesReset();
                  listAzureTemplatesStart();
                }}
                className="modal-close"
              />
              <RegisterAzureTemplate
                closeModal={() => setIsOpen(false)}
              />
            </div>
          </Modal>
      {!azureTemplateID ? (
        <></>
      ) : (
        <div className="datasets__details">
          <div className="datasets__details__header">
            <HiArrowLeft
              style={{
                // padding: '2rem',
                width: '3rem',
                height: '3rem',
                cursor: 'pointer',
              }}
              onClick={() => {
                setAzureTemplateID(null);
                listAzureTemplatesStart();
              }}
            />
            <div className="datasets__details__header__text">
              Azure Template Settings{azureTemplateID && <> - {azureTemplateID}</>}
            </div>
          </div>
          <AzureTemplateInfo
              azureTemplateID={azureTemplateID || ''}
              slideToPrev={() => setAzureTemplateID(null)}
          />
        </div>
      )}
    </div>
  );
};

export default AzureTemplatesManager;
