import type { TFormFieldsRenderer } from '@components/FormFieldsRenderer';

import { FieldValues, FormState } from 'react-hook-form';

export const formData: (
  formState: FormState<FieldValues>
) => TFormFieldsRenderer['fields'] = (formState) => {
  return {
    'Title': {
      type: 'text',
    },
    'SubscriptionDays': {
      type: 'number',
      title: 'Access Duration (days)'
    },
    'Request Comments': {
      type: 'textarea',
    },
  };
};

// TITLE, SUBSCRIPTION DAYS AND LEGAL AGREEMENT
