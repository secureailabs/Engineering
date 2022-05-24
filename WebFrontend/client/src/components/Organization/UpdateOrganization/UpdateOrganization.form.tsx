import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { Link } from 'react-router-dom';
import SingleFormViewBG from '@assets/SingleFormViewBG.png';
import { yupResolver } from '@hookform/resolvers/yup';

import UpdateOrganizationScheme from './UpdateOrganization.scheme';
import Logo from '@components/Logo';

import Form from '@components/Form';
import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TUpdateOrganizationFormProps } from './UpdateOrganization.types';
// import UpdateOrganizationScheme from 'src/formSchemes/UpdateOrganizationScheme';
import {
  TPutOrganizationStart,
  TGetOrganizationSuccess,
} from '@app/redux/organization/organization.typeDefs';

import { formData } from './UpdateOrganization.data';

import Button from '@components/Button';

const UpdateOrganization: React.FC<TUpdateOrganizationFormProps> = ({
  putOrganizationReset,
  putOrganizationStart,
  organizationData,
  userData,
}) => {
  const { register, handleSubmit, formState, trigger } = useForm({
    resolver: yupResolver(UpdateOrganizationScheme),
    mode: 'onChange',
    defaultValues: {
      ...organizationData,
    },
  });

  const onSubmit: SubmitHandler<TGetOrganizationSuccess> = (data) => {
    console.log(data);
    // console.log(userData?.OrganizationGuid)
    // console.log(userData?.OrganizationGuid.replace('{', '').replace('}', ''))
    putOrganizationStart({
      OrganizationGuid:
        userData?.OrganizationGuid || '',
      OrganizationInformation: data,
    });
  };
  return (
    <div
      className='settings_container'
    >
      <Form actualForm={true} onSubmit={handleSubmit(onSubmit)}>
        <>
          <FormFieldsRenderer
            formState={formState}
            register={register}
            fields={formData(formState)}
          />
          <Button type="submit" disabled={!(formState.isValid && formState.isDirty)}>
            Update Organization
          </Button>
        </>
      </Form>
    </div>
  );
};

export default UpdateOrganization;
