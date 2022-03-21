import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  postAccountManagerStart,
  postAccountManagerReset,
  getAllAccountManagersReset,
  getAllAccountManagersStart
} from '@redux/accountManager/accountManager.actions';
import { selectAccountManager } from '@redux/accountManager/accountManager.selectors';
import { selectUser } from '@redux/user/user.selectors';
import RegisterAccount from './RegisterAccount.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TPostAccountManagerStart, TGetAllAccountManagersStart } from '@redux/accountManager/accountManager.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    postAccountManagerState: selectAccountManager(state)
      .postAccountManagerState,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  postAccountManagerStart: (data: TPostAccountManagerStart) =>
    dispatch(postAccountManagerStart(data)),
  postAccountManagerReset: () => dispatch(postAccountManagerReset()),
  getAllAccountManagersStart: (key: string) =>
  dispatch(getAllAccountManagersStart({ OrganizationGuid: key })),
  getAllAccountManagersReset: () => dispatch(getAllAccountManagersReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  RegisterAccount
);
