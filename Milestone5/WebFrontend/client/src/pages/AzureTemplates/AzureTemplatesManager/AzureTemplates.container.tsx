import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getAllAzureTemplatesStart,
  getAllAzureTemplatesReset,
} from '@redux/azureTemplate/azureTemplate.actions';
import AzureTemplatesManager from './AzureTemplates.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { selectAzureTemplate } from '@redux/azureTemplate/azureTemplate.selectors';

const mapStateToProps = (state: IState) => {
  return {
    getAllAzureTemplatesError: selectAzureTemplate(state)
      .getAllAzureTemplatesError,
    getAllAzureTemplatesState: selectAzureTemplate(state)
      .getAllAzureTemplatesState,
    getAllAzureTemplatesData: selectAzureTemplate(state)
      .getAllAzureTemplatesData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getAllAzureTemplatesStart: () => dispatch(getAllAzureTemplatesStart()),
  getAllAzureTemplatesReset: () => dispatch(getAllAzureTemplatesReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  AzureTemplatesManager
);
