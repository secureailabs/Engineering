import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getAccountManagerStart,
  getAccountManagerReset,
} from '@redux/accountManager/accountManager.actions';
import { selectAccountManager } from '@redux/accountManager/accountManager.selectors';
import { selectUser } from '@redux/user/user.selectors';
import AccountInfo from './AccountInfo.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

const mapStateToProps = (state: IState) => {
  return {
    // getAccountManagerError: selectAccountManager(state).getAccountManagerError,
    // getAccountManagerState: selectAccountManager(state).getAccountManagerState,
    // getAccountManagerData: selectAccountManager(state).getAccountManagerData,
    userData: selectUser(state).userData
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  // getAccountManagerStart: (key: string) =>
  //   dispatch(getAccountManagerStart({AccountManagerGuid: key})),
  // getAccountManagerReset: () => dispatch(getAccountManagerReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  AccountInfo
);
