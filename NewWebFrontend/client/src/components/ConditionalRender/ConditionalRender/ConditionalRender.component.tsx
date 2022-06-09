import React, { ReactElement } from 'react';

import Spinner, { SpinnerOnly } from '../../Spinner';

import { IConditionalRender } from './ConditionalRender.types';

const ConditionalRender: React.FC<IConditionalRender> = ({
  state,
  success,
  failure,
  Loading,
  children,
  spinnerOnly = false,
}): ReactElement => {
  switch (state) {
    case 'success':
      return <>{success()}</>;
    case 'failure':
      return <>{failure()}</>;
    case 'isLoading':
      //@ts-ignore
      return Loading ? Loading : spinnerOnly ? <SpinnerOnly /> : <Spinner />;
    default:
      return <>{children}</>;
  }
};

export default ConditionalRender;
