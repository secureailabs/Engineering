import React from 'react';

import type { TTileProps } from './TTile.types';

const Tile: React.FC<TTileProps> = ({ Icon, title, description, onClick }) => {
  return (
    <div className="tile" onClick={onClick}>
      <div className="tile__title">{title}</div>
      <Icon className="tile__icon" />

      <div className="tile__description">{description}</div>
    </div>
  );
};

export default Tile;
