import type { TFormFieldsRenderer } from '@components/FormFieldsRenderer';
import setFormIcon from '@utils/setFormIcon';

import { FieldValues, FormState } from 'react-hook-form';

export const formData: (
  formState: FormState<FieldValues>
) => TFormFieldsRenderer['fields'] = (formState) => {
  return {
    RetentionTime: {
      type: 'number',
      title: 'Retention Time (days)',
    },
    LegalAgreement: {
      type: 'textarea',
    },
    HostForVirtualMachines: {
      type: 'radio',
      options: [
            {value: 'Data Owner', displayedText: 'Data Owner'},
            {value: 'Researcher'},
          ],
    },
    NumberOfVirtualMachines: {
      type: 'number',
    },
    NumberOfVCPU: {
      title: 'Number of Virtual CPUs',
      type: 'radio',
      options: [
        {value: '4'},
        {value: '8'},
        {value: '16'},
        {value: '32'},
        {value: '48'},
      ],
    },
    HostRegion: {
      type: 'radio',
      options: [
        {value: 'eastus', displayedText:'US East'},
        {value: 'eastus2', displayedText:'US East 2'},
        {value: 'northeurope', displayedText:'North Europe'},
        {value: 'westeurope', displayedText:'West Europe'},
      ],
    }
  };
};
