import { connect } from 'react-redux';
import { compose } from 'redux';

import { selectUser } from '@redux/user/user.selectors';

import ProtectedRoute from './ProtectedRoute.component';
import { IState } from '@redux/root-reducer';

import { useQueryClient } from 'react-query';

const mapStateToProps = (state: IState) => {
  return {
    userState: selectUser(state).userState,
    userData: selectUser(state).userData,
  };
};

export default compose(connect(mapStateToProps))(ProtectedRoute);
