import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  patchAssociateAzureStart,
  patchAssociateAzureReset,
  getDigitalContractStart
} from '@redux/digitalContract/digitalContract.actions';
import { selectDigitalContract } from '@redux/digitalContract/digitalContract.selectors';
import { TPatchAssociateAzureStart, TGetDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';
import { selectUser } from '@redux/user/user.selectors';
import EditAzureTemplate from './EditAzureTemplate.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

const mapStateToProps = (state: IState) => {
  return {
    patchAssociateAzureError: selectDigitalContract(state)
      .patchAssociateAzureError,
    patchAssociateAzureState: selectDigitalContract(state)
      .patchAssociateAzureState,
    patchAssociateAzureData: selectDigitalContract(state)
      .patchAssociateAzureData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  patchAssociateAzureStart: (data: TPatchAssociateAzureStart) =>
    dispatch(patchAssociateAzureStart(data)),
  patchAssociateAzureReset: () => dispatch(patchAssociateAzureReset()),
  getDigitalContractStart: (data: TGetDigitalContractStart) =>
    dispatch(getDigitalContractStart(data)),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  EditAzureTemplate
);
