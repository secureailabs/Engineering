import { IDefaults } from '@redux/typedefs';
import {
  TGetDigitalContractStart,
  TPatchAssociateAzureStart,
} from '@redux/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';

export type TEditAzureTemplateForm = {
  patchAssociateAzureStart(data: TPatchAssociateAzureStart): void;
  digitalContractID: string;
};

export type TEditAzureTemplateSuccess = {
  patchAssociateAzureStart(data: TPatchAssociateAzureStart): void;
  digitalContractID: string;
  getDigitalContractStart(data: TGetDigitalContractStart): void;
  patchAssociateAzureState: IDefaults['state'];
  patchAssociateAzureReset(): void;
};

export type TEditAzureTemplate = {
  getDigitalContractStart(data: TGetDigitalContractStart): void;
  patchAssociateAzureStart(data: TPatchAssociateAzureStart): void;
  patchAssociateAzureReset(): void;
  patchAssociateAzureState: IDefaults['state'];
  digitalContractID: string;
  userData: IUserData;
};
