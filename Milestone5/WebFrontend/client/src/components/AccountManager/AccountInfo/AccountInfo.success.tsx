import React, { useState } from 'react';
import { TAccountInfoSuccess } from './AccountInfo.types';
import DeleteAccount from '@components/AccountManager/DeleteAccount';
import ReopenAccount from '@components/AccountManager/ReopenAccount';
import Modal from 'react-modal';
import Button from '@components/Button';
import InfoDisplay from '@components/InfoDisplay';
import {
  convertObjectToArray,
  reorganizeArray,
  changeArrayKeys,
} from '@components/InfoDisplay/InfoDisplay.utils';
import { AiFillCloseCircle } from 'react-icons/ai';
import accessRightsNumberToString from '@utils/accessRightsNumberToString';
import accountStatusNumberToString from '@utils/accountStatusNumberToString';
import { TInfoDisplay } from '@components/InfoDisplay/InfoDisplay.types';

const AccountInfo: React.FC<TAccountInfoSuccess> = ({
  getAccountManagerData,
  accountManagerID,
  userData,
  slideToPrev,
}) => {
  const [modalIsOpen, setIsOpen] = React.useState(false);
  console.log('GET ACCOUNT MANAGER DATA: ', getAccountManagerData);
  if (getAccountManagerData) {
    let newData: Record<string, any> = getAccountManagerData.AccountManager;
    let arrayData = convertObjectToArray(newData);
    arrayData = reorganizeArray(arrayData, [
      'Username',
      'Title',
      'Email',
      'PhoneNumber',
      'AccessRights',
    ]);
    arrayData = changeArrayKeys(arrayData, [
      'Name',
      'Job Title',
      'Email',
      'Phone Number',
      'Access Rights',
    ]);
    arrayData[4][1] = accessRightsNumberToString(arrayData[4][1]);

    console.log('ARRAY DATA: ', arrayData);
    const info_display: TInfoDisplay['data'] = [
      {
        section_title: 'Username',
        section_data: getAccountManagerData.AccountManager.Username,
      },
      {
        section_title: 'Title',
        section_data: getAccountManagerData.AccountManager.Title,
      },
      {
        section_title: 'Email',
        section_data: getAccountManagerData.AccountManager.Email,
      },
      {
        section_title: 'Phone Number',
        section_data: getAccountManagerData.AccountManager.PhoneNumber,
      },
      {
        section_title: 'Access Rights',
        section_data: accessRightsNumberToString(getAccountManagerData.AccountManager.AccessRights),
      },
      {
        section_title: 'Account Status',
        section_data: accountStatusNumberToString(getAccountManagerData.AccountManager.AccountStatus),
      },
    ];

    return (
      <div className="accountinfo">
        <InfoDisplay data={info_display} />
        {getAccountManagerData.AccountManager.AccountStatus <= 1 &&
          accountManagerID != userData?.UserGuid && (
            <>
              <div className="digitalcontractinfo__button">
                <Button onClick={() => setIsOpen(true)}>Close Account</Button>
              </div>
              <Modal isOpen={modalIsOpen} contentLabel="Example Modal">
                <div className="modal-container">
                  <AiFillCloseCircle
                    onClick={() => setIsOpen(false)}
                    className="modal-close"
                  />
                  <DeleteAccount
                    closeModal={() => {
                      setIsOpen(false);
                      slideToPrev();
                    }}
                    UserGuid={accountManagerID}
                    OrganizationGuid={userData?.OrganizationGuid || ''}
                  />
                </div>
              </Modal>
            </>
          )}
        {getAccountManagerData.AccountManager.AccountStatus >= 2 &&
          accountManagerID != userData?.UserGuid && (
            <>
              <div className="digitalcontractinfo__button">
                <Button onClick={() => setIsOpen(true)}>Reopen Account</Button>
              </div>
              <Modal isOpen={modalIsOpen} contentLabel="Example Modal">
                <div className="modal-container">
                  <AiFillCloseCircle
                    onClick={() => setIsOpen(false)}
                    className="modal-close"
                  />
                  <ReopenAccount
                    closeModal={() => {
                      setIsOpen(false);
                      slideToPrev();
                    }}
                    OrganizationGuid={userData?.OrganizationGuid || ''}
                    UserGuid={accountManagerID}
                  />
                </div>
              </Modal>
            </>
          )}
      </div>
    );
  }
  return <>Failed to fetch user data, please try again later.</>;
};

export default AccountInfo;
