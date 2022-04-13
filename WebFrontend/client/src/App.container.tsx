import { connect } from 'react-redux';
import { bindActionCreators, compose, Dispatch } from 'redux';

import {
  checkUserSession,
  checkUserSessionAsync,
} from './redux/user/user.actions';

import { RootAction } from '@redux/root.types';

import App from './App';

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) =>
  bindActionCreators(
    {
      checkUserSession,
      checkUserSessionAsync,
    },
    dispatch
  );
//@ts-ignore
export default compose(connect(null, mapDispatchToProps))(App);
