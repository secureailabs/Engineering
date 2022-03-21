import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  listAzureTemplatesStart,
  listAzureTemplatesReset,
} from '@redux/azureTemplatesManager/azureTemplatesManager.actions';
import AzureTemplatesManager from './AzureTemplatesManager.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { selectAzureTemplatesManager } from '@redux/azureTemplatesManager/azureTemplatesManager.selectors';

const mapStateToProps = (state: IState) => {
  return {
    listAzureTemplatesError: selectAzureTemplatesManager(state)
      .listAzureTemplatesError,
    listAzureTemplatesState: selectAzureTemplatesManager(state)
      .listAzureTemplatesState,
    listAzureTemplatesData: selectAzureTemplatesManager(state)
      .listAzureTemplatesData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  listAzureTemplatesStart: () =>
  dispatch(listAzureTemplatesStart()),
  listAzureTemplatesReset: () => dispatch(listAzureTemplatesReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  AzureTemplatesManager
);
