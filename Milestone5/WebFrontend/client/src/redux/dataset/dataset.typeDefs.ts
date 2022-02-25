export type TPostDatasetStart = {
  DataOwnerOrganization: string;
  Title: string;
  VersionNumber: string;
  SubscriptionDays: number;
  DatasetGuid: string;
  Description: string;
  LegalAgreement: string;
  DatasetDRMMetadataSize: number;
  DatasetDRMMetadata: string;
};
export type TPostDatasetSuccess = null;

export type TPatchAcceptDatasetStart = {
  DatasetGuid: string;
  RetentionTime: number;
  EULA: string;
  LegalAgreement: number;
};

export type TPatchAcceptDatasetSuccess = null;

export type TPatchActivateDatasetStart = {
  DatasetGuid: string;
  EULA: string;
  LegalAgreement: number;
};

export type TPatchActivateDatasetSuccess = null;

export type TGetAllDatasetsSuccess = {
  Datasets: Record<string, TGetDatasetSuccess['Dataset']>;
};

export type TGetDatasetSuccess = {
  Dataset: {
    DataOwnerGuid: string;
    DatasetGuid: string;
    DatasetName: string;
    Description: string;
    Versions?: Record<string, TGetDatasetSuccess>;
    Version?: number;
    JurisdictionalLimitations: string;
    Keywords: string;
    OrganizationName: string;
    PrivacyLevel: number;
    PublishDate: number;
  };
};

export type TGetDatasetStart = {
  DatasetGuid: string;
};

export type TGetDatasetVersionSuccess = TGetDatasetSuccess;

export type TGetDatasetVersionStart = TGetDatasetStart & {
  Version: string;
};
