import type { TFormFieldsRenderer } from '@components/FormFieldsRenderer';
import setFormIcon from '@utils/setFormIcon';

import { FieldValues, FormState } from 'react-hook-form';

export const formData: (
  formState: FormState<FieldValues>
) => TFormFieldsRenderer['fields'] = (formState) => {
  return {
    AzureTemplateGuid: {
      type: 'text',
    },
  };
};