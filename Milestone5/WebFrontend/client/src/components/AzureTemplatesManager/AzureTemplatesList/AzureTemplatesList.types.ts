import { TPullAzureTemplateSuccess } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';

export type TAzureTemplatesList = {
  setAzureTemplateID(azureTemplate: string): void;
  onClick?(key: string): void;

  data: Array<TPullAzureTemplateSuccess['Template']>;
};
