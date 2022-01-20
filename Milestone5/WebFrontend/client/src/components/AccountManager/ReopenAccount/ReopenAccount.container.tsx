import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  putAccountManagerReset,
  putAccountManagerStart,
  getAllAccountManagersStart,
  getAllAccountManagersReset,
} from '@redux/accountManager/accountManager.actions';
import ReopenAccount from './ReopenAccount.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TDeleteAccountManagerStart, TGetAllAccountManagersStart } from '@redux/accountManager/accountManager.typeDefs';
import { selectAccountManager } from '@redux/accountManager/accountManager.selectors';

const mapStateToProps = (state: IState) => {
  return {
    putAccountManagerError: selectAccountManager(state)
      .putAccountManagerError,
    putAccountManagerState: selectAccountManager(state)
      .putAccountManagerState,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  putAccountManagerStart: (
    data: TDeleteAccountManagerStart
  ) =>dispatch(putAccountManagerStart(data)),
  putAccountManagerReset: () =>
    dispatch(putAccountManagerReset()),
  getAllAccountManagersStart: (
    data: TGetAllAccountManagersStart
  ) => dispatch(getAllAccountManagersStart(data)),
  getAllAccountManagersReset: () => dispatch(getAllAccountManagersReset())
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  ReopenAccount
);
