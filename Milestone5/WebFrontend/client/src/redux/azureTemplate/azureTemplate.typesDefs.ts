export type TPostAzureTemplateStart = {
  TemplateData: {
    Name: string;
    Description: string;
    SubscriptionID: string;
    Secret: string;
    TenantID: string;
    ApplicationID: string;
    ResourceGroup: string;
    VirtualNetwork: string;
    HostRegion: string;
    VirtualMachineImage: string;
  };
};

export type TPostAzureTemplateSuccess = null;

export type TGetAllAzureTemplatesStart = null;

export type TGetAllAzureTemplatesSuccess = {
  Templates: Record<
    string,
    {
      Name: string;
      Description: string;
      SubscriptionID: string;
      TenantID: string;
      ApplicationID: string;
      ResourceGroup: string;
      VirtualNetwork: string;
      HostRegion: string;
      VirtualMachineImage: string;
      State: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11;
      Note: string;
    }
  >;
};

export type TGetAzureTemplateStart = {
  TemplateGuid: string;
};

export type TGetAzureTemplateSuccess = {
  Template: {
    TemplateGuid: string;
    Name: string;
    Description: string;
    SubscriptionID: string;
    TenantID: string;
    ApplicationID: string;
    ResourceGroup: string;
    VirtualNetwork: string;
    HostRegion: string;
    VirtualMachineImage: string;
    State: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11;
    Note: string;
  };
};

export type TPutUpdateAzureTemplateStart = {
  TemplateGuid: string;
  TemplateData: {
    Name: string;
    Description: string;
    SubscriptionID: string;
    Secret?: string;
    TenantID: string;
    ApplicationID: string;
    ResourceGroup: string;
    VirtualNetwork: string;
    HostRegion: string;
    VirtualMachineImage: string;
    State: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11;
  };
};

export type TPutUpdateAzureTemplateSuccess = null;

export type TPutUpdateAzureSecretStart = {
  TemplateGuid: string;
  TemplateData: {
    Name: string;
    Description: string;
    SubscriptionID: string;
    Secret?: string;
    TenantID: string;
    ApplicationID: string;
    ResourceGroup: string;
    VirtualNetwork: string;
    HostRegion: string;
    VirtualMachineImage: string;
    State: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11;
  };
};

export type TPutUpdateAzureSecretSuccess = null;

export type TDeleteAzureTemplateStart = {
  TemplateGuid: string;
};

export type TDeleteAzureTemplateSuccess = null;
