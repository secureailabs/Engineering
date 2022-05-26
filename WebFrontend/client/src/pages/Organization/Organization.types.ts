import { TGetOrganizationSuccess } from '@APIs/organization/organization.typeDefs';

import { IUserData } from '@APIs/user/user.typeDefs';
import { IDefaults } from '@APIs/typedefs';

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
