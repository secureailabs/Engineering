import React, { ReactElement } from 'react';

import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css';
import Loader from 'react-loader-spinner';

const Spinner: React.FC = (): ReactElement => (
  <div className="spinner">
    <Loader type="Puff" color="#fcd0b7" height={100} width={100} />
  </div>
);

export default Spinner;
