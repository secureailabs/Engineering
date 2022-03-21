import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  provisionDigitalContractReset,
  provisionDigitalContractStart,
} from '@redux/digitalContract/digitalContract.actions';
import { selectDigitalContract } from '@redux/digitalContract/digitalContract.selectors';
import ProvisionDigitalContract from './ProvisionDigitalContract.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TProvisionDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    provisionDigitalContractError: selectDigitalContract(state)
      .provisionDigitalContractError,
    provisionDigitalContractState: selectDigitalContract(state)
      .provisionDigitalContractState,
    provisionDigitalContractData: selectDigitalContract(state)
      .provisionDigitalContractData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  provisionDigitalContractStart: (
    data: TProvisionDigitalContractStart
  ) => dispatch(provisionDigitalContractStart(data)),
  provisionDigitalContractReset: () =>
    dispatch(provisionDigitalContractReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  ProvisionDigitalContract
);
