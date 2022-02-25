import { TGetAllAzureTemplatesSuccess } from '@redux/azureTemplate/azureTemplate.typesDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TAzureTemplatesProps = {
  getAllAzureTemplatesStart(): void;
  getAllAzureTemplatesReset(): void;
  getAllAzureTemplatesState: IDefaults['state'];
  getAllAzureTemplatesData: TGetAllAzureTemplatesSuccess;
};

export type TAzureTemplatesSuccessProps = {
  getAllAzureTemplatesData: TGetAllAzureTemplatesSuccess;
};
