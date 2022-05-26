import { TGetAllUnifiedRegistriesSuccess } from '@APIs/unifiedRegistry/unifiedRegistry.types';
import { IUserData } from '@APIs/user/user.typeDefs';
import { IDefaults } from '@APIs/typedefs';
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
