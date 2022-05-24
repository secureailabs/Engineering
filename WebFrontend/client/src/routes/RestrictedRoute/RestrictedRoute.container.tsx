import { connect } from 'react-redux';
import { compose } from 'redux';

import { selectUser } from '@app/redux/user/user.selectors';

import RestrictedRoute from './RestrictedRoute.component';
import { IState } from '@app/redux/root-reducer';

const mapStateToProps = (state: IState) => {
  return {
    userState: selectUser(state).userState,
    userData: selectUser(state).userData,
  };
};

export default compose(connect(mapStateToProps))(RestrictedRoute);
