import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getAllDigitalContractsStart,
  getAllDigitalContractsReset,
} from '@redux/digitalContract/digitalContract.actions';
import { selectDigitalContract } from '@redux/digitalContract/digitalContract.selectors';
import { selectUser } from '@redux/user/user.selectors';
import DigitalContracts from './DigitalContracts.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

const mapStateToProps = (state: IState) => {
  return {
    getAllDigitalContractsError: selectDigitalContract(state)
      .getAllDigitalContractsError,
    getAllDigitalContractsState: selectDigitalContract(state)
      .getAllDigitalContractsState,
    getAllDigitalContractsData: selectDigitalContract(state)
      .getAllDigitalContractsData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getAllDigitalContractsStart: () => dispatch(getAllDigitalContractsStart()),
  getAllDigitalContractsReset: () => dispatch(getAllDigitalContractsReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  //@ts-ignore
  DigitalContracts
);
