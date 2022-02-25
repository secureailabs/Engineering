import React, { useEffect, useState } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TDatasetsProps } from './Datasets.types';
import { CSSTransition } from 'react-transition-group';

import DatasetsSuccess from './Datasets.success';
import DatasetsFailure from './Datasets.failure';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { HiArrowLeft } from 'react-icons/hi';
import VirtualMachineInfo from '@components/VirtualMachineInfo';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

const Datasets: React.FC<TDatasetsProps> = ({
  getAllDatasetsReset,
  getAllDatasetsStart,
  getAllDatasetsState,
  getAllDatasetsData,
}) => {
  useEffect(() => {
    getAllDatasetsReset();
    getAllDatasetsStart();
  }, []);

  return (
    <StandardContent title="Datasets">
      <ConditionalRender
        //@ts-ignore
        state={getAllDatasetsState}
        success={() => (
          <DatasetsSuccess getAllDatasetsData={getAllDatasetsData} />
        )}
        failure={DatasetsFailure}
        Loading={
          <>
            <Spinner />
          </>
        }
      >
        <></>
      </ConditionalRender>
    </StandardContent>
  );
};

export default Datasets;
