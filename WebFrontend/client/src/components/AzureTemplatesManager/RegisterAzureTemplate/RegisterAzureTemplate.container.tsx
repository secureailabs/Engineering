import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  registerAzureTemplateStart,
  registerAzureTemplateReset,
  listAzureTemplatesReset,
  listAzureTemplatesStart
} from '@redux/azureTemplatesManager/azureTemplatesManager.actions';
import { selectAzureTemplatesManager } from '@redux/azureTemplatesManager/azureTemplatesManager.selectors';
import RegisterAzureTemplate from './RegisterAzureTemplate.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TRegisterAzureTemplateStart } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';

const mapStateToProps = (state: IState) => {
  return {
    registerAzureTemplateState: selectAzureTemplatesManager(state)
      .registerAzureTemplateState,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  registerAzureTemplateStart: (data: TRegisterAzureTemplateStart) =>
    dispatch(registerAzureTemplateStart(data)),
  registerAzureTemplateReset: () => dispatch(registerAzureTemplateReset()),
  listAzureTemplatesStart: () =>
  dispatch(listAzureTemplatesStart()),
  listAzureTemplatesReset: () => dispatch(listAzureTemplatesReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  RegisterAzureTemplate
);
