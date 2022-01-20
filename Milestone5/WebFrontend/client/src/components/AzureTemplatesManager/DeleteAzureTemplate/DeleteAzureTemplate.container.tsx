import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  deleteAzureTemplateReset,
  deleteAzureTemplateStart,
  listAzureTemplatesStart,
  listAzureTemplatesReset,
} from '@redux/azureTemplatesManager/azureTemplatesManager.actions';
import  DeleteAzureTemplate from './DeleteAzureTemplate.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TDeleteAzureTemplateStart } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';
import { selectAzureTemplatesManager } from '@redux/azureTemplatesManager/azureTemplatesManager.selectors';

const mapStateToProps = (state: IState) => {
  return {
    deleteAzureTemplateError: selectAzureTemplatesManager(state)
      .deleteAzureTemplateError,
    deleteAzureTemplateState: selectAzureTemplatesManager(state)
      .deleteAzureTemplateState,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  deleteAzureTemplateStart: (
    data: TDeleteAzureTemplateStart
  ) =>dispatch(deleteAzureTemplateStart(data)),
  deleteAzureTemplateReset: () =>
    dispatch(deleteAzureTemplateReset()),
  listAzureTemplatesStart: () => dispatch(listAzureTemplatesStart()),
  listAzureTemplatesReset: () => dispatch(listAzureTemplatesReset())
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  DeleteAzureTemplate
);
