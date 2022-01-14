import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import { signUpStart, signUpReset } from '@redux/user/user.actions';
import { selectUser } from '@redux/user/user.selectors';
import SignUp from './SignUp.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

import { IPostUserStart } from '@redux/user/user.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    userError: selectUser(state).userError,
    userState: selectUser(state).userState,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  signUpStart: (data: IPostUserStart) => dispatch(signUpStart(data)),
  signUpReset: () => dispatch(signUpReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(SignUp);
