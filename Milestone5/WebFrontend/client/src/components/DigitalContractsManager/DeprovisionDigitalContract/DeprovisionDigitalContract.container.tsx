import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  deprovisionDigitalContractReset,
  deprovisionDigitalContractStart,
} from '@redux/digitalContract/digitalContract.actions';
import { selectDigitalContract } from '@redux/digitalContract/digitalContract.selectors';
import DeprovisionDigitalContract from './DeprovisionDigitalContract.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TDeprovisionDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    deprovisionDigitalContractError: selectDigitalContract(state)
      .deprovisionDigitalContractError,
    deprovisionDigitalContractState: selectDigitalContract(state)
      .deprovisionDigitalContractState,
    deprovisionDigitalContractData: selectDigitalContract(state)
      .deprovisionDigitalContractData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  deprovisionDigitalContractStart: (
    data: TDeprovisionDigitalContractStart
  ) => dispatch(deprovisionDigitalContractStart(data)),
  deprovisionDigitalContractReset: () =>
    dispatch(deprovisionDigitalContractReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  DeprovisionDigitalContract
);
