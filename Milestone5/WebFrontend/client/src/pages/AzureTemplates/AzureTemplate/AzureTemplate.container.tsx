import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getAzureTemplateStart,
  getAzureTemplateReset,
} from '@redux/azureTemplate/azureTemplate.actions';
import { selectAzureTemplate } from '@redux/azureTemplate/azureTemplate.selectors';
import { selectUser } from '@redux/user/user.selectors';
import AzureTemplate from './AzureTemplate.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TGetAzureTemplateStart } from '@redux/azureTemplate/azureTemplate.typesDefs';

const mapStateToProps = (state: IState) => {
  return {
    getAzureTemplateError: selectAzureTemplate(state).getAzureTemplateError,
    getAzureTemplateState: selectAzureTemplate(state).getAzureTemplateState,
    getAzureTemplateData: selectAzureTemplate(state).getAzureTemplateData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getAzureTemplateStart: (data: TGetAzureTemplateStart) =>
    dispatch(getAzureTemplateStart(data)),
  getAzureTemplateReset: () => dispatch(getAzureTemplateReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  AzureTemplate
);
