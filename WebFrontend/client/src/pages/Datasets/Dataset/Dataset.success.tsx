import React from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';

import { TDatasetSuccessProps } from './Dataset.types';

import Button from '@secureailabs/web-ui/components/Button';
import Table from '@components/Table';

import RequestDataAccessForm from '@components/DigitalContractForms/RequestDataAccessForm';

const DatasetSuccess: React.FC<TDatasetSuccessProps> = ({ getDatasetData, userData }) => {
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {
      ...getDatasetData,
      DataOwner: getDatasetData.organization.name,
      publish_date: new Date(
        getDatasetData?.publish_date * 1000
      ).toLocaleDateString('en-US'),
      NumberOfVersions: 1,
    },
  });

  const columns = React.useMemo(
    () => [
      {
        Header: 'Version',
        accessor: 'version',
        width: 300,
      },

      {
        Header: 'Publish Date',
        accessor: 'publish_date',
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

  const [modalIsOpen, setIsOpen] = React.useState(false);

  return (
    <div>
      <StandardContent back={true} title={getDatasetData?.name}>
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
                publish_date: {},
                DataOwner: {},
                keywords: {},
                description: {},
              }}
            />
          </div>
        </Card>
      </StandardContent>
      <StandardContent title={getDatasetData?.name}>
        <Table
          base_url={`/dashboard/datasets/${getDatasetData?.id}`}
          id_accessor="key"
          columns={columns}
          data={[]}
        />
      </StandardContent>
      <div
        style={{
          width: '20rem',
          marginLeft: '5rem',
        }}
      >
        {
          getDatasetData.organization.id != userData?.organization.id && <Button full={false} button_type="primary" onClick={() => { setIsOpen(true) }}>
            Request Access
          </Button>
        }
      </div>
      {modalIsOpen &&
        <RequestDataAccessForm setIsOpen={setIsOpen} DataOwnerOrganization={getDatasetData.organization.id} DatasetGuid={getDatasetData.id} />
      }
    </div>
  );
};

export default DatasetSuccess;
