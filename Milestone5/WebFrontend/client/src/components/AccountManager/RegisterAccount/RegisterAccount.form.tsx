import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TPostAccountManagerStart } from '@redux/accountManager/accountManager.typeDefs';

import { formData } from './RegisterAccount.data';

import Button from '@components/Button';

import { TRegisterAccountFormProps } from './RegisterAccount.types';

import RegisterAccountScheme from './RegisterAccount.scheme';

const RegisterAccountForm: React.FC<TRegisterAccountFormProps> = ({
  postAccountManagerStart,
  postAccountManagerReset,
  userData,
}) => {
  useEffect(() => {
    postAccountManagerReset();
  }, []);
  const { register, handleSubmit, formState, trigger, watch } = useForm({
    resolver: yupResolver(RegisterAccountScheme),
    mode: 'onSubmit',
    defaultValues: {
      Email: '',
      Password: '',
      PasswordConfirmation: '',
      // AccessRights: '',
      Name: '',
      Title: '',
      PhoneNumber: '',
    }
  });
  const onSubmit: SubmitHandler<TPostAccountManagerStart> = (data) => {
    const newData = {
      ...data,
      AccessRights: '1',
      OrganizationGuid: userData?.OrganizationGuid || '',
    };
    //@ts-ignore
    delete newData['PasswordConfirmation'];

    console.log(newData);
    postAccountManagerStart(newData);
  };

  console.log('RegisterAccount.form')

  return (
    <div className="registeraccount">
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
          <div className="dcforminfo">
            <div className="dcforminfo__title">Create New Account</div>
            <div className="dcforminfo__description">
              To create a new user, enter their credentials, their permissions
              and relevant information about them.
            </div>
          </div>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState, trigger)}
          />
          <Button type="submit">Create New Account</Button>
        </>
      </Form>
    </div>
  );
};

export default RegisterAccountForm;
