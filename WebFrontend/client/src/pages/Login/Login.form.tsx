import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { Link } from 'react-router-dom';
import SingleFormViewBG from '@assets/SingleFormViewBG.png';
import { yupResolver } from '@hookform/resolvers/yup';

import LoginScheme from '../../formSchemes/LoginScheme';
import Logo from '@components/Logo';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TLoginFormProps } from './Login.types';
// import LoginScheme from 'src/formSchemes/LoginScheme';
import { IEmailAndPassword } from '@redux/user/user.typeDefs';

import { formData } from './Login.data';

import Button from '@components/Button';

const Login: React.FC<TLoginFormProps> = ({ signInReset, signInStart }) => {
  const { register, handleSubmit, formState, trigger } = useForm({
    resolver: yupResolver(LoginScheme),
    mode: 'onSubmit',
  });
  useEffect(() => {
    signInReset();
  }, []);
  const onSubmit: SubmitHandler<IEmailAndPassword> = (data) => {
    console.log(data);
    signInStart(data);
  };
  return (
    <div
      className="login"
      style={{
        backgroundImage: `url(${SingleFormViewBG})`,
        backgroundSize: 'cover',
      }}
    >
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
          <Logo />
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button
            type="submit"
            disabled={!formState.isDirty && formState.isValid}
          >
            Log In
          </Button>
          <a href='./signup' style={{color: 'black'}}>Signup</a>
        </>
      </Form>
    </div>
  );
};

export default Login;
