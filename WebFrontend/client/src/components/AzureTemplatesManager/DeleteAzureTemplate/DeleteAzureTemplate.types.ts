import { IDefaults } from '@redux/typedefs';
import {
  TDeleteAzureTemplateStart,
} from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';

export type TDeleteAzureTemplateProps = {
  deleteAzureTemplateStart(
    data: TDeleteAzureTemplateStart
  ): void;
  deleteAzureTemplateReset(): void;
  deleteAzureTemplateState: IDefaults['state'];

  listAzureTemplatesReset(): void;
  listAzureTemplatesStart(): void;

  TemplateGuid: string;

  closeModal(): void;
};

export type TDeleteAzureTemplateFormProps = {
  deleteAzureTemplateStart(
    data: TDeleteAzureTemplateStart
  ): void;
  deleteAzureTemplateReset(): void;

  TemplateGuid: string;
};

export type TDeleteAzureTemplateSuccessProps = {
  closeModal(): void;
}
