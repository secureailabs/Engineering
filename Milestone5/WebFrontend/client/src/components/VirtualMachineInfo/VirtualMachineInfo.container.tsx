import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getVirtualMachineStart,
  getVirtualMachineReset,
} from '@redux/virtualMachineManager/virtualMachineManager.actions';
import { selectVirtualMachine } from '@redux/virtualMachineManager/virtualMachineManager.selectors';
import { selectUser } from '@redux/user/user.selectors';
import VirtualMachineInfo from './VirtualMachineInfo.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

const mapStateToProps = (state: IState) => {
  return {
    getVirtualMachineError: selectVirtualMachine(state).getVirtualMachineError,
    getVirtualMachineState: selectVirtualMachine(state).getVirtualMachineState,
    getVirtualMachineData: selectVirtualMachine(state).getVirtualMachineData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getVirtualMachineStart: (key: string) =>
    dispatch(getVirtualMachineStart({ VirtualMachineGuid: key })),
  getVirtualMachineReset: () => dispatch(getVirtualMachineReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  VirtualMachineInfo
);
