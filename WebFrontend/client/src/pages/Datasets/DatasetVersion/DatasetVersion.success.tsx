import React from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';
import stageNumberToString from '@utils/stageNumberToString';

import { TDatasetVersionSuccessProps } from './DatasetVersion.types';

import Margin from '@secureailabs/web-ui/components/Margin';

import Button from '@secureailabs/web-ui/components/Button';

import Table from '@components/Table';

const DatasetSuccess: React.FC<TDatasetVersionSuccessProps> = ({
  getDatasetVersionData,
  getDatasetData,
}) => {
  console.log(getDatasetData);
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {
      ...getDatasetVersionData,
      NumberOfVersions: Object.keys(getDatasetData?.Versions || {})
        .length,
      PublishDate: new Date(
        getDatasetVersionData?.PublishDate
      ).toLocaleDateString('en-US'),
    },
  });

  return (
    <StandardContent
      back={true}
      title={getDatasetVersionData?.DatasetName}
    >
      <>
        <Card primaryText="">
          <div className="form-double">
            <FormFieldsRenderer
              register={register}
              formState={formState}
              fields={{
                NumberOfVersions: {
                  label: 'No. of Versions',
                  placeholder: 'No. of Versions',
                  type: 'text',
                },
                PublishDate: {},
                DataOwner: {},
                Keywords: {},
                Description: {},
                Comments: {},
              }}
            />
          </div>
        </Card>
        <Margin size={8} />
        <Button full={false} button_type="primary">
          Request Access
        </Button>
      </>
    </StandardContent>
  );
};

export default DatasetSuccess;
