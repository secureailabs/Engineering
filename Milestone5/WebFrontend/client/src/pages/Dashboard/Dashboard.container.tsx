import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import { signOutStart } from '@redux/user/user.actions';
import { selectUser } from '@redux/user/user.selectors';
import Dashboard from './Dashboard.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

//trying to remove func from dispatch functions
const mapStateToProps = (state: IState) => {
  return {
    userData: selectUser(state).userData,
  };
};

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  logout: () => dispatch(signOutStart()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(Dashboard);
