import React from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import UpdateAccessRightsScheme from './UpdateAccessRights.scheme';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TUpdateAccessRightsFormProps } from './UpdateAccessRights.types';
import { TPutUpdateAccessRightsStart } from '@redux/accountManager/accountManager.typeDefs';

import { formData } from './UpdateAccessRights.data';

import Button from '@components/Button';

const UpdateAccessRights: React.FC<TUpdateAccessRightsFormProps> = ({
  putUpdateAccessRightsReset,
  putUpdateAccessRightsStart,
  userData,
  UserGuid,
}) => {
  const { register, handleSubmit, formState, trigger } = useForm({
    resolver: yupResolver(UpdateAccessRightsScheme),
    mode: 'onSubmit',
  });

  const onSubmit: SubmitHandler<{
    AccessRights: TPutUpdateAccessRightsStart['AccessRights'];
  }> = (data) => {
    console.log(data);
    putUpdateAccessRightsStart({
      UserGuid: UserGuid,
      ...data,
    });
  };
  return (
    <div
      style={{
        maxWidth: '100rem',
        margin: '0 auto',
      }}
    >
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button type="submit" disabled={!formState.isValid}>
            Update AccessRights
          </Button>
        </>
      </Form>
    </div>
  );
};

export default UpdateAccessRights;
