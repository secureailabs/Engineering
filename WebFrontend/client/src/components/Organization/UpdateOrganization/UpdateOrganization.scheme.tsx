import * as yup from 'yup';
import 'yup-phone';

const phoneRegExp = /^[^a-zA-Z]*$/;

const UpdateOrganizationScheme = yup.object({
  OrganizationName: yup
    .string()
    .required('Organization name field is required'),
  OrganizationAddress: yup
    .string()
    .required('Organization address field is required'),
  PrimaryContactEmail: yup
    .string()
    .required('Primary contact email field is required')
    .email('Invalid email address'),
  PrimaryContactName: yup
    .string()
    .required('Primary contact name field is required'),
  PrimaryContactPhoneNumber: yup
    .string()
    .required('Primary contact phone number field is required'),
  // .phone('US', false, 'Invalid phone number')
  // .matches(phoneRegExp, 'A phone number cannot contain any letters'),
  PrimaryContactTitle: yup
    .string()
    .required('Primary contact title field is required'),
  SecondaryContactEmail: yup
    .string()
    .required('Secondary contact email field is required')
    .email('Invalid email address'),
  SecondaryContactName: yup
    .string()
    .required('Secondary contact name field is required'),
  SecondaryContactPhoneNumber: yup
    .string()
    .required('Secondary contact phone number field is required'),
  // .phone('US', false, 'Invalid phone number')
  // .matches(phoneRegExp, 'A phone number cannot contain any letters'),
  SecondaryContactTitle: yup
    .string()
    .required('Secondary contact title field is required'),
});
export default UpdateOrganizationScheme;
