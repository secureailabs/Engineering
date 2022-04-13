import { TGetDigitalContractSuccess, TGetDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';
import { AxiosError } from 'axios';

export type TDigitalContractProps = {
  userData: IUserData;
};

export type TDigitalContractSuccessProps = {
  getDigitalContractData: TGetDigitalContractSuccess['DigitalContract'];
  userData: IUserData
};

export type TDigitalContractError = {
  error: AxiosError<any> | null
}