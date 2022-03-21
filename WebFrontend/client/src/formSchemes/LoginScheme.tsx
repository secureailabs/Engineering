import * as yup from 'yup';
import password from 'yup-password';

// Adds password methods to yup
password(yup);

const LoginScheme = yup.object({
  email: yup
    .string()
    .email('Invalid email address')
    .required('Email field is required'),
  password: yup
    .string()
    // .password()
    // .min(15, 'Password must have at least 15 characters')
    // .minLowercase(1, 'Password must have at least one lowercase')
    // .minUppercase(1, 'Password must have at least one uppercase')
    // .minNumbers(1, 'Password must have at least one number')
    // .minSymbols(1, 'Password must have at least one punctuation')
    .required('Password field is required'),
});
export default LoginScheme;
