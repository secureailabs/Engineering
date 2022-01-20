import type { TFormFieldsRenderer } from '@components/FormFieldsRenderer';
import setFormIcon from '@utils/setFormIcon';

import { FieldValues, FormState } from 'react-hook-form';

export const formData: (
  formState: FormState<FieldValues>
) => TFormFieldsRenderer['fields'] = (formState) => {
  return {
    Name: {
      type: 'text',
      tooltip: {
        icon: setFormIcon(formState, 'Name', true, true, false)
      },
    },
    Title: {
      type: 'text',
      title: 'Job title',
      tooltip: {
        icon: setFormIcon(formState, 'Title', true, true, false)
      },
    },
    PhoneNumber: {
      type: 'text',
      tooltip: {
        icon: setFormIcon(formState, 'PhoneNumber', true, true, false)
      },
    },
  };
};
