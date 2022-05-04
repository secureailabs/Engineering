import React from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';
import stageNumberToString from '@utils/stageNumberToString';

import { TDatasetSuccessProps } from './Dataset.types';
import getPartnerOrg from '@utils/getPartnerOrg';

import Button from '@secureailabs/web-ui/components/Button';
import Modal from '@secureailabs/web-ui/components/Modal';
import Table from '@components/Table';

const DatasetSuccess: React.FC<TDatasetSuccessProps> = ({ getDatasetData }) => {
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {
      ...getDatasetData,
      DataOwner: getDatasetData.OrganizationName,
      NumberOfVersions: Object.keys(getDatasetData?.Versions || {})
        .length,
      PublishDate: new Date(
        getDatasetData?.PublishDate
      ).toLocaleDateString('en-US'),
    },
  });

  const columns = React.useMemo(
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
    getDatasetData?.Versions || {}
  ).map(([key, value]) => {
    return {
      key,
      ...value,
      DataOwner: value.OrganizationName,
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

  const [modalIsOpen, setIsOpen] = React.useState(false);

  return (
    <div>
      <StandardContent back={true} title={getDatasetData?.DatasetName}>
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
      <StandardContent title={getDatasetData?.DatasetName}>
        <Table
          base_url={`/dashboard/datasets/${getDatasetData?.DatasetGuid}`}
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
        <Button full={false} button_type="primary" onClick={() => { setIsOpen(true) }}>
          Request Access
        </Button>
      </div>
      {modalIsOpen && 
        <Modal
          title='Request Dataset Access'
          description="To request access to this dataset, enter the title of your research, for how long you'll need access to the data, and any comments regarding your request."
          close={() => { setIsOpen(false) }}
        >
          <form className="form">
            <FormFieldsRenderer
              register={register}
              button_text="Request Data Access"
              formState={formState}
              fields={{
                title: {
                  label: 'Title',
                  placeholder: 'Title',
                  type: 'text',
                },
                access_duration: {
                  label: 'Access Duration (days)',
                  placeholder: 'Access Duration (days)',
                  type: 'text',
                },
                comments: {
                  label: 'Request Comments',
                  placeholder: 'Comments',
                  type: 'textarea',
                },
              }}
            />
          </form>
        </Modal>
      }
    </div>
  );
};

export default DatasetSuccess;
