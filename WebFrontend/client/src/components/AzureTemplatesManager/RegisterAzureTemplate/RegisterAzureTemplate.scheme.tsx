import * as yup from 'yup';

const RegisterAzureTemplateScheme = yup.object({
  Name: yup
  .string()
  .required('Name field is required'),
  Description: yup
  .string()
  .required('Description field is required'),
  HostRegion: yup
    .string()
    .required('Host region field is required'),
  SubscriptionID: yup
  .string()
  .required('Subscription ID field is required'),
  Secret: yup
  .string()
  .required('Secret field is required'),
  TenantID: yup
  .string()
  .required('Tenand ID field is required'),
  ApplicationID: yup
  .string()
  .required('Applicaiton ID field is required'),
  ResourceGroup: yup
  .string()
  .required('Resource group field is required'),
  VirtualNetwork: yup
  .string()
  .required('Virtual Network field is required'),
  NetworkSecurityGroup: yup
  .string()
  .required('Network Security Group field is required'),
  VirtualMachineImage: yup
  .string()
  .required('Virtual Machine Image field is required'),
});
export default RegisterAzureTemplateScheme;
