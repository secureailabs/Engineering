import { IDefaults } from '@redux/typedefs';
import { TUpdateAzureTemplateStart, TPullAzureTemplateSuccess } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';

export type TUpdateAzureSecretProps = {
  updateAzureSecretStart(data: TUpdateAzureTemplateStart): void;
  updateAzureSecretReset(): void;
  updateAzureSecretState: IDefaults['state'];
  pullAzureTemplateData: TPullAzureTemplateSuccess;
  closeModal(): void;
};

export type TUpdateAzureSecretFormProps = {
  updateAzureSecretStart(data: TUpdateAzureTemplateStart): void;
  pullAzureTemplateData: TPullAzureTemplateSuccess;
};

export type TUpdateAzureSecretSuccessProps = {
  closeModal(): void;
}
