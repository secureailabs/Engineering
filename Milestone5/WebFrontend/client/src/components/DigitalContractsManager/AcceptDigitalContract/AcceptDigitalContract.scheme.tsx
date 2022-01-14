import * as yup from 'yup';

const AcceptDigitalContractScheme = yup.object({
  'RetentionTime': yup
    .number()
    .positive()
    .integer()
    .required('Retention time is required'),
  'LegalAgreement': yup
    .string()
    .required('Legal agreement is required'),
  'HostForVirtualMachines': yup
    .string()
    .nullable()
    .required('Host of virtual machines field is required'),
  'NumberOfVirtualMachines': yup
    .number()
    .positive()
    .integer()
    .required('Number of virtual machines is required'),
  'NumberOfVCPU': yup
    .number()
    .positive()
    .integer()
    .required('Number of Virtual CPUs is required'),
  'HostRegion': yup
    .string()
    .required('Host region is required')
});
export default AcceptDigitalContractScheme;
