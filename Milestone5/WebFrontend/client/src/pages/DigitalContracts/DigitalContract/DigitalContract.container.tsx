import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getDigitalContractStart,
  getDigitalContractReset,
} from '@redux/digitalContract/digitalContract.actions';
import { selectDigitalContract } from '@redux/digitalContract/digitalContract.selectors';
import { selectUser } from '@redux/user/user.selectors';
import DigitalContract from './DigitalContract.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TGetDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    getDigitalContractError: selectDigitalContract(state)
      .getDigitalContractError,
    getDigitalContractState: selectDigitalContract(state)
      .getDigitalContractState,
    getDigitalContractData: selectDigitalContract(state).getDigitalContractData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getDigitalContractStart: (data: TGetDigitalContractStart) =>
    dispatch(getDigitalContractStart(data)),
  getDigitalContractReset: () => dispatch(getDigitalContractReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  DigitalContract
);
