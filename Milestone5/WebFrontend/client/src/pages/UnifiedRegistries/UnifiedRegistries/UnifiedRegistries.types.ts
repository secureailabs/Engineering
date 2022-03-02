import { TGetAllUnifiedRegistriesSuccess } from '@redux/unifiedRegistry/unifiedRegistry.types';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TUnifiedRegistriesProps = {
  getAllUnifiedRegistriesStart(): void;
  getAllUnifiedRegistriesReset(): void;
  getAllUnifiedRegistriesState: IDefaults['state'];
  getAllUnifiedRegistriesData: TGetAllUnifiedRegistriesSuccess;
};

export type TUnifiedRegistriesSuccessProps = {
  getAllUnifiedRegistriesData: TGetAllUnifiedRegistriesSuccess;
};
