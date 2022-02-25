import { TGetAzureTemplateSuccess } from '@redux/azureTemplate/azureTemplate.typesDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TAzureTemplateProps = {
  getAzureTemplateStart(): void;
  getAzureTemplateReset(): void;
  getAzureTemplateState: IDefaults['state'];
  getAzureTemplateData: TGetAzureTemplateSuccess;
  userData: IUserData;
};

export type TAzureTemplateSuccessProps = {
  getAzureTemplateData: TGetAzureTemplateSuccess;
};
