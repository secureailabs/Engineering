import { IUserData } from '@APIs/user/user.typeDefs';
import { IDefaults } from '@APIs/typedefs';

export type TNavBarProps = {
  userData: IUserData;
  signOutStart(): void;
};
