import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  putUpdatePasswordStart,
  putUpdatePasswordReset,
} from '@redux/accountManager/accountManager.actions';
import UpdatePassword from './UpdatePassword.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { selectAccountManager } from '@redux/accountManager/accountManager.selectors';
import { selectUser } from '@redux/user/user.selectors';
import { TPutUpdatePasswordStart } from '@redux/accountManager/accountManager.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    putUpdatePasswordError: selectAccountManager(state).putUpdatePasswordError,
    putUpdatePasswordState: selectAccountManager(state).putUpdatePasswordState,
    putUpdatePasswordData: selectAccountManager(state).putUpdatePasswordData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  // putUpdatePasswordStart: (data: TGetUpdatePasswordStart) => dispatch(putUpdatePasswordStart(data)),
  putUpdatePasswordStart: (data: TPutUpdatePasswordStart) =>
    dispatch(putUpdatePasswordStart(data)),
  putUpdatePasswordReset: () => dispatch(putUpdatePasswordReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  UpdatePassword
);
