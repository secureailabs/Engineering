import { IDefaults } from '@redux/typedefs';
import {
  TPutAccountManagerSuccess,
  TPutAccountManagerStart,
} from '@redux/accountManager/accountManager.typeDefs';

export type TReopenAccountProps = {
  putAccountManagerStart(
    data: TPutAccountManagerStart
  ): void;
  putAccountManagerReset(): void;
  putAccountManagerState: IDefaults['state'];

  getAllAccountManagersStart(data: { OrganizationGuid: string }): void;
  getAllAccountManagersReset(): void;
  OrganizationGuid: string;

  UserGuid: string;
  closeModal(): void;
};

export type TReopenAccountFormProps = {
  putAccountManagerStart(
    data: TPutAccountManagerStart
  ): void;
  putAccountManagerReset(): void;

  UserGuid: string;
};

export type TReopenAccountSuccessProps = {
  closeModal(): void;
}
