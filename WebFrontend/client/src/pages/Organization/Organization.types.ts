import { TGetOrganizationSuccess } from '@app/redux/organization/organization.typeDefs';

import { IUserData } from '@app/redux/user/user.typeDefs';
import { IDefaults } from '@app/redux/typedefs';

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
