import { AxiosError } from 'axios';
import React from 'react';


export type TActivateDigitalContractFormProps = {
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>,
  DigitalContractGuid: string,
  UrlOnSuccess?: string
};

export type TActivateDigitalContractFormSuccessProps = {
  UrlOnSuccess: string
};

export type TActivateDigitalContractFormFailureProps = {
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>,
  error: AxiosError<any> | null
}