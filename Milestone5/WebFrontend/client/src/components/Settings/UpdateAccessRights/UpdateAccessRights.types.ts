import { TPutUpdateAccessRightsStart } from '@redux/accountManager/accountManager.typeDefs';
import { IDefaults } from '@redux/typedefs';
import { IUserData } from '@redux/user/user.typeDefs';

export type TUpdateAccessRightsProps = {
  putUpdateAccessRightsStart(data: TPutUpdateAccessRightsStart): void;
  putUpdateAccessRightsReset(): void;
  putUpdateAccessRightsState: IDefaults['state'];
  UserGuid: string;
  userData: IUserData;
};

export type TUpdateAccessRightsFormProps = {
  putUpdateAccessRightsStart(data: TPutUpdateAccessRightsStart): void;
  putUpdateAccessRightsReset(): void;
  UserGuid: string;
  userData: IUserData;
};
