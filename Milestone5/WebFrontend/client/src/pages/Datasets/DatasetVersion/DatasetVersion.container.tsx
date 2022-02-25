import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getDatasetVersionStart,
  getDatasetVersionReset,
} from '@redux/dataset/dataset.actions';
import { selectDataset } from '@redux/dataset/dataset.selectors';
import { selectUser } from '@redux/user/user.selectors';
import DatasetVersion from './DatasetVersion.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TGetDatasetVersionStart } from '@redux/dataset/dataset.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    getDatasetVersionError: selectDataset(state).getDatasetVersionError,
    getDatasetVersionState: selectDataset(state).getDatasetVersionState,
    getDatasetVersionData: selectDataset(state).getDatasetVersionData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getDatasetVersionStart: (data: TGetDatasetVersionStart) =>
    dispatch(getDatasetVersionStart(data)),
  getDatasetVersionReset: () => dispatch(getDatasetVersionReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  DatasetVersion
);
