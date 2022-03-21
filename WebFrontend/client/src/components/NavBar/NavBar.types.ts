import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TNavBarProps = {
  userData: IUserData;
  signOutStart(): void;
};
