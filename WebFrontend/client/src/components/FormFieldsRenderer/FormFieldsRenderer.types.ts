import { FieldValues, FormState, UseFormRegister } from 'react-hook-form';

import { TTextInputProps } from '@components/Inputs/TextInput';
import { TRadioInputProps } from '@components/Inputs/RadioInput';

export type TFormFieldsRenderer = {
  fields: Record<
    string,
    {
      type: 'text' | 'password' | 'textarea' | 'number' | 'radio' | 'select';
      title?: TTextInputProps['title'];
      tooltip?: TTextInputProps['tooltip'];
      options?: TRadioInputProps['options'];
      errorMessage?: TTextInputProps['errorMessage'];
      onChange?: TTextInputProps['onChange'];
    }
  >;
  register: UseFormRegister<any>;
  formState: FormState<any>;
  description?: string;
};
