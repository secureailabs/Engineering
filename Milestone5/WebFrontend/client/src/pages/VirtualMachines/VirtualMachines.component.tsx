import React, { useEffect, useState } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TVirtualMachinesProps } from './VirtualMachines.types';
import { CSSTransition } from 'react-transition-group';

import VirtualMachinesSuccess from './VirtualMachines.success';
import VirtualMachinesFailure from './VirtualMachines.failure';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { HiArrowLeft } from 'react-icons/hi';
import VirtualMachineInfo from '@components/VirtualMachineInfo';

const VirtualMachines: React.FC<TVirtualMachinesProps> = ({
  getAllVirtualMachinesReset,
  getAllVirtualMachinesStart,
  getAllVirtualMachinesState,
  getAllVirtualMachinesData,
  userData,
}) => {
  useEffect(() => {
    getAllVirtualMachinesReset();
    getAllVirtualMachinesStart();
  }, []);

  const [stageView, setStageView] = useState<
    TVirtualMachinesProps['getAllVirtualMachinesData']['']['ResearcherOrganization']
  >('Researcher');
  const [virtualMachineID, setVirtualMachineID] = useState<null | string>(null);
  const vmCount = (host: 'Researcher' | 'Data Owner') => {
    let count = 0;
    Object.keys(getAllVirtualMachinesData).map((el) => {
      if (getAllVirtualMachinesData[el].HostForVirtualMachines == host) {
        count += Object.keys(
          getAllVirtualMachinesData[el].VirtualMachinesAssociatedWithDc
        ).length;
      }
    });
    return count;
  };
  return (
    <div
      className={`digitalcontracts ${
        virtualMachineID ? `digitalcontracts--active` : ''
      }`}
    >
      <div className={`digitalcontracts__container `}>
        <div className="digitalcontractlist__listtitle">
          Secure Computation Nodes
          <div
            className="digitalcontractlist__listtitle__options"
            style={{ gridTemplateColumns: '1fr 1fr', maxWidth: '35rem' }}
          >
            <button
              className={
                'digitalcontractlist__listtitle__options__choice' +
                (stageView == 'Researcher' ? '__current' : '')
              }
              onClick={() => setStageView('Researcher')}
            >
              Researcher (
              {getAllVirtualMachinesData ? vmCount('Researcher') : '...'})
            </button>
            <button
              className={
                'digitalcontractlist__listtitle__options__choice' +
                (stageView == 'Data Owner' ? '__current' : '')
              }
              onClick={() => setStageView('Data Owner')}
            >
              Data Owner (
              {getAllVirtualMachinesData ? vmCount('Data Owner') : '...'})
            </button>
          </div>
        </div>
        <ConditionalRender
          //@ts-ignore
          state={getAllVirtualMachinesState}
          success={() => (
            <VirtualMachinesSuccess
              getAllVirtualMachinesData={getAllVirtualMachinesData}
              userData={userData}
              stageView={stageView}
              setVirtualMachineID={setVirtualMachineID}
            />
          )}
          failure={VirtualMachinesFailure}
          Loading={
            <>
              <Spinner />
            </>
          }
        >
          <></>
        </ConditionalRender>
      </div>
      <CSSTransition in={!!virtualMachineID} timeout={200} classNames="my-node">
        {virtualMachineID ? (
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
                  setVirtualMachineID(null);
                  getAllVirtualMachinesStart();
                }}
              />
              <div className="digitalcontracts__details__header__text">
                Virtual Machine Details
              </div>
            </div>
            <VirtualMachineInfo virtualMachineID={virtualMachineID} />
          </div>
        ) : (
          <></>
        )}
      </CSSTransition>
    </div>
  );
};

export default VirtualMachines;
