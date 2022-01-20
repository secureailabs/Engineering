import { TListAzureTemplatesSuccess } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TAzureTemplatesManagerProps = {
  listAzureTemplatesStart(): void;
  listAzureTemplatesReset(): void;
  listAzureTemplatesState: IDefaults['state'];
  listAzureTemplatesData: TListAzureTemplatesSuccess;
  onClick(key: string): void;
};

export type TAzureTemplatesManagerSuccessProps = {
  setAzureTemplateID(data: string | null): void;
  listAzureTemplatesData: TListAzureTemplatesSuccess;
  onClick(key: string): void;
};
