import { IconType } from 'react-icons/lib';

export type TTileProps = {
  title: string;
  description: string;
  Icon: IconType;
  onClick: () => void;
};
