import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TAccountManagerProps } from './AccountManager.types';
import RegisterAccount from '@components/AccountManager/RegisterAccount';
import AccountInfo from '@components/AccountManager/AccountInfo';
import AccountManagerSuccess from './AccountManager.success';
import AccountManagerFailure from './AccountManager.failure';
import { useEffect, useState } from 'react';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { CSSTransition } from 'react-transition-group';
import Modal from 'react-modal';
import { AiFillCloseCircle } from 'react-icons/ai';
import { HiArrowLeft } from 'react-icons/hi';

const AccountManager: React.FC<TAccountManagerProps> = ({
  getAllAccountManagersReset,
  getAllAccountManagersStart,
  getAllAccountManagersState,
  getAllAccountManagersData,
  userData,
}) => {
  useEffect(() => {
    getAllAccountManagersReset();
    getAllAccountManagersStart(userData?.OrganizationGuid || '');
    console.log('accounts updated')
  }, []);

  const [accountManagerID, setAccountManagerID] = useState<null | string>(null);
  const [accountsFilter, setAccountsFilter] = useState<null | string>('open');
  const [modalIsOpen, setIsOpen] = React.useState(false);

  return (
    <div className={`accountmanager ${accountManagerID ? `accountmanager--active` : ''}`}>
      <div className="getallaccounts">
        <div className="getallaccounts__listtitle">
          <div className='getallaccounts__listtitle__titlewbutton'>
            Users
            <button onClick={() => setIsOpen(true)}>Create New Account</button>
          </div>
        <div className="getallaccounts__listtitle__options">
            <button
              className={
                'getallaccounts__listtitle__options__choice' +
                (accountsFilter == 'open' ? '__current' : '')
              }
              onClick={() => setAccountsFilter('open')}
            >
              Open Accounts
            </button>
            <button
              className={
                'getallaccounts__listtitle__options__choice' +
                (accountsFilter == 'closed' ? '__current' : '')
              }
              onClick={() => setAccountsFilter('closed')}
            >
              Closed accounts
            </button>
            </div>
          </div>
        <ConditionalRender
          //@ts-ignore
          state={getAllAccountManagersState}
          success={() => (
            <CSSTransition
              in={!!accountManagerID}
              timeout={200}
              classNames="my-node"
            >
              <AccountManagerSuccess
                accountsFilter={accountsFilter || ''}
                setAccountManagerID={setAccountManagerID}
                getAllAccountManagersData={getAllAccountManagersData}
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
      <Modal isOpen={modalIsOpen} contentLabel="Register User">
            <div className="modal-container">
              <AiFillCloseCircle
                onClick={() => setIsOpen(false)}
                className="modal-close"
              />
              <RegisterAccount
                closeModal={() => setIsOpen(false)}
              />
            </div>
          </Modal>
      {!accountManagerID ? (
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
                setAccountManagerID(null);
                getAllAccountManagersStart(userData?.OrganizationGuid || '');
              }}
            />
            <div className="datasets__details__header__text">
              User Details
            </div>
          </div>
          <AccountInfo
              accountManagerID={accountManagerID || ''}
              slideToPrev={() => setAccountManagerID(null)}
              getAccountManagerData={{AccountManager: getAllAccountManagersData.OrganizationUsers[accountManagerID]}}
          />
        </div>
      )}
    </div>
  );
};

export default AccountManager;
