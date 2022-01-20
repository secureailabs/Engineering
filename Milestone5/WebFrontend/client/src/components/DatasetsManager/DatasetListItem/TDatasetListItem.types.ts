export type TDatasetListItem = {
  // The index is used to switch between white and whitesmoke bg colors
  index: number;
  DatasetName: string;
  DataOwnerGuid: string;
  OrganizationName: string;
  Keywords: string;
  PublishDate: number;
  onClick(): void;
};
