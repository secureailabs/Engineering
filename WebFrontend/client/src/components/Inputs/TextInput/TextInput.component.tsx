import React from 'react';
import Tooltip from '@components/ToolTip';
import ErrorMessage from '@components/ErrorMessage';

import type { TTextInputProps } from './TextInput.types';

const TextInput: React.FC<TTextInputProps> = (props) => {
  // Make the input type password if needed

  // Extract the onChange from register so we can add something to it
  const { register, onChange, ...otherProps } = props;
  // console.log(props.title)
      
  return (
    <div className="text-input" id={`${props.label}_inputdiv`}>
      <label className="text-input__label">{props.title}</label>
      {'tooltip' in props && <Tooltip {...props.tooltip} />}
      <input
        {...register(props.label)}
            // onChange={(e) => {
            //   onChange && onChange(e);
            //   if (props.onChange) {
            //     props.onChange(e);
            //   }
            // }}
        {...otherProps}
        autoComplete='off'
        readOnly
        onFocus={(e) => {
          const input:any = e.target
          if (input.hasAttribute('readonly')) {
            input.removeAttribute('readonly');
            
            // show safari virtual keyboard
            input.blur();
            input.focus(); 
          }
          }
        }
      />
      {props.errorMessage &&
        props.tooltip?.icon != '?' &&
        props.tooltip?.icon != undefined && (
          <ErrorMessage errorMessage={props.errorMessage} />
      )}
    </div>
      )
};

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

export default TextInput;
