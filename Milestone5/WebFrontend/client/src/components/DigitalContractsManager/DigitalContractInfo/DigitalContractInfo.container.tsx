import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getDigitalContractStart,
  getDigitalContractReset,
} from '@redux/digitalContract/digitalContract.actions';
import { selectDigitalContract } from '@redux/digitalContract/digitalContract.selectors';
import { selectUser } from '@redux/user/user.selectors';
import DigitalContractInfo from './DigitalContractInfo.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

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
  getDigitalContractStart: (key: string) =>
    dispatch(getDigitalContractStart({ DigitalContractGuid: key })),
  getDigitalContractReset: () => dispatch(getDigitalContractReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  DigitalContractInfo
);
