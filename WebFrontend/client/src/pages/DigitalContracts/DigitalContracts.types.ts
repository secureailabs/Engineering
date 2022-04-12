import { TGetAllDigitalContractsSuccess } from '@redux/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TDigitalContractsProps = {
  getAllDigitalContractsStart(): void;
  getAllDigitalContractsReset(): void;
  getAllDigitalContractsState: IDefaults['state'];
  getAllDigitalContractsData: TGetAllDigitalContractsSuccess;
  userData: IUserData;
};

export type TDigitalContractsSuccessProps = {
  getAllDigitalContractsData: TGetAllDigitalContractsSuccess;
  userData: IUserData;
  stageView: number;
  setDigitalContractID(stage: null | string): void;
};
