import React from 'react';
import Tooltip from '@components/ToolTip';
import ErrorMessage from '@components/ErrorMessage';

import type { TTextAreaInputProps } from './TextAreaInput.types';

const TextAreaInput: React.FC<TTextAreaInputProps> = (props) => {
  // Make the input type password if needed

  // Extract the onChange from register so we can add something to it
  const { register, onChange, ...otherProps } = props;
      return (
      <div className="textarea-input" id={`${props.label}_inputdiv`}>
        <label className='text-input__label'>{props.title}</label>
        {'tooltip' in props && <Tooltip {...props.tooltip} />}
        <textarea
          placeholder={props.placeholder}
          // onChange={(e) => {
          //   onChange && onChange(e);
          //   if (props.onChange) {
          //     props.onChange(e);
          //   }
          // }}
          {...register(props.label)}
          autoComplete='off'
        />
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

export default TextAreaInput;
