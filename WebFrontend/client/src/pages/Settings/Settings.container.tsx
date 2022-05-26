import { connect } from 'react-redux';
import { compose } from 'redux';

import { selectUser } from '@app/redux/user/user.selectors';
import Settings from './Settings.component';
import { IState } from '@app/redux/root-reducer';
const mapStateToProps = (state: IState) => {
  return {
    userData: selectUser(state).userData,
  };
};

export default compose(connect(mapStateToProps))(Settings);
