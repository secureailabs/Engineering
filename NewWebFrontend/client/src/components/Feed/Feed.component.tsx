import React, { useEffect, useState } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TFeedProps } from './Feed.types';
import { CSSTransition } from 'react-transition-group';

import FeedsSuccess from './Feed.success';
import FeedsFailure from './Feed.failure';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { HiArrowLeft } from 'react-icons/hi';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import { demo_data } from '@APIs/feed/feed.data';

const Feed: React.FC<TFeedProps> = ({
  // getAllFeedsReset,
  // getAllFeedsStart,
  // getAllFeedsState,
  limit,
  containerHeight,
}) => {
  // useEffect(() => {
  //   getAllFeedsReset();
  //   getAllFeedsStart();
  // }, []);

  return (
    <ConditionalRender
      //@ts-ignore
      // state={getAllFeedsState}
      state={'success'}
      success={() => (
        <FeedsSuccess
          containerHeight={containerHeight}
          limit={limit}
          // @ts-ignore
          getAllFeedsData={demo_data}
        />
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
