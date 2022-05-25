import { connect } from 'react-redux';
import { compose } from 'redux';

import { selectUser } from '@app/redux/user/user.selectors';
import DigitalContract from './DigitalContract.component';
import { IState } from '@app/redux/root-reducer';
import { IUserData } from '@APIs/user/user.typeDefs';

const mapStateToProps = (state: IState): { userData: IUserData } => {
  return {
    userData: selectUser(state).userData,
  };
};


export default compose(connect(mapStateToProps))(DigitalContract);
