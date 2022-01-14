import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  patchActivateDigitalContractReset,
  patchActivateDigitalContractStart,
} from '@redux/digitalContract/digitalContract.actions';
import { selectDigitalContract } from '@redux/digitalContract/digitalContract.selectors';
import ActivateDigitalContract from './ActivateDigitalContract.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TPatchActivateDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    patchActivateDigitalContractError: selectDigitalContract(state)
      .patchActivateDigitalContractError,
    patchActivateDigitalContractState: selectDigitalContract(state)
      .patchActivateDigitalContractState,
    patchActivateDigitalContractData: selectDigitalContract(state)
      .patchActivateDigitalContractData,
    getDigitalContractData: selectDigitalContract(state).getDigitalContractData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  patchActivateDigitalContractStart: (
    data: TPatchActivateDigitalContractStart
  ) => dispatch(patchActivateDigitalContractStart(data)),
  patchActivateDigitalContractReset: () =>
    dispatch(patchActivateDigitalContractReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  ActivateDigitalContract
);
