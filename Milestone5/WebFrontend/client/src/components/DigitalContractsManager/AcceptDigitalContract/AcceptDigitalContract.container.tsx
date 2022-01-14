import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  patchAcceptDigitalContractReset,
  patchAcceptDigitalContractStart,
} from '@redux/digitalContract/digitalContract.actions';
import { selectDigitalContract } from '@redux/digitalContract/digitalContract.selectors';
import AcceptDigitalContract from './AcceptDigitalContract.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TPatchAcceptDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    patchAcceptDigitalContractError: selectDigitalContract(state)
      .patchAcceptDigitalContractError,
    patchAcceptDigitalContractState: selectDigitalContract(state)
      .patchAcceptDigitalContractState,
    patchAcceptDigitalContractData: selectDigitalContract(state)
      .patchAcceptDigitalContractData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  patchAcceptDigitalContractStart: (data: TPatchAcceptDigitalContractStart) =>
    dispatch(patchAcceptDigitalContractStart(data)),
  patchAcceptDigitalContractReset: () =>
    dispatch(patchAcceptDigitalContractReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  AcceptDigitalContract
);
