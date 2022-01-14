import type { TFormFieldsRenderer } from '@components/FormFieldsRenderer';
import setFormIcon from '@utils/setFormIcon';

import { FieldValues, FormState } from 'react-hook-form';

export const formData: (
  formState: FormState<FieldValues>,
  trigger: (name?: any) => Promise<boolean>
) => TFormFieldsRenderer['fields'] = (formState, trigger) => {
  return {
    CurrentPassword: {
      type: 'password',
      tooltip: {
        icon: setFormIcon(formState, 'CurrentPassword', false, true, false)
      },
      errorMessage: formState.errors.CurrentPassword?.message,
    },
    NewPassword: {
      type: 'password',
      tooltip: {
        icon: setFormIcon(formState, 'NewPassword', true),
        tooltiptext:
          'Your password needs to be at least 15 characters long, must have one uppercase, one lowercase, one number and one punctuation in it and less than 50% of the password must be made up of words.',
      },
      errorMessage: formState.errors.NewPassword?.message,
      onChange: () => {
        if (formState.touchedFields.NewPassword) {
          trigger('ConfirmNewPassword');
        }
      },
    },
    ConfirmNewPassword: {
      type: 'password',
      tooltip: {
        icon: setFormIcon(formState, 'ConfirmNewPassword', true, true),
      },
      errorMessage: formState.errors.ConfirmNewPassword?.message,
    }
  };
};
