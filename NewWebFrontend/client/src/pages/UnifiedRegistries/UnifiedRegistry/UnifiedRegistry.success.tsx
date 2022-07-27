import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import Card from '@secureailabs/web-ui/components/Card';
import { HiOutlineExternalLink, HiPencil } from 'react-icons/hi';
import { ImPencil } from 'react-icons/im';
import Text from '@secureailabs/web-ui/components/Text';
import Heading from '@secureailabs/web-ui/components/Heading';
import Button from '@secureailabs/web-ui/components/Button';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';

import DatasetsSuccess from '@pages/Datasets/Datasets/Datasets.success';

import PatientSummary from '@components/PatientSummary';

import Margin from '@secureailabs/web-ui/components/Margin';

import type { TUnifiedRegistrySuccessProps } from './UnifiedRegistry.types';
import { useParams } from 'react-router';

const UnifiedRegistrySuccess: React.FC<TUnifiedRegistrySuccessProps> = ({
  getUnifiedRegistryData,
}) => {

  const { id } = useParams()
  const index = id ? parseInt(id.slice(-1)) - 1 : 0
  const owner = index == 0

  const [editMode, setEditMode] = useState(false);

  const [providersOpen, setProvidersOpen] = useState(false);
  const [usersOpen, setUsersOpen] = useState(false);

  const { register, formState, reset } = useForm({
    mode: 'onSubmit',
    defaultValues: getUnifiedRegistryData,
  });

  useEffect(() => reset(getUnifiedRegistryData), [getUnifiedRegistryData])

  return !editMode ?
    <>
      {owner && <div className='edit-button-container'>
        {/* @ts-ignore */}
        <Button onClick={() => setEditMode(true)} button_type='secondary' height='5rem' full={false}><div className='edit-button-container__button-div'><ImPencil size={12} /><p>Edit Info</p></div></Button>
      </div>
      }
      <Card primaryText="">
        <div className="unified-registry-card">
          <div className="unified-registry-card__header">
            <img src={getUnifiedRegistryData.Image} />
            <div className='unified-registry-card__title-and-org'>
              <p className="unified-registry-card__title">{getUnifiedRegistryData.Name}</p>
              <div>
                <p className="unified-registry-card__owner">Owned by {getUnifiedRegistryData.owner_org} - {getUnifiedRegistryData.owner_name} - {getUnifiedRegistryData.owner_email}</p>
              </div>
            </div>
          </div>
          <div className="unified-registry-card__body">
            <p className="unified-registry-card__description">
              {getUnifiedRegistryData.Description}
            </p>
            <div className='unified-registry-card__moreinfo'>
              <a className="unified-registry-card__link">
                Data Model Spec
                <HiOutlineExternalLink />
              </a>
              <div></div>
              <a className="unified-registry-card__link" href={getUnifiedRegistryData.owner_org_url} target="_blank" rel="noopener noreferrer">Request Access</a>
              <p>Registry creation on 1 Jan 2022</p>
              <p>.</p>
              <p>Registry Last updated on 1 Jan 2022</p>
            </div>
            <Margin size={5} />
          </div>
        </div>
      </Card>
      <Margin size={5} />

      <Heading fontWeight='500'>Members</Heading>

      <Margin size={5} />

      <Card primaryText='Data Providers' secondaryText={providersOpen ? '\u25b2' : '\u25bc'} secondaryTextColor='black' secondaryTextOnClick={() => setProvidersOpen(!providersOpen)}>{providersOpen ?
        <div className='unified-registry-section'>
          <div className='unified-registry-section__rows--providers'>
            {// @ts-ignore
              getUnifiedRegistryData.members_data?.providers?.map((elem) => (elem.buttonText != 'Revoke Invite' || owner) && <div className='unified-registry-section__row'><Text fontWeight='500'>{elem.name}</Text><Text color='primary'>{(elem.buttonText == 'Revoke Invite') ? 'Invite Pending' : ''}</Text>{owner && <Button button_type='secondary' height='3.6rem' padded={false} full onClick={() => { }}>{elem.buttonText}</Button>}</div>)}
          </div>
          {owner && <div className='unified-registry-section__bottom-button-container'><Button button_type='secondary' height='3.6rem' full onClick={() => { }}>+ Invite New Data Provider</Button></div>}
        </div>
        : undefined
      }</Card>

      <Margin size={5} />

      <Card primaryText='Data Users' secondaryText={usersOpen ? '\u25b2' : '\u25bc'} secondaryTextColor='black' secondaryTextOnClick={() => setUsersOpen(!usersOpen)}>{usersOpen ?
        <div className='unified-registry-section__rows--users'>
          {/* @ts-ignore */}
          {getUnifiedRegistryData.members_data?.users.map((elem) => <div className='unified-registry-section__row'><Text fontWeight='500'>{elem.name}</Text><Text className='access-details-text' color='primary'>Dataset Access Details</Text></div>)}
          {owner && <div className='unified-registry-section__bottom-button-container'><Button button_type='secondary' height='3.6rem' full onClick={() => { }}>+ Add New Data Users</Button></div>}
        </div>
        : undefined
      }</Card>

      <Margin size={5} />

      <PatientSummary containerHeight={false} />

      <Margin size={10} />

      <DatasetsSuccess
        // @ts-ignore
        getAllDatasetsData={getUnifiedRegistryData.Datasets}
      />
    </>
    :
    <>
      <Card primaryText=''>
        <div className="unified-registry-card">
          <div className="unified-registry-card__header">
            <img src={getUnifiedRegistryData.Image} />
            <div className='unified-registry-card__header__image-edit-icon-div'><label htmlFor='image-upload'><ImPencil color='white' size={15} /></label><input type='file' id='image-upload' /></div>
          </div>
          <div className='registry-modification-form'>
            <FormFieldsRenderer formState={formState} register={register} fields={{ owner_org: { label: 'Organization Name', placeholder: getUnifiedRegistryData.owner_name || 'Organization Name', type: 'text' }, Description: { label: 'Description', placeholder: getUnifiedRegistryData.Description || 'Description', 'type': 'textarea' }, dataModelSpec: { label: 'Data Model Specifications', placeholder: 'Enter Url', type: 'text' }, owner_org_url: { label: 'Request Access', placeholder: 'Enter Url', type: 'text' } }} />
          </div>
        </div>
      </Card>
      <Margin size={5} />
      <div className='unified-registry-edit-page-buttons-div'>
        <Button button_type='primary' full onClick={() => setEditMode(false)}>Save Changes</Button>
        <Button button_type='secondary' full onClick={() => setEditMode(false)}>Reset Changes</Button>
      </div>

    </>;
};

export default UnifiedRegistrySuccess;
