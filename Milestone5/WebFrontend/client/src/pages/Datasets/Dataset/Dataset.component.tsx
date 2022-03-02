import React, { useEffect } from 'react';

import { useParams } from 'react-router-dom';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import { ConditionalRender } from '@components/ConditionalRender';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';

import Spinner from '@components/Spinner/SpinnerOnly.component';
import { TDatasetProps } from './Dataset.types';

import DatasetSuccess from './Dataset.success';

const Dataset: React.FC<TDatasetProps> = ({
  getDatasetReset,
  getDatasetStart,
  getDatasetState,
  getDatasetData,
}) => {
  const params = useParams();
  useEffect(() => {
    getDatasetReset();
    //@ts-ignore
    getDatasetStart({ DatasetGuid: params.id });
  }, []);
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {},
  });

  return (
    <>
      <ConditionalRender
        //@ts-ignore
        state={getDatasetState}
        success={() => <DatasetSuccess getDatasetData={getDatasetData} />}
        //@ts-ignore
        failure={<>Failure</>}
        Loading={
          <>
            <Spinner />
          </>
        }
      >
        <></>
      </ConditionalRender>
    </>
  );
};

export default Dataset;
