import React from 'react';
import type { UseFormRegister } from 'react-hook-form';

import type { TTooltipProps } from '@components/ToolTip';

export type TTextInputProps = {
  // Text displayed above the input
  title?: string;
  // Used for the label's for attribute
  label: string;

  placeholder?: string;

  tooltip?: TTooltipProps;
  errorMessage?: string;
  onChange?: (
    e: React.FormEvent<HTMLInputElement> | React.FormEvent<HTMLTextAreaElement>
  ) => void;
  register: UseFormRegister<any>;
  type: string;
  defaultValue?: string;
};
