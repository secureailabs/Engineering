import { IconType } from 'react-icons';

export type TGetAllDocumentationSuccess = {
  documentation: Array<TGetDocumentationSuccess>;
};

export type TGetDocumentationSuccess = {
  id: string;
  icon: IconType;
  primaryText: string;
  secondaryText: string;
  documentationUrl: string;
};

export type TGetDocumentationStart = {
  id: string;
};
