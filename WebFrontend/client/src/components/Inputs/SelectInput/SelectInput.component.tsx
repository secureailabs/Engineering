import React from 'react';
import { headerCase } from 'header-case';
import Tooltip from '@components/ToolTip';
import ErrorMessage from '@components/ErrorMessage';

import type { TSelectInputProps } from './SelectInput.types';

const SelectInput: React.FC<TSelectInputProps> = (props) => {

  const { register, onChange, ...otherProps } = props;

  return (
    <div className='select-input'>
     <label className='text-input__label'>{props.title ? props.title : headerCase(props.label)}</label>
     {'tooltip' in props && <Tooltip {...props.tooltip} />}
      <select {...register(props.label)}>
      {props.options.map(value => (
        <option key={value.value} value={value.value}>
          {value.displayedText ? value.displayedText : headerCase(value.value)}
        </option>
      ))}
      </select>
      {props.errorMessage &&
        props.tooltip?.icon != '?' &&
        props.tooltip?.icon != undefined && (
          <ErrorMessage errorMessage={props.errorMessage} />
      )}
    </div>
  )
};

export default SelectInput;
