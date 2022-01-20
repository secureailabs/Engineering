import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import UpdatePasswordScheme from './UpdatePassword.scheme';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TUpdatePasswordFormProps } from './UpdatePassword.types';
import {
  TPutUpdatePasswordStart,
  TPutUpdatePasswordSuccess,
} from '@redux/accountManager/accountManager.typeDefs';

import { formData } from './UpdatePassword.data';

import Button from '@components/Button';

const UpdatePassword: React.FC<TUpdatePasswordFormProps> = ({
  putUpdatePasswordReset,
  putUpdatePasswordStart,
  userData,
}) => {
  const { register, handleSubmit, formState, trigger } = useForm({
    resolver: yupResolver(UpdatePasswordScheme),
    mode: 'onChange',
    defaultValues: {
      CurrentPassword: '',
      NewPassword: '',
      ConfirmNewPassword: ''
    }
  });

  const onSubmit: SubmitHandler<TPutUpdatePasswordStart> = (data) => {
    console.log(data);
    putUpdatePasswordStart({
      Email: 'upt@mghl.com',
      CurrentPassword: data.CurrentPassword,
      NewPassword: data.NewPassword,
    });
  };

  return (
    <div
        className="settings_container"
        style={{
          marginTop: '5rem',
        }}
    >
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState, trigger)}
          />
          <Button type="submit" disabled={!formState.isValid}>
            Update Password
          </Button>
        </>
      </Form>
    </div>
  );
};

export default UpdatePassword;
