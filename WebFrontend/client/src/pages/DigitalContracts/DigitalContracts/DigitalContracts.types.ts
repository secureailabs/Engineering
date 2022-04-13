import { TGetAllDigitalContractsSuccess } from '@redux/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';
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