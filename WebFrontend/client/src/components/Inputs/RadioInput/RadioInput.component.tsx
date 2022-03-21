import React from 'react';
import { headerCase } from 'header-case';
import Tooltip from '@components/ToolTip';
import ErrorMessage from '@components/ErrorMessage';

import type { TRadioInputProps } from './RadioInput.types';

const RadioInput: React.FC<TRadioInputProps> = (props) => {
  // Make the input type password if needed

  // Extract the onChange from register so we can add something to it
  const { register, onChange, ...otherProps } = props;
  // console.log(props.title)

  // console.log('radio')
  // console.log(props.options)
  // console.log('test')
  // console.log(Object.entries(props.options ? props.options : []).map((value) => value))

  return (
    <div className='radio-input'>
     <label className='text-input__label'>{props.title}</label>
      <div className='radio-input__options' id={props.label}>
        {Object.entries(props.options ? props.options : []).map(([key, value]) => (
          <div className='radio-input__options__option' key={key}>
            <input type="radio" id={value.value}
              value={value.value}
              { ...register(props.label) } />
            <label>{value.displayedText ? value.displayedText : headerCase(value.value)}</label>
            {'tooltip' in value && <Tooltip {...value.tooltip} />}
          </div>
        ))}
      </div>
      {props.errorMessage &&
        props.tooltip?.icon != '?' &&
        props.tooltip?.icon != undefined && (
          <ErrorMessage errorMessage={props.errorMessage} />
      )}
    </div>
  )

//   return (
//     <div className="text-input">
//       <label className='text-input__label'>{props.title}</label>
//       {'tooltip' in props && <Tooltip {...props.tooltip} />}
//       {props.type != 'textarea' ? (
//         <input
//           {...register(props.label)}
//           // onChange={(e) => {
//           //   onChange && onChange(e);
//           //   if (props.onChange) {
//           //     props.onChange(e);
//           //   }
//           // }}
//           {...otherProps}
//         />
//       ) : (
//         <textarea
//           placeholder={props.placeholder}
//           // onChange={(e) => {
//           //   onChange && onChange(e);
//           //   if (props.onChange) {
//           //     props.onChange(e);
//           //   }
//           // }}
//           {...register(props.label)}
//         />
//       )}
//       {props.errorMessage &&
//         props.tooltip?.icon != '?' &&
//         props.tooltip?.icon != undefined && (
//           <ErrorMessage errorMessage={props.errorMessage} />
//         )}
//     </div>
//   );
};

export default RadioInput;
