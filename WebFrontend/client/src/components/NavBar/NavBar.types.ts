import { IUserData } from '@app/redux/user/user.typeDefs';
import { IDefaults } from '@app/redux/typedefs';

export type TNavBarProps = {
  userData: IUserData;
  signOutStart(): void;
};
