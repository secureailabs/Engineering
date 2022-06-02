import React from 'react';
//@ts-ignore
import SailLogo from '@assets/SailLogo.png';

const Logo: React.FC = () => {
  return (
    <div className="logo">
      <img src={SailLogo} />
    </div>
  );
};

export default Logo;
