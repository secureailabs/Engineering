import React, { useEffect, useState } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TDigitalContractsProps } from './DigitalContracts.types';
import { CSSTransition } from 'react-transition-group';

import DigitalContractsSuccess from './DigitalContracts.success';
import DigitalContractsFailure from './DigitalContracts.failure';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { HiArrowLeft } from 'react-icons/hi';
import DigitalContractInfo from '@components/DigitalContractsManager/DigitalContractInfo';
import getDCStage from '@utils/getDCStage';

const DigitalContracts: React.FC<TDigitalContractsProps> = ({
  getAllDigitalContractsReset,
  getAllDigitalContractsStart,
  getAllDigitalContractsState,
  getAllDigitalContractsData,
  userData,
}) => {
  useEffect(() => {
    getAllDigitalContractsReset();
    getAllDigitalContractsStart();
  }, []);

  const [stageView, setStageView] = useState(3);
  const [digitalContractID, setDigitalContractID] = useState<null | string>(
    null
  );

  return (
    <div
      className={`digitalcontracts ${
        digitalContractID ? `digitalcontracts--active` : ''
      }`}
    >
      <div className={`digitalcontracts__container `}>
        <div className="digitalcontractlist__listtitle">
          Digital Contracts
          <div className="digitalcontractlist__listtitle__options">
            <button
              className={
                'digitalcontractlist__listtitle__options__choice' +
                (stageView == 1 ? '__current' : '')
              }
              onClick={() => setStageView(1)}
            >
              Waiting for Approval ({getAllDigitalContractsData ? Object.entries(getAllDigitalContractsData.DigitalContracts).filter(([key, value]) => value.ContractStage == 1).length : ''})
            </button>
            <button
              className={
                'digitalcontractlist__listtitle__options__choice' +
                (stageView == 2 ? '__current' : '')
              }
              onClick={() => setStageView(2)}
            >
              Waiting for Activation ({getAllDigitalContractsData ? Object.entries(getAllDigitalContractsData.DigitalContracts).filter(([key, value]) => value.ContractStage == 2).length : ''})
            </button>
            <button
              className={
                'digitalcontractlist__listtitle__options__choice' +
                (stageView == 3 ? '__current' : '')
              }
              onClick={() => setStageView(3)}
            >
              Activated ({getAllDigitalContractsData ? Object.entries(getAllDigitalContractsData.DigitalContracts).filter(([key, value]) => getDCStage(value.ContractStage, value.ExpirationTime) == 3).length : ''})
            </button>
            <button
              className={
                'digitalcontractlist__listtitle__options__choice' +
                (stageView == 4 ? '__current' : '')
              }
              onClick={() => setStageView(4)}
            >
              Expired ({getAllDigitalContractsData ? Object.entries(getAllDigitalContractsData.DigitalContracts).filter(([key, value]) => getDCStage(value.ContractStage, value.ExpirationTime) == 4).length : ''})
            </button>
          </div>
        </div>
        <ConditionalRender
          //@ts-ignore
          state={getAllDigitalContractsState}
          success={() => (
            <DigitalContractsSuccess
              getAllDigitalContractsData={getAllDigitalContractsData}
              userData={userData}
              stageView={stageView}
              setDigitalContractID={setDigitalContractID}
            />
          )}
          failure={DigitalContractsFailure}
          Loading={
            <>
              <Spinner />
            </>
          }
        >
          <></>
        </ConditionalRender>
      </div>
      <CSSTransition
        in={!!digitalContractID}
        timeout={200}
        classNames="my-node"
      >
        {digitalContractID ? (
          <div className="digitalcontracts__details">
            <div className="digitalcontracts__details__header">
              <HiArrowLeft
                style={{
                  // padding: '2rem',
                  width: '3rem',
                  height: '3rem',
                  cursor: 'pointer',
                }}
                onClick={() => {
                  setDigitalContractID(null);
                  getAllDigitalContractsStart();
                }}
              />
              <div className="digitalcontracts__details__header__text">
                Digital Contract Details{digitalContractID && <> - {digitalContractID}</>}
              </div>
            </div>
            <DigitalContractInfo digitalContractID={digitalContractID} />
          </div>
        ) : (
          <></>
        )}
      </CSSTransition>
    </div>
  );
};

export default DigitalContracts;
