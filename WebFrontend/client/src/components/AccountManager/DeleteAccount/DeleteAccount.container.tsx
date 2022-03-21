import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  deleteAccountManagerReset,
  deleteAccountManagerStart,
  getAllAccountManagersStart,
  getAllAccountManagersReset,
} from '@redux/accountManager/accountManager.actions';
import  DeleteAccount from './DeleteAccount.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TDeleteAccountManagerStart, TGetAllAccountManagersStart } from '@redux/accountManager/accountManager.typeDefs';
import { selectAccountManager } from '@redux/accountManager/accountManager.selectors';

const mapStateToProps = (state: IState) => {
  return {
    deleteAccountManagerError: selectAccountManager(state)
      .deleteAccountManagerError,
    deleteAccountManagerState: selectAccountManager(state)
      .deleteAccountManagerState,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  deleteAccountManagerStart: (
    data: TDeleteAccountManagerStart
  ) =>dispatch(deleteAccountManagerStart(data)),
  deleteAccountManagerReset: () =>
    dispatch(deleteAccountManagerReset()),
  getAllAccountManagersStart: (
    data: TGetAllAccountManagersStart
  ) => dispatch(getAllAccountManagersStart(data)),
  getAllAccountManagersReset: () => dispatch(getAllAccountManagersReset())
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  DeleteAccount
);
