import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getAllDatasetsStart,
  getAllDatasetsReset,
} from '@redux/dataset/dataset.actions';
import { selectDataset } from '@redux/dataset/dataset.selectors';
import Datasets from './Datasets.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

const mapStateToProps = (state: IState) => {
  return {
    getAllDatasetsError: selectDataset(state).getAllDatasetsError,
    getAllDatasetsState: selectDataset(state).getAllDatasetsState,
    getAllDatasetsData: selectDataset(state).getAllDatasetsData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getAllDatasetsStart: () => dispatch(getAllDatasetsStart()),
  getAllDatasetsReset: () => dispatch(getAllDatasetsReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  //@ts-ignore
  Datasets
);
