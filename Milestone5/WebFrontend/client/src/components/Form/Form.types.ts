import { ReactElement } from 'react';

export type TForm = {
  children: ReactElement;
  actualForm?: boolean;
  onSubmit?(): void;
};
