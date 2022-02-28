import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import { signOutStart } from '@redux/user/user.actions';
import Dashboard from './Dashboard.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  logout: () => dispatch(signOutStart()),
});

export default compose(connect(undefined, mapDispatchToProps))(Dashboard);
