import * as yup from 'yup';
import password from 'yup-password';
import 'yup-phone';

const phoneRegExp = /^[^a-zA-Z]*$/

// Adds password methods to yup
password(yup);

const RegisterUserScheme = yup.object({
  Email: yup
  .string()
  .required('Email field is required')
  .email('Invalid email address'),
  Password: yup
    .string()
    .required('Password field is required')
    .password()
    .min(15, 'Password must have at least 15 characters')
    .minLowercase(1, 'Password must have at least one lowercase')
    .minUppercase(1, 'Password must have at least one uppercase')
    .minNumbers(1, 'Password must have at least one number')
    .minSymbols(1, 'Password must have at least one punctuation'),
  PasswordConfirmation: yup
    .string()
    .required('Password confirmation field is required')
    .oneOf([yup.ref('Password'), null], 'Passwords must match')
    .password()
    // Also has all of the password field's requirements
    // because we dont want it to be valid if the pwd isnt valid
    .min(15, 'Password must have at least 15 characters')
    .minLowercase(1, 'Password must have at least one lowercase')
    .minUppercase(1, 'Password must have at least one uppercase')
    .minNumbers(1, 'Password must have at least one number')
    .minSymbols(1, 'Password must have at least one punctuation'),
  // AccessRights: yup
  //   .string()
  //   .nullable()
  //   .required('Access rights field is required.'),
  Name: yup
    .string()
    .required('Name field is required'),
  Title: yup
    .string()
    .required('Title field is required'),
  PhoneNumber: yup
    .string()
    .nullable()
    .required('Phone number field is required')
    // .phone(undefined, undefined, 'Invalid phone number')
    .matches(phoneRegExp, 'A phone number cannot contain any letters'),
});
export default RegisterUserScheme;
