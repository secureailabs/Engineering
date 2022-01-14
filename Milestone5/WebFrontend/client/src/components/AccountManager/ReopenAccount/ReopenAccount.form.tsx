import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TReopenAccountFormProps } from './ReopenAccount.types';
import { TDeleteAccountManagerStart } from '@redux/accountManager/accountManager.typeDefs';

import { formData } from './ReopenAccount.data';

import Button from '@components/Button';

const ActivateDigitalContract: React.FC<TReopenAccountFormProps> = ({
  putAccountManagerReset,
  putAccountManagerStart,
  UserGuid
}) => {
  useEffect(() => {
    putAccountManagerReset();
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

    putAccountManagerStart(newData);
  };
  return (
    <div className="reopenaccount">
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
        <div className='dcforminfo'>
          <div className='dcforminfo__title'>Reopen Account</div>
          <div className='dcforminfo__description'>
              Please confirm you want to reopen this account. If you do so, the user will have access to the platform until you close their account again.
          </div>
        </div>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button type="submit">Reopen Account</Button>
        </>
      </Form>
    </div>
  );
};

export default ActivateDigitalContract;
