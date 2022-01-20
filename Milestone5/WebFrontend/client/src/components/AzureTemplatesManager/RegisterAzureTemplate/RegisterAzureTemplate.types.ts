import { TRegisterAzureTemplateStart } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';
import { IDefaults } from '@redux/typedefs';

export type TRegisterAzureTemplateProps = {
  registerAzureTemplateStart(data: TRegisterAzureTemplateStart): void;
  registerAzureTemplateReset(): void;
  listAzureTemplatesStart(): void;
  listAzureTemplatesReset(): void;
  registerAzureTemplateState: IDefaults['state'];
  closeModal(): void;
};

export type TRegisterAzureTemplateFormProps = {
  registerAzureTemplateStart(data: TRegisterAzureTemplateStart): void;
  registerAzureTemplateReset(): void;
};

export type TRegisterAzureTemplateSuccess = {
  closeModal(): void;
};
