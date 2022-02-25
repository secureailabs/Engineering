import React, { useEffect, useState } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TFeedProps } from './Feed.types';
import { CSSTransition } from 'react-transition-group';

import FeedsSuccess from './Feed.success';
import FeedsFailure from './Feed.failure';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { HiArrowLeft } from 'react-icons/hi';
import VirtualMachineInfo from '@components/VirtualMachineInfo';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

const Feed: React.FC<TFeedProps> = ({
  getAllFeedsReset,
  getAllFeedsStart,
  getAllFeedsState,
  getAllFeedsData,
  limit,
  containerHeight,
}) => {
  useEffect(() => {
    getAllFeedsReset();
    getAllFeedsStart();
  }, []);

  console.log(getAllFeedsData);

  return (
    <ConditionalRender
      //@ts-ignore
      // state={getAllFeedsState}
      state={getAllFeedsState}
      success={() => (
        <FeedsSuccess limit={limit} getAllFeedsData={getAllFeedsData} />
      )}
      failure={FeedsFailure}
      Loading={
        <>
          <Spinner />
        </>
      }
    >
      <></>
    </ConditionalRender>
  );
};

export default Feed;
