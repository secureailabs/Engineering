import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';
import { signOutStart } from '@app/redux/user/user.actions';

import { selectUser } from '@app/redux/user/user.selectors';
import NavBar from './NavBar.component';
import { IState } from '@app/redux/root-reducer';
import { RootAction } from '@app/redux/root.types';

const mapStateToProps = (state: IState) => {
  return {
    userData: selectUser(state).userData,
  };
};

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  signOutStart: () => dispatch(signOutStart()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(NavBar);
