import { TPostDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TRegisterDigitalContractProps = {
  postDigitalContractStart(data: TPostDigitalContractStart): void;
  postDigitalContractReset(): void;
  postDigitalContractState: IDefaults['state'];
  userData: IUserData;
  DatasetGuid: string;
  JurisdictionalLimitations: string;
  DatasetName: string;
  DataOwnerOrganization: string;
  closeModal(): void;
};

export type TRegisterDigitalContractFormProps = {
  postDigitalContractStart(data: TPostDigitalContractStart): void;
  postDigitalContractReset(): void;
  userData: IUserData;
  DatasetGuid: string;
  JurisdictionalLimitations: string;
  DatasetName: string;
  DataOwnerOrganization: string;
};

export type TRegisterDigitalContractSuccess = {
  closeModal(): void;
};
