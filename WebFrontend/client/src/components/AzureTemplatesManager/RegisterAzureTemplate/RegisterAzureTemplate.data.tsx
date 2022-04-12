import type { TFormFieldsRenderer } from '@components/FormFieldsRenderer';

import { FieldValues, FormState } from 'react-hook-form';

export const formData: (
  formState: FormState<FieldValues>,
  trigger: (name?: any) => Promise<boolean>
) => TFormFieldsRenderer['fields'] = (formState, trigger) => {
  return {
    Name: {
      type: 'text',
      tooltip: {icon: '?', tooltiptext: 'Name you wish to provide for your template.'}
    },
    HostRegion: {
      type: 'select',
      tooltip: {icon: '?', tooltiptext: 'The region to host the computation node virtual machines.'},
      options: [
        {value: 'eastus', displayedText:'US East'},
        {value: 'eastus2', displayedText:'US East 2'},
        {value: 'northeurope', displayedText:'North Europe'},
        {value: 'westeurope', displayedText:'West Europe'},
      ],
    },
    Description: {
      type: 'textarea',
      tooltip: {icon: '?', tooltiptext: 'Description you want to give to your template.'}
    },
    SubscriptionID: {
      title: 'Subscription ID',
      type: 'text',
      tooltip: {icon: '?', tooltiptext: 'Azure subscription.'},
    },
    Secret: {
      type: 'password',
      title: 'Secret/Password'
    },
    TenantID: {
      title: 'Tenant ID',
      type: 'text',
      tooltip: {icon: '?', tooltiptext: 'GUID of Azure tenant who is signing in.'},
    },
    ApplicationID: {
      title: 'Application ID',
      type: 'text',
      tooltip: {icon: '?', tooltiptext: 'Application GUID which can be created using \'az ad sp create-for-rbac\'.'},
    },
    ResourceGroup: {
      type: 'text',
      tooltip: {icon: '?', tooltiptext: 'All the computation resources will be present in this resource group, it will be created if it doesn\'t already exist.'},
    },
    VirtualNetwork: {
      type: 'text',
      tooltip: {icon: '?', tooltiptext: 'An existing virtual network can be used. If not present in the resource group, a new one will be created with default settings and the provided name.'},
    },
    VirtualMachineImage: {
      type: 'text',
      title: 'Virtual Machine Image',
      tooltip: {icon: '?', tooltiptext: 'An existing virtual machine from the same resource group can be used. If it\'s not present, a new one will be created with the provided name.'},
    },
    NetworkSecurityGroup: {
      type: 'text',
      tooltip: {icon: '?', tooltiptext: 'An existing network security group can be used. If it\'s not present in the resource group, a new one will be created with default settings and the provided name.'},
    },
  };
};

// TITLE, SUBSCRIPTION DAYS AND LEGAL AGREEMENT
