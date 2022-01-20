import type { TFormFieldsRenderer } from '@components/FormFieldsRenderer';

import { FieldValues, FormState } from 'react-hook-form';
import setFormIcon from '@utils/setFormIcon';
import accessRightsNumberToString from '@utils/accessRightsNumberToString';

export const formData: (
  formState: FormState<FieldValues>,
  trigger: (name?: any) => Promise<boolean>
) => TFormFieldsRenderer['fields'] = (formState, trigger) => {
  return {
    Email: {
      type: 'text',
      tooltip: {
        icon: setFormIcon(formState, 'Email', false, true, false),
      },
      errorMessage: formState.errors.Email?.message,
    },
    Password: {
      type: 'password',
      errorMessage: formState.errors.Password?.message,
      tooltip: {
        icon: setFormIcon(formState, 'Password', false, true, false),
        tooltiptext:
          'A password needs to be at least 15 characters long, must have one uppercase, one lowercase, one number and one punctuation in it and less than 50% of the password must be made up of words.',
      },
      onChange: () => {
        if (formState.touchedFields.PasswordConfirmation) {
          trigger('PasswordConfirmation');
        }
      }
    },
    PasswordConfirmation: {
      type: 'password',
      errorMessage: formState.errors.PasswordConfirmation?.message,
      tooltip: {
        icon: setFormIcon(formState, 'PasswordConfirmation', false, true, false),
        tooltiptext:
          'A password needs to be at least 15 characters long, must have one uppercase, one lowercase, one number and one punctuation in it and less than 50% of the password must be made up of words.',
      },
    },
    // AccessRights: {
    //   type:  'radio',
    //   options: [
    //     {value: '1', displayedText: accessRightsNumberToString(1), tooltip: {tooltiptext: `${accessRightsNumberToString(1)}s have every permission.\n\nPermissions:\n\t\u2022 do this \n\t\u2022 do that`, icon: '?'}},
    //     {value: '2', displayedText: accessRightsNumberToString(2), tooltip: {tooltiptext: `${accessRightsNumberToString(2)}s ...\n\nPermissions:\n\t\u2022 do this \n\t\u2022 do that`, icon: '?'}},
    //     {value: '3', displayedText: accessRightsNumberToString(3), tooltip: {tooltiptext: `${accessRightsNumberToString(3)}s ...\n\nPermissions:\n\t\u2022 do this \n\t\u2022 do that`, icon: '?'}},
    //     {value: '4', displayedText: accessRightsNumberToString(4), tooltip: {tooltiptext: `${accessRightsNumberToString(4)}s ...\n\nPermissions:\n\t\u2022 do this \n\t\u2022 do that`, icon: '?'}},
    //     {value: '5', displayedText: accessRightsNumberToString(5), tooltip: {tooltiptext: `${accessRightsNumberToString(5)}s ...\n\nPermissions:\n\t\u2022 do this \n\t\u2022 do that`, icon: '?'}},
    //   ],
    //   tooltip: {
    //     icon: setFormIcon(formState, 'AccessRights', false, true, false),
    //     tooltiptext: 'This should be the legal name of your organization.',
    //   },
    //   errorMessage: formState.errors.AccessRights?.message,
    // },
    Name: {
      type: 'text',
      errorMessage: formState.errors.Name?.message,
      tooltip: {
        icon: setFormIcon(formState, 'Name', false, true, false),
        tooltiptext: 'This should be the legal name of your organization.',
      },
    },
    Title: {
      type: 'text',
      title: 'Job Title',
      tooltip: {
        icon: setFormIcon(formState, 'Title', false, true, false),
        tooltiptext: 'This should be the legal name of your organization.',
      },
      errorMessage: formState.errors.Title?.message,
    },
    PhoneNumber: {
      type: 'text',
      errorMessage: formState.errors.PhoneNumber?.message,
      tooltip: {
        icon: setFormIcon(formState, 'PhoneNumber', false, true, false),
        tooltiptext: 'This should be your work phone number.',
      },
    },
  };
};

// TITLE, SUBSCRIPTION DAYS AND LEGAL AGREEMENT
