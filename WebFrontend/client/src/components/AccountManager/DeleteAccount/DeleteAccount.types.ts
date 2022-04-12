import { IDefaults } from '@redux/typedefs';
import {
  TDeleteAccountManagerSuccess,
  TDeleteAccountManagerStart,
} from '@redux/accountManager/accountManager.typeDefs';

export type TDeleteAccountProps = {
  deleteAccountManagerStart(
    data: TDeleteAccountManagerStart
  ): void;
  deleteAccountManagerReset(): void;
  deleteAccountManagerState: IDefaults['state'];

  closeModal(): void;
  getAllAccountManagersStart(data: {OrganizationGuid: string}): void;
  getAllAccountManagersReset(): void;
  OrganizationGuid: string;
  UserGuid: string;
};

export type TDeleteAccountFormProps = {
  deleteAccountManagerStart(
    data: TDeleteAccountManagerStart
  ): void;
  deleteAccountManagerReset(): void;

  UserGuid: string;
};

export type TDeleteAccountSuccessProps = {
  closeModal(): void;
}
