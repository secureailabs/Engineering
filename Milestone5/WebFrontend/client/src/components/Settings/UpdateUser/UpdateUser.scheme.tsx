import * as yup from 'yup';
import 'yup-phone';

const phoneRegExp = /^[^a-zA-Z]*$/;

const UpdateOrganizationScheme = yup.object({
  Name: yup.string().required('Name field is required'),
  Title: yup.string().required('Title field is required'),
  PhoneNumber: yup
    .string()
    .nullable()
    .required('Phone number field is required'),
  // .phone('US', false, 'Invalid phone number')
  // .matches(phoneRegExp, 'A phone number cannot contain any letters'),
});
export default UpdateOrganizationScheme;
