import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import { signInStart, signInReset } from '@redux/user/user.actions';
import { selectUser } from '@redux/user/user.selectors';
import Login from './Login.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

const mapStateToProps = (state: IState) => {
  return {
    userError: selectUser(state).userError,
    userState: selectUser(state).userState,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  signInStart: ({ email, password }: { email: string; password: string }) =>
    dispatch(signInStart({ email, password })),
  signInReset: () => dispatch(signInReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(Login);
