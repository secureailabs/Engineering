//@ts-nocheck
import React from 'react';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';
import stageNumberToString from '@utils/stageNumberToString';

import { TDigitalContractSuccessProps } from './DigitalContract.types';
import getPartnerOrg from '@utils/getPartnerOrg';
import { useForm, SubmitHandler } from 'react-hook-form';


const UpdateOrganization = ({ organizationData }: any) => {
    const { register, formState } = useForm({
        mode: 'onSubmit',
        defaultValues: organizationData,
      });
    return (
        <>
        <Card primaryText="">
          <div className="form-double">
            <FormFieldsRenderer
              register={register}
              formState={formState}
              fields={{
                OrganizationName: {
                  label: 'Organization Name',
                  placeholder: 'Organization Name',
                  type: 'text',
                },
                OrganizationAddress: {
                  label: 'Organization Address',
                  placeholder: 'Organization Address',
                  type: 'text',
                },
                PrimaryContactName: {
                  label: 'Primary Contact Name',
                  placeholder: 'Priamry Contact Job Title',
                  type: 'text',
                },
                PriamryContactPhoneNumber: {
                  label: 'Primary Contact Phone Number',
                  placeholder: 'Primary Contact Phone Number',
                  type: 'text',
                },
                SecondaryContactName: {
                  label: 'Secondary Contact Name',
                  placeholder: 'Secondary Contact Name',
                  type: 'text',
                },
                SecondaryContactJobTitle: {
                  label: 'Secondary Contact Job Title',
                  placeholder: 'Secondary Contact Job Title',
                  type: 'text',
                },

                SecondaryContactEmail: {
                  label: 'Secondary Contact Email',
                  placeholder: 'Secondary Contact Email',
                  type: 'text',
                },
                SecondaryContactPhoneNumber: {
                  label: 'Secondary Contact Phone Number',
                  placeholder: 'Number of Virtual CPUs',
                  type: 'text',
                },
                Description: {
                  label: 'Description',
                  placeholder: 'Description',
                  type: 'text',
                },
                Logo: {
                  label: 'Logo',
                  placeholder: 'Logo',
                  type: 'image',
                },
              }}
            />
          </div>
        </Card>
      </>
    )
};

export default UpdateOrganization;