import { TGetAllUnifiedRegistriesSuccess } from '@app/redux/unifiedRegistry/unifiedRegistry.types';
import { IUserData } from '@app/redux/user/user.typeDefs';
import { IDefaults } from '@app/redux/typedefs';
import { AxiosError } from 'axios';

export type TUnifiedRegistriesProps = {
  getAllUnifiedRegistriesStart(): void;
  getAllUnifiedRegistriesReset(): void;
  getAllUnifiedRegistriesState: IDefaults['state'];
  getAllUnifiedRegistriesData: TGetAllUnifiedRegistriesSuccess;
};

export type TUnifiedRegistriesSuccessProps = {
  getAllUnifiedRegistriesData: TGetAllUnifiedRegistriesSuccess;
};

export type TUnifiedRegistriesError = {
  error: AxiosError<any> | null;
};
