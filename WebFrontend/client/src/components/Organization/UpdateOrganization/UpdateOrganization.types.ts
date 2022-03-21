import {
  TPutOrganizationStart,
  TGetOrganizationSuccess,
} from '@redux/organization/organization.typeDefs';
import { IDefaults } from '@redux/typedefs';
import { IUserData } from '@redux/user/user.typeDefs';

export type TUpdateOrganizationProps = {
  putOrganizationStart(data: TPutOrganizationStart): void;
  putOrganizationReset(): void;
  getOrganizationStart(): void;
  putOrganizationState: IDefaults['state'];
  organizationData: TGetOrganizationSuccess;
  userData: IUserData;
};

export type TUpdateOrganizationFormProps = {
  putOrganizationStart(data: TPutOrganizationStart): void;
  putOrganizationReset(): void;
  organizationData: TGetOrganizationSuccess;
  userData: IUserData;
};

export type TUpdateOrganizationSuccessProps = {
  putOrganizationStart(data: TPutOrganizationStart): void;
  putOrganizationState: IDefaults['state'];
  updateSuccess: (data: boolean) => void;
  getOrganizationStart(): void;
};
