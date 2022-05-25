import {
  TGetUnifiedRegistryStart,
  TGetUnifiedRegistrySuccess,
} from '@APIs/unifiedRegistry/unifiedRegistry.types';
import { IDefaults } from '@APIs/typedefs';
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

