import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getAllAccountManagersStart,
  getAllAccountManagersReset,
} from '@redux/accountManager/accountManager.actions';
import AccountManager from './AccountManager.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { selectAccountManager } from '@redux/accountManager/accountManager.selectors';
import { selectUser } from '@redux/user/user.selectors';

const mapStateToProps = (state: IState) => {
  return {
    getAllAccountManagersError: selectAccountManager(state)
      .getAllAccountManagersError,
    getAllAccountManagersState: selectAccountManager(state)
      .getAllAccountManagersState,
    getAllAccountManagersData: selectAccountManager(state)
      .getAllAccountManagersData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  // getAllAccountManagersStart: (data: TGetAllAccountManagersStart) => dispatch(getAllAccountManagersStart(data)),
  getAllAccountManagersStart: (key: string) =>
  dispatch(getAllAccountManagersStart({ OrganizationGuid: key })),
  getAllAccountManagersReset: () => dispatch(getAllAccountManagersReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  AccountManager
);
