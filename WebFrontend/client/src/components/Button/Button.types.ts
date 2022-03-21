import { ReactElement } from 'react';

export type TButton = {
  children: ReactElement | string;
  onClick?(): void;
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset' | undefined;
  size?: 'small';
};
