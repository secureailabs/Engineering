import React from 'react';

export interface IConditionalRender {
  spinnerOnly?: boolean;
  state: 'success' | 'failure' | 'isLoading' | null;
  children: React.FC | JSX.Element;
  failure(): React.FC | JSX.Element;
  success(): React.FC | JSX.Element;
  Loading?: React.FC | JSX.Element;
}
