import { TGetAllDigitalContractsSuccess } from '@APIs/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@APIs/user/user.typeDefs';
import { IDefaults } from '@APIs/typedefs';
import { AxiosError } from 'axios';


export type TDigitalContractsProps = {
  getAllDigitalContractsStart(): void;
  getAllDigitalContractsReset(): void;
  getAllDigitalContractsState: IDefaults['state'];
  getAllDigitalContractsData: TGetAllDigitalContractsSuccess;
  userData: IUserData;
};

export type TDigitalContractsSuccessProps = {
  getAllDigitalContractsData: TGetAllDigitalContractsSuccess['DigitalContracts'];
  userData: IUserData;
};

export type TDigitalContractError = {
  error: AxiosError<any> | null
}