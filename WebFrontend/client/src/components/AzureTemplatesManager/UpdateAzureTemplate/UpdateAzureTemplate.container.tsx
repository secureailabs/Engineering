import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  updateAzureTemplateStart,
  updateAzureTemplateReset,
  pullAzureTemplateStart,
} from '@redux/azureTemplatesManager/azureTemplatesManager.actions';
import UpdateAzureTemplate from './UpdateAzureTemplate.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { selectAzureTemplatesManager } from '@redux/azureTemplatesManager/azureTemplatesManager.selectors';

import { TUpdateAzureTemplateStart, TPullAzureTemplateStart } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';

const mapStateToProps = (state: IState) => {
  return {
    updateAzureTemplateError: selectAzureTemplatesManager(state).updateAzureTemplateError,
    updateAzureTemplateState: selectAzureTemplatesManager(state).updateAzureTemplateState,
    updateAzureTemplateData: selectAzureTemplatesManager(state).updateAzureTemplateData,
    pullAzureTemplateData: selectAzureTemplatesManager(state).pullAzureTemplateData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  updateAzureTemplateStart: (data: TUpdateAzureTemplateStart) =>
    dispatch(updateAzureTemplateStart(data)),
  updateAzureTemplateReset: () => dispatch(updateAzureTemplateReset()),
  pullAzureTemplateStart: (data: TPullAzureTemplateStart) => 
    dispatch(pullAzureTemplateStart(data)),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  UpdateAzureTemplate
);
