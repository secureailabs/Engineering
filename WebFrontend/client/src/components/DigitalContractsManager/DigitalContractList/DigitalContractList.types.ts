import { TGetAllDigitalContractsSuccess } from '@redux/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
export type TDigitalContractList = {
  setDigitalContractID(digitalContract: string): void;
  data: Array<TGetAllDigitalContractsSuccess['DigitalContracts']['']>;
  stage: TGetAllDigitalContractsSuccess['DigitalContracts']['']['ContractStage']; 
};
