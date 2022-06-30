import React, { useState } from 'react';
import Card from '@secureailabs/web-ui/components/Card';
import { HiOutlineExternalLink } from 'react-icons/hi';
import Text from '@secureailabs/web-ui/components/Text';
import Heading from '@secureailabs/web-ui/components/Heading';

import DatasetsSuccess from '@pages/Datasets/Datasets/Datasets.success';

import PatientSummary from '@components/PatientSummary';

import Margin from '@secureailabs/web-ui/components/Margin';

import type { TUnifiedRegistrySuccessProps } from './UnifiedRegistry.types';
import { useParams } from 'react-router';

const UnifiedRegistrySuccess: React.FC<TUnifiedRegistrySuccessProps> = ({
  getUnifiedRegistryData,
}) => {

  // const providersColumns = [
  //   {
  //     Header: '',
  //     accessor: 'name',
  //     width: 100
  //   },
  //   {
  //     Header: '',
  //     accessor: 'invite',
  //     Cell: ({ value }) => value ? <Text color='primary'>Invite Pending</Text> : <></>,
  //     width: 100
  //   },
  //   {
  //     Header: '',
  //     accessor: 'button_message',
  //     Cell: () => <Button button_type='secondary' full={false}>Render</Button>,
  //     width: 100
  //   }
  // ]

  // const providersData = [
  //   {
  //     name: 'Mayo',
  //     invite: false
  //   },
  //   {
  //     name: 'Vanderbuilt',
  //     invite: true
  //   }
  // ]

  // const usersColumns = [
  //   {
  //     Header: '',
  //     accessor: 'name',
  //     width: 100
  //   },
  //   {
  //     Header: '',
  //     accessor: 'name',
  //     Cell: () => <Text color='primary'>Data Access Details</Text>
  //   }
  // ]

  // const usersData = [
  //   {
  //     name: 'Pfizer'
  //   },
  //   {
  //     name: 'VUMC'
  //   }
  // ]

  const membersData = [['Mayo', 'Vanderbilt', 'Pfizer', 'VUMC'], ['Mercy General Hospital', 'Cornell', 'GSK', 'NewYork-Presbyterian Hospital']]

  const { id } = useParams()

  const [providersOpen, setProvidersOpen] = useState(false);
  const [usersOpen, setUsersOpen] = useState(false);

  return (
    <>
      <Card primaryText="">
        <div className="unified-registry-card">
          <div className="unified-registry-card__header">
            <img src={getUnifiedRegistryData.Image} />
            <div>
              <p className="unified-registry-card__title">{getUnifiedRegistryData.Name}</p>
              <div>
                <p className="unified-registry-card__owner">({getUnifiedRegistryData.owner_name} @ {getUnifiedRegistryData.owner_org})</p>
                <p className="unified-registry-card__access">Request Access</p>
              </div>
            </div>
          </div>
          <div className="unified-registry-card__body">
            <p className="unified-registry-card__description">
              {getUnifiedRegistryData.Description}
            </p>
            <p className="unified-registry-card__link">
              Data Model Spec
              <HiOutlineExternalLink />
            </p>
            <div className="unified-registry-card__dates">
              <p>Registry creation on 1 Jan 2022</p>
              <p>.</p>
              <p>Registry Last updated on 1 Jan 2022</p>
            </div>
            <Margin size={10} />
          </div>
        </div>
      </Card>
      <Margin size={5} />

      <Heading fontWeight='500'>Members</Heading>

      <Margin size={5} />

      <Card primaryText='Data Providers' secondaryText={providersOpen ? '\u25b2' : '\u25bc'} secondaryTextColor='black'  secondaryTextOnClick={() => setProvidersOpen(!providersOpen)}>{providersOpen ?
        // <Table columns={providersColumns} data={providersData} show_head={false}></Table>
        // <></>
        <>
          <div style={{ display: 'grid', gridTemplateColumns: '25fr 3fr 1fr', alignItems: 'center', paddingBottom: '0.5rem' }}><Text fontWeight='500'>{membersData[id ? parseInt(id.slice(-1)) - 1 : 0][0]}</Text><div></div><button onClick={() => { }} className='button button--secondary button--full' style={{ width: '12rem', height: '4rem', padding: '1rem 2rem' }}>Render</button></div>
          <div style={{ display: 'grid', gridTemplateColumns: '25fr 3fr 1fr', alignItems: 'center', paddingTop: '1rem', marginTop: '1rem', borderTop: '1px solid #deebef' }}><Text fontWeight='500'>{membersData[id ? parseInt(id.slice(-1)) - 1 : 0][1]}</Text><Text color='primary'>Invite Pending</Text><button onClick={() => { }} className='button button--secondary button--full' style={{ width: '12rem', height: '4rem', padding: '1rem 2rem'}}>Revoke Invite</button></div>
          <button onClick={() => { }} className='button button--secondary button--full' style={{ width: '20rem', height: '4rem', padding: '1rem 2rem'}}>+ Invite New Data Provider</button>
        </>
        : undefined
      }</Card>

      <Margin size={5} />

      <Card primaryText='Data Users' secondaryText={usersOpen ? '\u25b2' : '\u25bc' }  secondaryTextColor='black' secondaryTextOnClick={() => setUsersOpen(!usersOpen)}>{usersOpen ?
        <>
          <div style={{ display: 'grid', gridTemplateColumns: '15fr 3fr 3fr', alignItems: 'center', padding: '1rem 0px' }}><Text fontWeight='500'>{membersData[id ? parseInt(id.slice(-1)) - 1 : 0][2]}</Text><div></div><Text color='primary'>Dataset Access Details</Text></div>
          <div style={{ display: 'grid', gridTemplateColumns: '15fr 3fr 3fr', alignItems: 'center', paddingTop: '2rem', margin: '1rem 0px', borderTop: '1px solid #deebef' }}><Text fontWeight='500'>{membersData[id ? parseInt(id.slice(-1)) - 1 : 0][3]}</Text><div></div><Text color='primary'>Dataset Access Details</Text></div>
          <button onClick={() => { }} className='button button--secondary button--full' style={{ width: '20rem', height: '4rem', padding: '1rem 2rem' }}>+ Add New Data Users</button>
        </>
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
  );
};

export default UnifiedRegistrySuccess;
