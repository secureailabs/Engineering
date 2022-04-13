import { connect } from 'react-redux';
import { compose } from 'redux';

import { selectUser } from '@redux/user/user.selectors';
import DigitalContract from './DigitalContract.component';
import { IState } from '@redux/root-reducer';
import { IUserData } from '@redux/user/user.typeDefs';

const mapStateToProps = (state: IState): { userData: IUserData } => {
  return {
    userData: selectUser(state).userData,
  };
};


export default compose(connect(mapStateToProps))(DigitalContract);
