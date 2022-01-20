import type { TFormFieldsRenderer } from '@components/FormFieldsRenderer';
import setFormIcon from '@utils/setFormIcon';

import { FieldValues, FormState } from 'react-hook-form';

//@ts-ignore
export const formData: (
  formState: FormState<FieldValues>,
  trigger: (name?: any) => Promise<boolean>
) => Array<[string, TFormFieldsRenderer['fields']]> = (formState, trigger) => {
  return [['You are about to create the administrator account for your organization. Please enter your organization\'s name and the administrator account\'s credentials.',
    {
      organizationName: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'organizationName'),
          tooltiptext: 'This should be the legal name of your organization.',
        },
        // errorMessage: formState.touchedFields.organizationName
        //   ? formState.errors.organizationName?.message
        //   : undefined,
        errorMessage: formState.errors.organizationName?.message
      },
      email: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'email'),
          tooltiptext:
            'Your email should be associated with the organization you are signing up for.',
        },
        errorMessage: formState.touchedFields.email
          ? formState.errors.email?.message
          : undefined,
      },
      password: {
        type: 'password',
        tooltip: {
          icon: setFormIcon(formState, 'password', true),
          tooltiptext:
            'Your password needs to be at least 15 characters long, must have one uppercase, one lowercase, one number and one punctuation in it and less than 50% of the password must be made up of words.',
        },
        errorMessage: formState.errors.password?.message,
        onChange: () => {
          if (formState.touchedFields.passwordConfirmation) {
            trigger('passwordConfirmation');
          }
        },
      },
      passwordConfirmation: {
        type: 'password',
        tooltip: {
          icon: setFormIcon(formState, 'passwordConfirmation', true, true),
        },
        errorMessage: formState.errors.passwordConfirmation?.message,
      },
    }],
    ['The administrator account will be at your name, let us know who you are and how we can contact you.', {
      name: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'name', false, false, false),
          tooltiptext: 'This should be your legal name.',
        },
        errorMessage: formState.touchedFields.name
          ? formState.errors.name?.message
          : undefined,
      },
      phoneNumber: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'phoneNumber', false, false, true),
          tooltiptext: 'This should be your work phone number.',
        },
        errorMessage: formState.touchedFields.phoneNumber
          ? formState.errors.phoneNumber?.message
          : undefined,
      },
      title: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'title', false, false, false),
          tooltiptext: 'This should be your job title.',
        },
        errorMessage: formState.touchedFields.title
          ? formState.errors.title?.message
          : undefined,
      },
    }],
    ['Who\'s the first person we should contact in case of emergency?', {
      primaryContactName: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'primaryContactName', false, true, false),
        },
        // onChange: () => console.log('changed'),
        errorMessage: formState.touchedFields.primaryContactName
          ? formState.errors.primaryContactName?.message
          : undefined,
      },
      primaryContactTitle: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'primaryContactTitle', false, true, false),
          // tooltiptext: 'This should be the legal name of your organization.',
        },
        errorMessage: formState.touchedFields.primaryContactTitle
          ? formState.errors.primaryContactTitle?.message
          : undefined,
      },
      primaryContactEmail: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'primaryContactEmail', false, true),
        },
        errorMessage: formState.touchedFields.primaryContactEmail
          ? formState.errors.primaryContactEmail?.message
          : undefined,
      },
      primaryContactPhoneNumber: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'primaryContactPhoneNumber', false, true, true),
          // tooltiptext: 'This should be the legal name of your organization.',
        },
        errorMessage: formState.touchedFields.primaryContactPhoneNumber
          ? formState.errors.primaryContactPhoneNumber?.message
          : undefined,
      },
    }],
    ['Who will save the day if the first person isn\'t available?', {
      secondaryContactName: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'secondaryContactName', false, true, false),
        },
        errorMessage: formState.touchedFields.secondaryContactName
          ? formState.errors.secondaryContactName?.message
          : undefined,
      },
      secondaryContactTitle: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'secondaryContactTitle', false, true, false),
        },
        errorMessage: formState.touchedFields.secondaryContactTitle
          ? formState.errors.secondaryContactTitle?.message
          : undefined,
      },
      secondaryContactEmail: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'secondaryContactEmail', false, true, true),
        },
        errorMessage: formState.touchedFields.secondaryContactEmail
          ? formState.errors.secondaryContactEmail?.message
          : undefined,
      },
      secondaryContactPhoneNumber: {
        type: 'text',
        tooltip: {
          icon: setFormIcon(formState, 'secondaryContactPhoneNumber', false, true, true),
        },
        errorMessage: formState.touchedFields.secondaryContactPhoneNumber
          ? formState.errors.secondaryContactPhoneNumber?.message
          : undefined,
      },
    }],
    ['One last thing, we need to know where to find you.', {
      organizationAddressLine1: {
        type: 'text',
        title: 'Organization Address Line 1',
        tooltip: {
          icon: setFormIcon(formState, 'organizationAddressLine1', false, false, false),
          tooltiptext: 'This should be the legal address of your organization.'
        },
        errorMessage: formState.touchedFields.organizationAddressLine1
          ? formState.errors.organizationAddressLine1?.message
          : undefined,
      },
      organizationAddressLine2: {
        type: 'text',
        title: 'Organization Address Line 2',
        errorMessage: formState.touchedFields.organizationAddressLine2
          ? formState.errors.organizationAddressLine2?.message
          : undefined,
      },
      organizationAddressCity: {
        type: 'text',
        title: 'City',
        tooltip: {
          icon: setFormIcon(formState, 'organizationAddressCity', false, true, false),
          tooltiptext: 'This should be the legal address of your organization.'
        },
        // errorMessage: formState.errors.organizationAddressCity?.message
        errorMessage: 'This is an error message'
        // errorMessage: formState.touchedFields.organizationAddressCity
        // ? formState.errors.organizationAddressCity?.message
        // : undefined,
      },
      organizationAddressState: {
        type: 'text',
        title: 'State/Province',
        tooltip: {
          icon: setFormIcon(formState, 'organizationAddressState', false, true, false),
          tooltiptext: 'This should be the legal address of your organization.'
        },
        errorMessage: formState.touchedFields.organizationAddressState
          ? formState.errors.organizationAddressState?.message
          : undefined,
      },
      organizationAddressZip: {
        type: 'text',
        title: 'Zip/Postal Code',
        tooltip: {
          icon: setFormIcon(formState, 'organizationAddressZip', false, true, false),
          tooltiptext: 'This should be the legal address of your organization.'
        },
        errorMessage: formState.touchedFields.organizationAddressZip
          ? formState.errors.organizationAddressZip?.message
          : undefined,
      },
      organizationAddressCountry: {
        type: 'text',
        title: 'Country',
        tooltip: {
          icon: setFormIcon(formState, 'organizationAddressCountry', false, true, false),
          tooltiptext: 'This should be the legal address of your organization.'
        },
        errorMessage: formState.touchedFields.organizationAddressCountry
          ? formState.errors.organizationAddressCountry?.message
          : undefined,
      },
    }],
  ];
};
