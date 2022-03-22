import { TGetDigitalContractSuccess, TGetDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TDigitalContractProps = {
  getDigitalContractStart(data: TGetDigitalContractStart): void;
  getDigitalContractReset(): void;
  getDigitalContractState: IDefaults['state'];
  getDigitalContractData: TGetDigitalContractSuccess;
  userData: IUserData;
};

export type TDigitalContractSuccessProps = {
  getDigitalContractData: TGetDigitalContractSuccess;
};
