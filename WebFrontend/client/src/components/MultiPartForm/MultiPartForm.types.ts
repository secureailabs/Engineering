import { TFormFieldsRenderer } from '@components/FormFieldsRenderer';

export type TMultiPartForm = {
  forms: Array<[string, TFormFieldsRenderer['fields']]>;
  formState: TFormFieldsRenderer['formState'];
  register: TFormFieldsRenderer['register'];
  onSubmit(): void;
};
