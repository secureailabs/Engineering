import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { Link } from 'react-router-dom';
import SingleFormViewBG from '@assets/SingleFormViewBG.png';
import { yupResolver } from '@hookform/resolvers/yup';

import UpdateUserScheme from './UpdateUser.scheme';
import Logo from '@components/Logo';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TUpdateUserFormProps } from './UpdateUser.types';
// import UpdateUserScheme from 'src/formSchemes/UpdateUserScheme';
import {
  TPutUpdateUserStart,
  TPutUpdateUserSuccess,
} from '@redux/accountManager/accountManager.typeDefs';

import { formData } from './UpdateUser.data';

import Button from '@components/Button';
import { GrIndicator } from 'react-icons/gr';

const UpdateUser: React.FC<TUpdateUserFormProps> = ({
  putUpdateUserReset,
  putUpdateUserStart,
  userData,
}) => {
  const { register, handleSubmit, formState, trigger } = useForm({
    resolver: yupResolver(UpdateUserScheme),
    mode: 'onChange',
    defaultValues: {
      Name: userData?.Username,
      Title: userData?.Title,
      PhoneNumber: userData?.PhoneNumber,
    },
  });

  const onSubmit: SubmitHandler<{
    Name: string;
    Title: string;
    PhoneNumber: string;
  }> = (data) => {
    console.log(data);
    putUpdateUserStart({
      UserGuid: userData?.UserGuid || '',
      UserInformation: {
        ...data,
      },
    });
  };
  return (
    <div
    className="settings_container"
    >
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button type="submit" disabled={!(formState.isValid && formState.isDirty)}>
            Update User
          </Button>
        </>
      </Form>
    </div>
  );
};

export default UpdateUser;
