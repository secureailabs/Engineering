import {
  TGetUnifiedRegistryStart,
  TGetUnifiedRegistrySuccess,
} from '@app/redux/unifiedRegistry/unifiedRegistry.types';
import { IDefaults } from '@app/redux/typedefs';
import { AxiosError } from 'axios';

export type TUnifiedRegistryProps = {
  getUnifiedRegistryStart(data: TGetUnifiedRegistryStart['ID']): void;
  getUnifiedRegistryReset(): void;
  getUnifiedRegistryState: IDefaults['state'];
  getUnifiedRegistryData: TGetUnifiedRegistrySuccess;
};

export type TUnifiedRegistrySuccessProps = {
  getUnifiedRegistryData: TGetUnifiedRegistrySuccess['UnifiedRegistry'];
};


export type TUnifiedRegistryError = {
  error: AxiosError<any> | null;
};

