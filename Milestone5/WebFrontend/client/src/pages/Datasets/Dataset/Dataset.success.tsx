import React from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';
import stageNumberToString from '@utils/stageNumberToString';

import { TDatasetSuccessProps } from './Dataset.types';
import getPartnerOrg from '@utils/getPartnerOrg';

import Button from '@secureailabs/web-ui/components/Button';

import Table from '@components/Table';

const DatasetSuccess: React.FC<TDatasetSuccessProps> = ({ getDatasetData }) => {
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {
      ...getDatasetData.Dataset,
      NumberOfVersions: Object.keys(getDatasetData?.Dataset?.Versions || {})
        .length,
      PublishDate: new Date(
        getDatasetData?.Dataset?.PublishDate
      ).toLocaleDateString('en-US'),
    },
  });

  let columns = React.useMemo(
    () => [
      {
        Header: 'Version',
        accessor: 'Version',
        width: 300,
      },

      {
        Header: 'Publish Date',
        accessor: 'PublishDate',
        width: 300,
      },

      {
        Header: 'No. of Patients',
        accessor: 'NumberOfPatients',

        width: 200,
      },
      {
        Header: 'Comments',
        accessor: 'Comments',
        width: 200,
      },
    ],
    []
  );

  const parsedData = Object.entries(
    getDatasetData?.Dataset?.Versions || {}
  ).map(([key, value]) => {
    return {
      key,
      ...value,
      PublishDate: new Date(value.PublishDate * 1000).toLocaleDateString(
        'en-US',
        {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        }
      ),
    };
  });
  return (
    <div>
      <StandardContent title={getDatasetData?.Dataset?.DatasetName}>
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
              }}
            />
          </div>
        </Card>
      </StandardContent>
      <StandardContent title={getDatasetData?.Dataset?.DatasetName}>
        <Table
          base_url={`/dashboard/datasets/${getDatasetData?.Dataset?.DatasetGuid}`}
          id_accessor="key"
          columns={columns}
          data={parsedData}
        />
      </StandardContent>
      <div
        style={{
          width: '20rem',
          marginLeft: '5rem',
        }}
      >
        <Button full={false} button_type="primary">
          Request Access
        </Button>
      </div>
    </div>
  );
};

export default DatasetSuccess;
