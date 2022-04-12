import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TDeleteAccountFormProps } from './DeleteAccount.types';
import { TDeleteAccountManagerStart } from '@redux/accountManager/accountManager.typeDefs';

import { formData } from './DeleteAccount.data';

import Button from '@components/Button';

const ActivateDigitalContract: React.FC<TDeleteAccountFormProps> = ({
  deleteAccountManagerReset,
  deleteAccountManagerStart,
  UserGuid
}) => {
  useEffect(() => {
    deleteAccountManagerReset();
  }, []);
  const { register, handleSubmit, formState } = useForm({
    mode: 'onSubmit',
  });
  const onSubmit: SubmitHandler<TDeleteAccountManagerStart> = (
    data
  ) => {
    const newData = {
      UserGuid: UserGuid
    };
    deleteAccountManagerStart(newData);
  };
  return (
    <div className="deleteaccount">
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
        <div className='dcforminfo'>
          <div className='dcforminfo__title'>Close Account</div>
          <div className='dcforminfo__description'>
              Please confirm you want to close this account. If you do so, the user won't have access to the platform until you reopen their account.
          </div>
        </div>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button type="submit">Close Account</Button>
        </>
      </Form>
    </div>
  );
};

export default ActivateDigitalContract;
