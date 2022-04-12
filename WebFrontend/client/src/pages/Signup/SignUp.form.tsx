import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
// import { Link } from 'react-router-dom';

import SingleFormViewBG from '@assets/SingleFormViewBG.png';
// import Logo from '@components/Logo/Logo';
import MultiPartForm from '@components/MultiPartForm';
import SignupScheme from '../../formSchemes/SignupScheme';
import { yupResolver } from '@hookform/resolvers/yup';

import { formData } from './SignUp.data';

import { TSignUpFormProps } from './SignUp.types';

// import { pascalCase } from 'change-case';

// const testThing = () => {
//   const test = {
//     email: 'adam@secureailabs.com',
//     password: '',
//     passwordConfirmation: '',
//     name: 'Adam Jasniewicz',
//     phoneNumber: '1234567890',
//     title: 'Mr',
//     organizationName: 'Test-Org',
//     organizationAddress: '123 Test Land',
//     primaryContactName: 'Vincent',
//     primaryContactTitle: 'Mr',
//     primaryContactEmail: 'vincent@secureailabs.com',
//     primaryContactPhoneNumber: '1234567890',
//     secondaryContactName: 'Bob',
//     secondaryContactTitle: 'Mr',
//     secondaryContactEmail: 'bob@example.com',
//     secondaryContactPhoneNumber: '12345678990',
//   };
//   let newTest: Record<string, string> = {};
//   console.log(
//     Object.entries(test).map(([key, value]) => {
//       newTest[pascalCase(key)] = value;
//     })
//   );
//   console.log(newTest);
// };

export type SignUpFormValues = {
  email: string;
  password: string;
  passwordConfirmation: string;
  name: string;
  phoneNumber: string;
  title: string;
  organizationName: string;
  primaryContactName: string;
  primaryContactTitle: string;
  primaryContactEmail: string;
  primaryContactPhoneNumber: string;
  secondaryContactName: string;
  secondaryContactTitle: string;
  secondaryContactEmail: string;
  secondaryContactPhoneNumber: string;
  organizationAddressLine1: string;
  organizationAddressLine2?:string;
  organizationAddressCity: string;
  organizationAddressState: string;
  organizationAddressZip: string;
  organizationAddressCountry: string;
};

const SignUpForm: React.FC<TSignUpFormProps> = ({
  signUpStart,
  signUpReset,
}) => {
  // testThing();

  const { register, trigger, handleSubmit, watch, formState, getValues } = useForm({
    resolver: yupResolver(SignupScheme),
    // Needed for dirtyFields to work (to know if the use typed in something)
    defaultValues: {
      // email: 'adam@secureailabs.com',
      email: '',
      password: '',
      passwordConfirmation: '',
      // name: 'Adam Jasniewicz',
      name: '',
      // phoneNumber: '1234567890',
      phoneNumber: '',
      // title: 'Mr',
      title: '',
      // organizationName: 'Test-Org',
      organizationName: '',
      // primaryContactName: 'Vincent',
      primaryContactName: '',
      // primaryContactTitle: 'Mr',
      primaryContactTitle: '',
      // primaryContactEmail: 'vincent@secureailabs.com',
      primaryContactEmail: '',
      // primaryContactPhoneNumber: '1234567890',
      primaryContactPhoneNumber: '',
      // secondaryContactName: 'Bob',
      secondaryContactName: '',
      // secondaryContactTitle: 'Mr',
      secondaryContactTitle: '',
      // secondaryContactEmail: 'bob@example.com',
      secondaryContactEmail: '',
      // secondaryContactPhoneNumber: '12345678990',
      secondaryContactPhoneNumber: '',
      // organizationAddress: '123 Test Land',
      // organizationAddress: '',
      organizationAddressLine1: '',
      organizationAddressLine2: '',
      organizationAddressCity: '',
      organizationAddressState: '',
      organizationAddressZip: '',
      organizationAddressCountry: '',
    },
    mode: 'onChange',
  });
  useEffect(() => {
    signUpReset();
    trigger();
  }, []);
  const onSubmit: SubmitHandler<SignUpFormValues> = (data) => {
    // console.log('HELLO');
    // console.log(data);
    signUpStart({
      organizationName: data.organizationName,
      email: data.email,
      password: data.password,
      name: data.name,
      phoneNumber: data.phoneNumber,
      title: data.title,
      primaryContactName: data.primaryContactName,
      primaryContactTitle: data.primaryContactTitle,
      primaryContactEmail: data.primaryContactEmail,
      primaryContactPhoneNumber: data.primaryContactPhoneNumber,
      secondaryContactName: data.secondaryContactName,
      secondaryContactTitle: data.secondaryContactTitle,
      secondaryContactEmail: data.secondaryContactEmail,
      secondaryContactPhoneNumber: data.secondaryContactPhoneNumber,
      organizationAddress: `${data.organizationAddressLine1}, 
        ${data.organizationAddressLine2}, 
        ${data.organizationAddressCity}, 
        ${data.organizationAddressState}, 
        ${data.organizationAddressCountry} 
        (${data.organizationAddressZip})`
    });
  };
  const watchPrimaryContactName = watch('primaryContactName')
  console.log(watchPrimaryContactName)
  return (
    <div
      className="signup"
      style={{ backgroundImage: `url(${SingleFormViewBG})` }}
    >
      <form onSubmit={handleSubmit(onSubmit)}>
        <MultiPartForm
          onSubmit={() => handleSubmit(onSubmit)}
          formState={formState}
          register={register}
          forms={formData(formState, trigger)}
        >
        </MultiPartForm>
      </form>
    </div>
  );
};

export default SignUpForm;
