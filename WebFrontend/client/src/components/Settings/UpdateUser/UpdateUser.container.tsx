import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  putUpdateUserStart,
  putUpdateUserReset,
} from '@redux/accountManager/accountManager.actions';
import UpdateUpdateUser from './UpdateUser.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { selectAccountManager } from '@redux/accountManager/accountManager.selectors';
import { selectUser } from '@redux/user/user.selectors';
import { TPutUpdateUserStart } from '@redux/accountManager/accountManager.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    putUpdateUserError: selectAccountManager(state).putUpdateUserError,
    putUpdateUserState: selectAccountManager(state).putUpdateUserState,
    putUpdateUserData: selectAccountManager(state).putUpdateUserData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  // putUpdateUserStart: (data: TGetUpdateUserStart) => dispatch(putUpdateUserStart(data)),
  putUpdateUserStart: (data: TPutUpdateUserStart) =>
    dispatch(putUpdateUserStart(data)),
  putUpdateUserReset: () => dispatch(putUpdateUserReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  UpdateUpdateUser
);
