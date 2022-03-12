import {
  TGetUnifiedRegistryStart,
  TGetUnifiedRegistrySuccess,
} from '@redux/unifiedRegistry/unifiedRegistry.types';
import { IDefaults } from '@redux/typedefs';

export type TUnifiedRegistryProps = {
  getUnifiedRegistryStart(data: TGetUnifiedRegistryStart['ID']): void;
  getUnifiedRegistryReset(): void;
  getUnifiedRegistryState: IDefaults['state'];
  getUnifiedRegistryData: TGetUnifiedRegistrySuccess;
};

export type TUnifiedRegistrySuccessProps = {
  getUnifiedRegistryData: TGetUnifiedRegistrySuccess;
};
