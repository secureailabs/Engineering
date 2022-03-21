import type { TFormFieldsRenderer } from '@components/FormFieldsRenderer';
import setFormIcon from '@utils/setFormIcon';

import { FieldValues, FormState } from 'react-hook-form';

export const formData: (
  formState: FormState<FieldValues>
) => TFormFieldsRenderer['fields'] = (formState) => {
  return {
    Name: {
      type: 'text',
    },
    HostRegion: {
      type: 'select',
      options: [
        {value: 'eastus', displayedText:'US East'},
        {value: 'eastus2', displayedText:'US East 2'},
        {value: 'northeurope', displayedText:'North Europe'},
        {value: 'westeurope', displayedText:'West Europe'},
      ],
    },
    Description: {
      type: 'textarea',
    },
    SubscriptionID: {
      type: 'text',
    },
    TenantID: {
      type: 'text',
    },
    ApplicationID: {
      type: 'text',
    },
    ResourceGroup: {
      type: 'text',
    },
    VirtualNetwork: {
      type: 'text',
    },
    NetworkSecurityGroup: {
      type: 'text',
    },
    VirtualMachineImage: {
      type: 'text',
      title: 'Virtual Machine Image'
    },
  }
};
