import {
  TGetDatasetSuccess,
  TGetDatasetStart,
} from '@app/redux/dataset/dataset.typeDefs';
import { IUserData } from '@app/redux/user/user.typeDefs';
import { IDefaults } from '@app/redux/typedefs';
import { AxiosError } from 'axios';
import React from 'react';


export type TRequestDataAccessFormProps = {
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>,
  DataOwnerOrganization: string,
  DatasetGuid: string,
  UrlOnSuccess?: string
};

export type TRequestDataAccessFormSuccessProps = {
  UrlOnSuccess: string
};

export type TRequestDataAccessFormFailureProps = {
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>,
  error: AxiosError<any> | null
}