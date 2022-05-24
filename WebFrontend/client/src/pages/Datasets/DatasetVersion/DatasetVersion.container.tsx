import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getDatasetVersionStart,
  getDatasetVersionReset,
} from '@app/redux/dataset/dataset.actions';
import { selectDataset } from '@app/redux/dataset/dataset.selectors';
import { selectUser } from '@app/redux/user/user.selectors';
import DatasetVersion from './DatasetVersion.component';
import { IState } from '@app/redux/root-reducer';
import { RootAction } from '@app/redux/root.types';
import { TGetDatasetVersionStart } from '@app/redux/dataset/dataset.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    getDatasetVersionError: selectDataset(state).getDatasetVersionError,
    getDatasetVersionState: selectDataset(state).getDatasetVersionState,
    getDatasetVersionData: selectDataset(state).getDatasetVersionData,
    getDatasetData: selectDataset(state).getDatasetData,
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
  //@ts-ignore
  DatasetVersion
);
