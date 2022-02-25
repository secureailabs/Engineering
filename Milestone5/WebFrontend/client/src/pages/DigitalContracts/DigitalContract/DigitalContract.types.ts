import { TGetDigitalContractSuccess } from '@redux/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TDigitalContractProps = {
  getDigitalContractStart(): void;
  getDigitalContractReset(): void;
  getDigitalContractState: IDefaults['state'];
  getDigitalContractData: TGetDigitalContractSuccess;
  userData: IUserData;
};

export type TDigitalContractSuccessProps = {
  getDigitalContractData: TGetDigitalContractSuccess;
};
