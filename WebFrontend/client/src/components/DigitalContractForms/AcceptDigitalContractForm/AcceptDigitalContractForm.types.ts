import { AxiosError } from 'axios';
import React from 'react';


export type TAcceptDigitalContractFormProps = {
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>,
  DigitalContractGuid: string,
  UrlOnSuccess?: string
};

export type TAcceptDigitalContractFormSuccessProps = {
  UrlOnSuccess: string
};

export type TAcceptDigitalContractFormFailureProps = {
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>,
  error: AxiosError<any> | null
}