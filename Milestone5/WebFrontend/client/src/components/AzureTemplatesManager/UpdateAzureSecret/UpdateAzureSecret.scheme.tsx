import * as yup from 'yup';

const UpdateAzureSecretScheme = yup.object({
  'Secret': yup
    .string()
    .required('Legal agreement is required'),
});
export default UpdateAzureSecretScheme;
