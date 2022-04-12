import React from 'react';

import { TButton } from './Button.types';

const Button: React.FC<TButton> = ({
  disabled,
  onClick,
  children,
  type,
  size,
}) => {
  return (
    <button
      className={size === 'small' ? 'button--small' : ''}
      type={type}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;
