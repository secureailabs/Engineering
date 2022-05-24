import { TGetDigitalContractSuccess, TGetDigitalContractStart } from '@app/redux/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@app/redux/user/user.typeDefs';
import { IDefaults } from '@app/redux/typedefs';
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