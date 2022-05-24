import { connect } from 'react-redux';
import { compose } from 'redux';

import { selectUser } from '@app/redux/user/user.selectors';

import { IState } from '@app/redux/root-reducer';

import UnProtectedRoute from './UnProtectedRoute.component';

const mapStateToProps = (state: IState) => {
  return {
    userState: selectUser(state).userState,
    userData: selectUser(state).userData,
  };
};

export default compose(connect(mapStateToProps))(UnProtectedRoute);
