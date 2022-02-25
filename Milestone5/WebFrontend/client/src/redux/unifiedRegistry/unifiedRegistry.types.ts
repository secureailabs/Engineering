import { TDatasetSuccessProps } from '@pages/Datasets/Dataset/Dataset.types';
import { TGetDatasetSuccess } from '../dataset/dataset.typeDefs';

export type TPostUnifiedRegistryStart = {
  Name: string;
  Description: string;
};
export type TPostUnifiedRegistrySuccess = null;

export type TDeleteUnifiedRegistryStart = {
  ID: string;
};
export type TDeleteUnifiedRegistrySuccess = null;

export type TGetAllUnifiedRegistriesStart = {};

export type TGetAllUnifiedRegistriesSuccess = {
  UnifiedRegistries: Record<
    string,
    TGetUnifiedRegistrySuccess['UnifiedRegistry']
  >;
};

export type TGetUnifiedRegistrySuccess = {
  UnifiedRegistry: {
    ID: string;
    Name: string;
    Description: string;
    Image: string;
    CreatedAt: Date;
    UpdateAt: Date;
    Datasets: Record<string, TGetDatasetSuccess['Dataset']>;
  };
};

export type TGetUnifiedRegistryStart = {
  ID: string;
};

export type TPutUnifiedRegistrySuccess = null;

export type TPutUnifiedRegistryStart = {
  ID: string;
};
