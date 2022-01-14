import React from 'react';

import { TFormFieldsRenderer } from './FormFieldsRenderer.types';

import TextInput from '@components/Inputs/TextInput';
import TextAreaInput from '@components/Inputs/TextAreaInput';
import RadioInput from '@components/Inputs/RadioInput';
import SelectInput from '@components/Inputs/SelectInput';

import { headerCase } from 'change-case';

const FormRenderer: React.FC<TFormFieldsRenderer> = ({
  fields,
  register,
  formState,
  description
}) => {
  return (
    <>
    {(description && description != '') &&
    <div className='formsfieldsdescription'>
      {description}
    </div>
  }
      {Object.entries(fields).map(([key, value], index) => {
        switch (value.type) {
          case 'textarea': {
            return (
            <TextAreaInput 
              {...register(key)}
              key={index}
              placeholder={value.title ? value.title: headerCase(key, { delimiter: ' ' })}
              title={value.title ? value.title:headerCase(key, { delimiter: ' ' })}
              label={key}
              register={register}
              tooltip={value.tooltip}
              // type={value.type}
              errorMessage={formState.errors[key]?.message}
            />)
            break;
          }
          case 'radio': {
            return (
              <RadioInput 
                {...register(key)}
                key={index}
                placeholder={value.title ? value.title: headerCase(key, { delimiter: ' ' })}
                title={value.title ? value.title:headerCase(key, { delimiter: ' ' })}
                label={key}
                register={register}
                tooltip={value.tooltip}
                // type={value.type}
                options={value.options || []}
                errorMessage={formState.errors[key]?.message}
              />)
              break;
          }
          case 'select': {
            return (
              <SelectInput 
                {...register(key)}
                key={index}
                title={value.title ? value.title:headerCase(key, { delimiter: ' ' })}
                label={key}
                register={register}
                tooltip={value.tooltip}
                // type={value.type}
                options={value.options || []}
                errorMessage={formState.errors[key]?.message}
              />)
              break;
          }
          case 'text':
          case 'password':
          case 'number':
            return (
              <TextInput
                {...register(key)}
                key={index}
                placeholder={value.title ? value.title: headerCase(key, { delimiter: ' ' })}
                title={value.title ? value.title:headerCase(key, { delimiter: ' ' })}
                label={key}
                register={register}
                tooltip={value.tooltip}
                type={value.type}
                errorMessage={formState.errors[key]?.message}
                // onChange={value?.onChange}
              />
            );
        }
      })}
    </>
  );
};

export default FormRenderer;
