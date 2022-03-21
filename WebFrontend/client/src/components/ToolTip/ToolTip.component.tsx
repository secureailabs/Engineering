import React from 'react';
import { FaQuestionCircle, FaTimes, FaCheck } from 'react-icons/fa';

import { TTooltipProps } from './ToolTip.types';

// We use this interface in TextInput.tsx to make sure the TextInput's tooltip prop contains everything
const Tooltip: React.FC<TTooltipProps> = (props) => {
  return (
    <div className="tool-tip">
      {props.icon == '?' && <FaQuestionCircle size={20} />}
      {props.icon == 'X' && <FaTimes size={20} />}
      {props.icon == 'V' && <FaCheck size={20} />}
      {'tooltiptext' in props && (
        <div className='tool-tip__textcontainer'>
          <span className="tool-tip__text">{props.tooltiptext}</span>
        </div>
      )}
    </div>
  );
};

export default Tooltip;
