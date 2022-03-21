import { IDefaults } from '@redux/typedefs';
import { TPullAzureTemplateSuccess } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';

export type TAzureTemplateInfoSuccess = {
  pullAzureTemplateData: TPullAzureTemplateSuccess | null;
  slideToPrev(): void;
};

export type TAzureTemplateInfo = {
  pullAzureTemplateStart(key: string): void;
  pullAzureTemplateReset(): void;
  pullAzureTemplateState: IDefaults['state'];
  pullAzureTemplateData: TPullAzureTemplateSuccess | null;
  azureTemplateID: string;
  slideToPrev(): void;
};
