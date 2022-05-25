import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getDatasetStart,
  getDatasetReset,
} from '@app/redux/dataset/dataset.actions';
import { selectDataset } from '@app/redux/dataset/dataset.selectors';
import { selectUser } from '@app/redux/user/user.selectors';
import Dataset from './RequestDataAccessForm.component';
import { IState } from '@app/redux/root-reducer';
import { RootAction } from '@app/redux/root.types';
import { TGetDatasetStart } from '@APIs/dataset/dataset.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    getDatasetError: selectDataset(state).getDatasetError,
    getDatasetState: selectDataset(state).getDatasetState,
    getDatasetData: selectDataset(state).getDatasetData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getDatasetStart: (data: TGetDatasetStart) => dispatch(getDatasetStart(data)),
  getDatasetReset: () => dispatch(getDatasetReset()),
});
//@ts-ignore
export default compose(connect(mapStateToProps, mapDispatchToProps))(Dataset);
