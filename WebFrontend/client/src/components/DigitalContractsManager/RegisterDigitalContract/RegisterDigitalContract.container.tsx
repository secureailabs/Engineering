import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  postDigitalContractStart,
  postDigitalContractReset,
} from '@redux/digitalContract/digitalContract.actions';
import { selectDigitalContract } from '@redux/digitalContract/digitalContract.selectors';
import { selectUser } from '@redux/user/user.selectors';
import RegisterDigitalContract from './RegisterDigitalContract.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TPostDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    postDigitalContractState: selectDigitalContract(state)
      .postDigitalContractState,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  postDigitalContractStart: (data: TPostDigitalContractStart) =>
    dispatch(postDigitalContractStart(data)),
  postDigitalContractReset: () => dispatch(postDigitalContractReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  RegisterDigitalContract
);
