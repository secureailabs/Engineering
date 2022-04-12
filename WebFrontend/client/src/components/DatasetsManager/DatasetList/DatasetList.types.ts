import { TGetAllDatasetsSuccess } from '@redux/dataset/dataset.typeDefs';

export type TDatasetList = {
  setDatasetID(dataset: string): void;
  Datasets: {
    PublishDate: string;
    DataOwnerGuid: string;
    DatasetGuid: string;
    DatasetName: string;
    Description: string;
    JurisdictionalLimitations: string;
    Keywords: string;
    OrganizationName: string;
    PrivacyLevel: number;
    key: string;
  }[];
};
