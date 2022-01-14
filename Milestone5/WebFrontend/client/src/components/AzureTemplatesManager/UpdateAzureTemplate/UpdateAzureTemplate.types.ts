import {
  TUpdateAzureTemplateStart,
  TPullAzureTemplateStart,
  TPullAzureTemplateSuccess,
} from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';
import { IDefaults } from '@redux/typedefs';

export type TUpdateAzureTemplateProps = {
  updateAzureTemplateStart(data: TUpdateAzureTemplateStart): void;
  updateAzureTemplateReset(): void;
  pullAzureTemplateStart(data: TPullAzureTemplateStart): void;
  updateAzureTemplateState: IDefaults['state'];
  pullAzureTemplateData: TPullAzureTemplateSuccess;
  slideToPrev(): void;
};

export type TUpdateAzureTemplateFormProps = {
  updateAzureTemplateStart(data: TUpdateAzureTemplateStart): void;
  updateAzureTemplateReset(): void;
  pullAzureTemplateData: TPullAzureTemplateSuccess;
  slideToPrev(): void;
};

export type TUpdateAzureTemplateSuccessProps = {
  updateAzureTemplateStart(data: TUpdateAzureTemplateStart): void;
  updateAzureTemplateState: IDefaults['state'];
  updateSuccess: (data: boolean) => void;
  pullAzureTemplateStart(data: TPullAzureTemplateStart): void;
  pullAzureTemplateData: TPullAzureTemplateSuccess;
};
