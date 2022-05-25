import {
  TGetDatasetSuccess,
  TGetDatasetStart,
} from '@APIs/dataset/dataset.typeDefs';
import { IUserData } from '@APIs/user/user.typeDefs';
import { IDefaults } from '@APIs/typedefs';
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