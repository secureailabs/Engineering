import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import { getAllFeedsStart, getAllFeedsReset } from '@app/redux/feed/feed.actions';
import { selectFeed } from '@app/redux/feed/feed.selector';
import Feed from './Feed.component';
import { IState } from '@app/redux/root-reducer';
import { RootAction } from '@app/redux/root.types';

const mapStateToProps = (state: IState) => {
  return {
    getAllFeedsError: selectFeed(state).getAllFeedsError,
    getAllFeedsState: selectFeed(state).getAllFeedsState,
    getAllFeedsData: selectFeed(state).getAllFeedsData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getAllFeedsStart: () => dispatch(getAllFeedsStart()),
  getAllFeedsReset: () => dispatch(getAllFeedsReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  //@ts-ignore
  Feed
);
