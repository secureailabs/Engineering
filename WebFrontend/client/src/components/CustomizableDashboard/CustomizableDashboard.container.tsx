import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getDatasetStart,
  getDatasetReset,
} from '@redux/dataset/dataset.actions';
import { selectUser } from '@redux/user/user.selectors';
import Customizabledashboard from './CustomizableDashboard.component';
import { IState } from '@redux/root-reducer';

const mapStateToProps = (state: IState) => {
  return {
    userData: selectUser(state).userData,
  };
};

export default compose(connect(mapStateToProps))(Customizabledashboard);
