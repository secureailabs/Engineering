import React from 'react';
import { BiError } from 'react-icons/bi';

import { TErrorMessageProps } from './ErrorMessage.types';

const ErrorMessage: React.FC<TErrorMessageProps> = (props) => {
  return (
    <div className="error-message">
      <BiError size={20} />
      {props.errorMessage}
    </div>
  );
};

export default ErrorMessage;
