import {
  TPutOrganizationStart,
  TGetOrganizationSuccess,
} from '@app/redux/organization/organization.typeDefs';
import { IDefaults } from '@app/redux/typedefs';
import { IUserData } from '@app/redux/user/user.typeDefs';

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
