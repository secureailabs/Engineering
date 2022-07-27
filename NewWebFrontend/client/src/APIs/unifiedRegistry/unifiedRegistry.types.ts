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
    NumberOfDataOwner: number,
    NumberOfPatients: number,
    Image: string;
    CreatedAt: Date;
    UpdateAt: Date;
    Datasets: Record<string, TGetDatasetSuccess>;

    // These types are for demo purposes only, they are not currently implemented in the backend
    owner_name?: string;
    owner_email?: string;
    owner_org?: string;
    owner_org_id?: string;
    owner_org_url?: string;
    members_data?: {
      providers: {
        name: string;
        buttonText: string;
        invite_pending?: boolean;
      }[]
      ,
      users: {
        name: string;
      }[]
    }
  };
};

export type TGetUnifiedRegistryStart = {
  ID: string;
};

export type TPutUnifiedRegistrySuccess = null;

export type TPutUnifiedRegistryStart = {
  ID: string;
};
