import React from 'react';
import Card from '@secureailabs/web-ui/components/Card';
import preview from '@assets/kca.png';
import { HiOutlineExternalLink } from 'react-icons/hi';
import Button from '@secureailabs/web-ui/components/Button';

import DatasetsSuccess from '@pages/Datasets/Datasets/Datasets.success';

import PatientSummary from '@components/PatientSummary';

import Margin from '@secureailabs/web-ui/components/Margin';

import type { TUnifiedRegistrySuccessProps } from './UnifiedRegistry.types';

const UnifiedRegistrySuccess: React.FC<TUnifiedRegistrySuccessProps> = ({
  getUnifiedRegistryData,
}) => {
  console.log('SASDFAS: ', getUnifiedRegistryData);
  return (
    <>
      <Card primaryText="">
        <div className="unified-registry-card">
          <div className="unified-registry-card__header">
            <img src={preview} />
            <div>
              <p className="unified-registry-card__title">KCA</p>
              <div>
                <p className="unified-registry-card__owner">(Sallie @ KCA)</p>
                <p className="unified-registry-card__access">Request Access</p>
              </div>
            </div>
          </div>
          <div className="unified-registry-card__body">
            <p className="unified-registry-card__description">
              Lorem Ipsum is simply dummy text of the printing and typesetting
              industry. Lorem Ipsum has been the industry&apos;s standard dummy
              text ever since the 1500s, when an unknown printer took a galley
              of type and scrambled it to make a type specimen book. It has
              survived not only five centuries, but also the leap into
              electronic typesetting, remaining essentially unchanged.
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
            <Button full={false} button_type="secondary">
              Data Owner
            </Button>

            <Margin size={5} />
          </div>
        </div>
      </Card>
      <Margin size={10} />
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
