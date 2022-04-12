import type { TFormFieldsRenderer } from '@components/FormFieldsRenderer';
import setFormIcon from '@utils/setFormIcon';

import { FieldValues, FormState } from 'react-hook-form';

export const formData: (
  formState: FormState<FieldValues>
) => TFormFieldsRenderer['fields'] = (formState) => {
  return {
    OrganizationName: {
      type: 'text',
      tooltip: {
        icon: setFormIcon(formState, 'OrganizationName', false, true , false),
        tooltiptext: 'This should be the legal name of your organization.',
      }
    },
    OrganizationAddress: {
      type: 'text',
      tooltip: {
        icon: setFormIcon(formState, 'PrganizationAddress', false, false, false),
        tooltiptext: 'This should be the legal address of your organization.'
      }
    },
    PrimaryContactName: {
      type: 'text',
      tooltip: {
        icon: setFormIcon(formState, 'PrimaryContactName', false, true, false),
      }
    },
    PrimaryContactTitle: {
      type: 'text',
      title: 'Primary Contact Job Title',
      tooltip: {
        icon: setFormIcon(formState, 'PrimaryContactTitle', false, true, false),
      }
    },
    PrimaryContactEmail: {
      type: 'text',
      tooltip: {
        icon: setFormIcon(formState, 'PrimaryContactEmail', false, true),
      }
    },
    PrimaryContactPhoneNumber: {
      type: 'text',
      tooltip: {
        icon: setFormIcon(formState, 'PrimaryContactPhoneNumber', false, true, true),
      },
    },
    SecondaryContactName: {
      type: 'text',
      tooltip: {
        icon: setFormIcon(formState, 'SecondaryContactName', false, true, false),
      }
    },
    SecondaryContactTitle: {
      type: 'text',
      title: 'Secondary Contact Job Title',
      tooltip: {
        icon: setFormIcon(formState, 'SecondaryContactTitle', false, true, false),
      }
    },
    SecondaryContactEmail: {
      type: 'text',
      tooltip: {
        icon: setFormIcon(formState, 'SecondaryContactEmail', false, true),
      }
    },
    SecondaryContactPhoneNumber: {
      type: 'text',
      tooltip: {
        icon: setFormIcon(formState, 'SecondaryContactPhoneNumber', false, true, true),
      },
    },
  }
};
