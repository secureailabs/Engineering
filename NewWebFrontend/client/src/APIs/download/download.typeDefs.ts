import { IconType } from 'react-icons';

export type TGetAllDownloadsSuccess = {
  downloads: Array<TGetDownloadSuccess>;
};

export type TGetDownloadSuccess = {
  id: string;
  icon: IconType;
  primaryText: string;
  secondaryText: string;
  version: string;
  publish_date: string;
  buttonText: string;
  buttonUrl: string;
  documentationUrl: string;
  documentationName: string;
  fileSize: string;
  systemRequirements: string;
};

export type TGetDownloadStart = {
  id: string;
};
