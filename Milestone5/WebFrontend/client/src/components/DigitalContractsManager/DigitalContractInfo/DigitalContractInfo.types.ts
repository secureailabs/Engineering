import { IDefaults } from '@redux/typedefs';
import { TGetDigitalContractSuccess } from '@redux/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';

export type TDigitalContractInfoSuccess = {
  getDigitalContractData: TGetDigitalContractSuccess | null;
  userData: IUserData;
  digitalContractID: string;
};

export type TDigitalContractInfo = {
  getDigitalContractStart(key: string): void;
  getDigitalContractReset(): void;
  getDigitalContractState: IDefaults['state'];
  getDigitalContractData: TGetDigitalContractSuccess | null;
  digitalContractID: string;
  userData: IUserData;
};
