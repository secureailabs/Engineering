import * as yup from 'yup';
import password from 'yup-password';

// Adds password methods to yup
password(yup);

// const UpdatePasswordScheme = yup.object().shape({
//   CurrentPassword: yup.string().required('Password field is required'),
//   NewPassword: yup.string().required('Password is required'),
//   ConfirmNewPassword: yup.string().required('Password field is required')
// });
const UpdatePasswordScheme = yup.object({
  CurrentPassword: yup.string()
    .required('Password field is required'),
  NewPassword: yup
  .string()
  .required('Password field is required')
  .password()
  .min(15, 'Password must have at least 15 characters')
  .minLowercase(1, 'Password must have at least one lowercase')
  .minUppercase(1, 'Password must have at least one uppercase')
  .minNumbers(1, 'Password must have at least one number')
  .minSymbols(1, 'Password must have at least one punctuation'),
ConfirmNewPassword: yup
  .string()
  .required('Password confirmation field is required')
  .oneOf([yup.ref('NewPassword'), null], 'Passwords must match')
  // Also has all of the password field's requirements
  // because we dont want it to be valid if the pwd isnt valid
  .min(15, 'Password must have at least 15 characters')
  .minLowercase(1, 'Password must have at least one lowercase')
  .minUppercase(1, 'Password must have at least one uppercase')
  .minNumbers(1, 'Password must have at least one number')
  .minSymbols(1, 'Password must have at least one punctuation'),
});
export default UpdatePasswordScheme;
