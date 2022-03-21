import * as yup from 'yup';
import password from 'yup-password';
import 'yup-phone';

const phoneRegExp = /^[^a-zA-Z]*$/

// Adds password methods to yup
password(yup);

const SignupScheme = yup.object({
  email: yup
    .string()
    .required('Email field is required')
    .email('Invalid email address'),
  organizationName: yup
    .string()
    .required('Organization field is required'),
  password: yup
    .string()
    .required('Password field is required')
    .password()
    .min(15, 'Password must have at least 15 characters')
    .minLowercase(1, 'Password must have at least one lowercase')
    .minUppercase(1, 'Password must have at least one uppercase')
    .minNumbers(1, 'Password must have at least one number')
    .minSymbols(1, 'Password must have at least one punctuation'),
  passwordConfirmation: yup
    .string()
    .required('Password confirmation field is required')
    .oneOf([yup.ref('password'), null], 'Passwords must match')
    // Also has all of the password field's requirements
    // because we dont want it to be valid if the pwd isnt valid
    .min(15, 'Password must have at least 15 characters')
    .minLowercase(1, 'Password must have at least one lowercase')
    .minUppercase(1, 'Password must have at least one uppercase')
    .minNumbers(1, 'Password must have at least one number')
    .minSymbols(1, 'Password must have at least one punctuation'),
  name: yup
    .string()
    .required('Name field is required'),
  phoneNumber: yup
    .string()
    .required('Phone number field is required')
    // .phone(undefined, undefined, 'Invalid phone number')
    .matches(phoneRegExp, 'A phone number cannot contain any letters'),
  title: yup
    .string()
    .required('Title field is required'),
  primaryContactName: yup
    .string()
    .required('Primary contact name field is required'),
  primaryContactTitle: yup
    .string()
    .required('Primary contact title field is required'),
  primaryContactEmail: yup
    .string()
    .required('Primary contact email address field is required')
    .email('Invalid email address'),
  primaryContactPhoneNumber: yup
    .string()
    .required('Primary contact phone number field is required')
    // .phone(undefined, undefined, 'Invalid phone number')
    .matches(phoneRegExp, 'A phone number cannot contain any letters'),
  secondaryContactName: yup
    .string()
    .required('Secondary contact name field is required'),
  secondaryContactTitle: yup
    .string()
    .required('Secondary contact title field is required'),
  secondaryContactEmail: yup
    .string()
    .required('Secondary contact email address field is required')
    .email('Invalid email address'),
  secondaryContactPhoneNumber: yup
    .string()
    .required('Secondary contact phone number field is required')
    // .phone(undefined, undefined, 'Invalid phone number')
    .matches(phoneRegExp, 'A phone number canno,t contain any letters'),
  organizationAddressLine1: yup
    .string()
    .required('Organization address line 1 field is required'),
  organizationAddressLine2: yup
    .string(),
  organizationAddressCity: yup
    .string()
    .required('Organization city field is required'),
  organizationAddressState: yup
    .string()
    .required('Organization state/province field is required'),
  organizationAddressZip: yup
    .string()
    .required('Organization zip/postal code field is required'),
  organizationAddressCountry: yup
    .string()
    .required('Organization country field is required'),
});

export default SignupScheme;
