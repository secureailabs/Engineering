import * as yup from 'yup';

const RegisterDigitalContractScheme = yup.object({
  'Title': yup
    .string()
    .required('Title is required'),
  'Request Comments': yup
    .string()
    .required('Request comments are required'),
  'SubscriptionDays': yup
    .number()
    .positive()
    .integer()
    .required('Access duration is requried'),
});
export default RegisterDigitalContractScheme;
