import type { TFormFieldsRenderer } from '@components/FormFieldsRenderer';

import { FieldValues, FormState } from 'react-hook-form';

export const formData: (
  formState: FormState<FieldValues>
) => TFormFieldsRenderer['fields'] = (formState) => {
  return {

  };
};
