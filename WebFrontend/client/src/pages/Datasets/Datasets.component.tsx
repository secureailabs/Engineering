import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TDatasetsProps } from './Datasets.types';

import DatasetsSuccess from './Datasets.success';
import DatasetsFailure from './Datasets.failure';
import { useEffect, useState } from 'react';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import DatasetInfo from '@components/DatasetsManager/DatasetInfo';
import { CSSTransition } from 'react-transition-group';

import { HiArrowLeft } from 'react-icons/hi';

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

  const [datasetID, setDatasetID] = useState<null | string>(null);
  return (
    <div className={`datasets ${datasetID ? `datasets--active` : ''}`}>
      <div className="datasetlist">
        <div className="datasetlist__listtitle">Datasets</div>
        <ConditionalRender
          //@ts-ignore
          state={getAllDatasetsState}
          success={() => (
            <CSSTransition in={!!datasetID} timeout={200} classNames="my-node">
              <DatasetsSuccess
                setDatasetID={setDatasetID}
                getAllDatasetsData={getAllDatasetsData}
              />
            </CSSTransition>
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
      </div>
      {datasetID ? (
        <div className="datasets__details">
          <div className="datasets__details__header">
            <HiArrowLeft
              style={{
                // padding: '2rem',
                width: '3rem',
                height: '3rem',
                cursor: 'pointer',
              }}
              onClick={() => {
                setDatasetID(null);
                getAllDatasetsStart();
              }}
            />
            <div className="datasets__details__header__text">
              Dataset Details
            </div>
          </div>
          <DatasetInfo datasetID={datasetID} />
        </div>
      ) : (
        <></>
      )}
    </div>
  );
};

export default Datasets;
