import { TGetDigitalContractSuccess, TGetDigitalContractStart } from '@APIs/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@APIs/user/user.typeDefs';
import { IDefaults } from '@APIs/typedefs';
import { AxiosError } from 'axios';

export type TDigitalContractProps = {
  userData: IUserData;
};

export type TDigitalContractSuccessProps = {
  getDigitalContractData: TGetDigitalContractSuccess;
  userData: IUserData
};

export type TDigitalContractError = {
  error: AxiosError<any> | null
}