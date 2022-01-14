export type TRegisterAzureTemplateStart = {
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
    }
}

export type TRegisterAzureTemplateSuccess = null;

export type TListAzureTemplatesStart = null

export type TListAzureTemplatesSuccess = {
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
}

export type TPullAzureTemplateStart = {
    TemplateGuid: string;
}

export type TPullAzureTemplateSuccess = {
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
    }
}

export type TUpdateAzureTemplateStart = {
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
    }
}

export type TUpdateAzureTemplateSuccess = null;

export type TDeleteAzureTemplateStart = {
    TemplateGuid: string;
}

export type TDeleteAzureTemplateSuccess = null;