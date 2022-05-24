import { TGetAllDigitalContractsSuccess } from '@app/redux/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@app/redux/user/user.typeDefs';
import { IDefaults } from '@app/redux/typedefs';
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