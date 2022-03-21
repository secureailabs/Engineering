import React from 'react';

import type { TForm } from './Form.types';

const Form: React.FC<TForm> = ({ children, actualForm, onSubmit }) => {
  if (actualForm) {
    return (
      <form onSubmit={onSubmit} autoComplete="new-password">
        <div className="form">{children}</div>
      </form>
    );
  }
  return <div className="form">{children}</div>;
};

export default Form;
