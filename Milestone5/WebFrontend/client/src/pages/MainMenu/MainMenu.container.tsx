import { connect } from 'react-redux';
import { compose } from 'redux';

import { selectUser } from '@redux/user/user.selectors';

import MainMenu from './MainMenu.component';
import { IState } from '@redux/root-reducer';

const mapStateToProps = (state: IState) => {
  return {
    userData: selectUser(state).userData,
  };
};

export default compose(connect(mapStateToProps))(MainMenu);
