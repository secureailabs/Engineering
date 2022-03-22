import React, { useEffect } from 'react';

import { useParams } from 'react-router';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import { ConditionalRender } from '@components/ConditionalRender';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';

import Spinner from '@components/Spinner/SpinnerOnly.component';
import { TDigitalContractProps } from './DigitalContract.types';

import DigitalContractSuccess from './DigitalContract.success';

const DigitalContract: React.FC<TDigitalContractProps> = ({ getDigitalContractData, getDigitalContractState, getDigitalContractStart }) => {
  const {  id } = useParams();
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {},
  });

  useEffect(() => {
    getDigitalContractStart({ DigitalContractGuid: id});

  }, []);
  return (
    <>
      <StandardContent title="Digital Contract">
        <ConditionalRender
          //@ts-ignore
          state={getDigitalContractState}
          success={() => (
            <DigitalContractSuccess getDigitalContractData={getDigitalContractData} />
          )}
          //@ts-ignore
          failure={() => <></>}
          Loading={
            <>
              <Spinner />
            </>
          }
        >
          <></>
        </ConditionalRender>
      </StandardContent>
    </>
  );
};

export default DigitalContract;
