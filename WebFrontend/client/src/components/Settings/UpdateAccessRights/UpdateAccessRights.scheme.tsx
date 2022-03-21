import * as yup from 'yup';
import password from 'yup-password';

// Adds password methods to yup
password(yup);

const UpdateOrganizationScheme = yup.object({
  AccessRights: yup.string().required('Password field is required'),
});
export default UpdateOrganizationScheme;
