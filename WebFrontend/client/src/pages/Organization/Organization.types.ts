import { TGetOrganizationSuccess } from '@redux/organization/organization.typeDefs';

import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TOrganizationProps = {
  getOrganizationStart(): void;
  getOrganizationReset(): void;
  getOrganizationState: IDefaults['state'];
  getOrganizationData: TGetOrganizationSuccess;
  userData: IUserData;
};

export type TOrganizationSuccessProps = {
  organizationData: TGetOrganizationSuccess;
};
