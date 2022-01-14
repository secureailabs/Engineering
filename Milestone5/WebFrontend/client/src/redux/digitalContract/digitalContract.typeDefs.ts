export type TPostDigitalContractStart = {
  DataOwnerOrganization: string;
  Title: string;
  VersionNumber: string;
  SubscriptionDays: number;
  DatasetGuid: string;
  Description: string;
  LegalAgreement: string;
  DatasetDRMMetadataSize: number;
  DatasetDRMMetadata: Record<string, string>;
};
export type TPostDigitalContractSuccess = null;

export type TPatchAcceptDigitalContractStart = {
  DigitalContractGuid: string;
  RetentionTime: number;
  LegalAgreement: string;
  HostForVirtualMachines: string;
  NumberOfVirtualMachines: number;
  NumberOfVCPU: number;
  HostRegion: string;
};

export type TPatchAcceptDigitalContractSuccess = null;

export type TPatchActivateDigitalContractStart = {
  DigitalContractGuid: string;
  EULA: string;
  LegalAgreement: string;
};

export type TPatchActivateDigitalContractSuccess = null;

export type TGetAllDigitalContractsSuccess = {
  DigitalContracts: Record<
    string,
    TGetDigitalContractSuccess['DigitalContract']
  >;
};

export type TGetDigitalContractSuccess = {
  DigitalContract: {
    Title: string;
    VersionNumber: string;
    ContractStage: number;
    SubscriptionDays: number;
    Description: string;
    DatasetGuid: string;
    DatasetName: string;
    ActivationTime: number;
    ExpirationTime: number;
    Eula: string;
    LegalAgreement: string;
    DataOwnerOrganization: string;
    DOOName: string;
    ResearcherOrganization: string;
    ROName: string;
    LastActivity: number;
    ProvisioningStatus: number;
    HostForVirtualMachines: string;
    NumberOfVCPU: number;
    AzureTemplateGuid?: string;
    NumberOfVirtualMachines?: number;
    Note: string;
  };
};

export type TGetDigitalContractStart = {
  DigitalContractGuid: string;
};

export type TPatchAssociateAzureStart = {
  AzureTemplateGuid: string;
  ListOfDigitalContracts: string[];
};

export type TPatchAssociateAzureSuccess = {};

export type TGetProvisioningStatusStart = {
  DigitalContractGuid: string;
};

export type TGetProvisioningStatusSuccess = {
  ProvisioningStatus: 1 | 2 | 3 | 4;
  VirtualMachines?: Record<string, string>;
};

export type TProvisionDigitalContractStart = {
  DigitalContractGuid: string;
};

export type TProvisionDigitalContractSuccess = null;

export type TDeprovisionDigitalContractStart = {
  DigitalContractGuid: string;
};

export type TDeprovisionDigitalContractSuccess = null;

