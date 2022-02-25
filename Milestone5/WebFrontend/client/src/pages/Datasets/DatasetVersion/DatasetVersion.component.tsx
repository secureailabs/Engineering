import React, { useEffect } from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import { useParams } from 'react-router-dom';

import { ConditionalRender } from '@components/ConditionalRender';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';

import Spinner from '@components/Spinner/SpinnerOnly.component';
import { TDatasetVersionProps } from './DatasetVersion.types';

import DatasetVersionSuccess from './DatasetVersion.success';

const DatasetVersion: React.FC<TDatasetVersionProps> = ({
  getDatasetVersionReset,
  getDatasetVersionStart,
  getDatasetVersionState,
  getDatasetVersionData,
}) => {
  const params = useParams();
  useEffect(() => {
    getDatasetVersionReset();
    getDatasetVersionStart({
      Version: params.version,
      DatasetGuid: params.id,
    });
  }, []);
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {},
  });

  return (
    <>
      <ConditionalRender
        //@ts-ignore
        state={getDatasetVersionState}
        success={() => (
          <DatasetVersionSuccess
            getDatasetVersionData={getDatasetVersionData}
          />
        )}
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

export default DatasetVersion;
