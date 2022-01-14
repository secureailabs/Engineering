import * as yup from 'yup';

const EditAzureTemplateScheme = yup.object({
  AzureTemplateGuid: yup.string(),
});
export default EditAzureTemplateScheme;
