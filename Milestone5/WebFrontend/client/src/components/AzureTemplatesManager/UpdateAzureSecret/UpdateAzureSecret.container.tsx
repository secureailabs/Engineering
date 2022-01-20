import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  updateAzureSecretReset,
  updateAzureSecretStart,
} from '@redux/azureTemplatesManager/azureTemplatesManager.actions';
import { selectAzureTemplatesManager } from '@redux/azureTemplatesManager/azureTemplatesManager.selectors';
import UpdateAzureSecret from './UpdateAzureSecret.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TUpdateAzureTemplateStart } from '@redux/azureTemplatesManager/azureTemplatesManager.typesDefs';

const mapStateToProps = (state: IState) => {
  return {
    updateAzureSecretError: selectAzureTemplatesManager(state)
      .updateAzureSecretError,
    updateAzureSecretState: selectAzureTemplatesManager(state)
      .updateAzureSecretState,
    pullAzureTemplateData: selectAzureTemplatesManager(state)
      .pullAzureTemplateData
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  updateAzureSecretStart: (data: TUpdateAzureTemplateStart) =>
    dispatch(updateAzureSecretStart(data)),
  updateAzureSecretReset: () =>
    dispatch(updateAzureSecretReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  UpdateAzureSecret
);
