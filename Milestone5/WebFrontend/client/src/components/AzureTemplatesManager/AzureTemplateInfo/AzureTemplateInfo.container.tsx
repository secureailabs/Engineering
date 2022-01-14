import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  pullAzureTemplateStart,
  pullAzureTemplateReset,
} from '@redux/azureTemplatesManager/azureTemplatesManager.actions';
import { selectAzureTemplatesManager } from '@redux/azureTemplatesManager/azureTemplatesManager.selectors';
import AzureTemplateInfo from './AzureTemplateInfo.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

const mapStateToProps = (state: IState) => {
  return {
    pullAzureTemplateData: selectAzureTemplatesManager(state).pullAzureTemplateData,
    pullAzureTemplateState: selectAzureTemplatesManager(state).pullAzureTemplateState,
    pullAzureTemplateError: selectAzureTemplatesManager(state).pullAzureTemplateError,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  pullAzureTemplateStart: (key: string) =>
    dispatch(pullAzureTemplateStart({ TemplateGuid: key })),
  pullAzureTemplateReset: () => dispatch(pullAzureTemplateReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  AzureTemplateInfo
);
