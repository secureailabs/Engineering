import React, { useState } from 'react';
import { Link } from 'react-router-dom';

import { TMultiPartForm } from './MultiPartForm.types';

import FormFieldsRenderer from '@components/FormFieldsRenderer';
import Logo from '@components/Logo';

import _ from 'lodash';

import Form from '@components/Form';

import Button from '@components/Button';


const checkIfCanContinue = (
  errors: TMultiPartForm['formState']['errors'],
  fields: TMultiPartForm['forms'][0][1],
  dirtyFields: TMultiPartForm['formState']['dirtyFields']
) => {
  // console.log('running check if can continue');
  // console.log(Object.keys(errors).length == 0);
  // console.log(_.isEmpty(_.xor(Object.keys(fields), Object.keys(dirtyFields))));
  // console.log(Object.keys(fields));
  // console.log(Object.keys(dirtyFields));
  // console.log('can continue?');
  // console.log(
    // Object.keys(errors).length == 0 &&
      // Object.keys(fields).every((val) => Object.keys(dirtyFields).includes(val)) &&
      Object.keys(errors).every((val) => !Object.keys(fields).includes(val))
  // );
  // const sim = _.intersectionWith(
  //   Object.keys(fields),
  //   Object.keys(errors),
  //   _.isEqual
  // );
  // return sim.length != 0;
  // console.log('errors: ')
  // console.log(errors)
  return (
    // Object.keys(errors).length == 0 &&
    // Object.keys(fields).every((val) => Object.keys(dirtyFields).includes(val)) &&
    Object.keys(errors).every((val) => !Object.keys(fields).includes(val))
  );
};

const MultiPartForm: React.FC<TMultiPartForm> = ({
  forms,
  formState,
  register,
}) => {
  const [part, updatePart] = useState<number>(0);
  // console.log('drity')
  // console.log(formState.touchedFields)

  return (
    <Form>
      <>
      <Logo />
        {forms.map((form, index) => {
          if (index === part) {
            return (
              <FormFieldsRenderer
                register={register}
                formState={formState}
                fields={form[1]}
                description={form[0]}
              />
            );
          } else {
            return (
              <div className="hidden" style={{ display: 'none' }}>
                <FormFieldsRenderer
                  register={register}
                  formState={formState}
                  fields={form[1]}
                  description={form[0]}
                />
              </div>
            );
          }
        })}

        {part > 0 && (
          <div className='gobackbuttoncontainer'>
            <Button
            key="go back"
            type="button"
            onClick={() => {
              updatePart(part - 1);
            }}
          >
            Go back
          </Button>
          </div>
        )}
        {part !== forms.length - 1 ? (
          <button
            type="button"
            onClick={() => {
              if (
                checkIfCanContinue(
                  formState.errors,
                  forms[part][1],
                  formState.dirtyFields
                )
              ) {
                updatePart(part + 1);
              }
            }}
            disabled={
              !checkIfCanContinue(
                formState.errors,
                forms[part][1],
                formState.dirtyFields
              )
            }
          >
            Continue
          </button>
        ) : (
          <button
            key="signup"
            type="submit"
            disabled={
              !checkIfCanContinue(
                formState.errors,
                forms[part][1],
                formState.dirtyFields
              )
            }>
            Signup
          </button>
        )}
      </>
    </Form>
  );
};

export default MultiPartForm;
