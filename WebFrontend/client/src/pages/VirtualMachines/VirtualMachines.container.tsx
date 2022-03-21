import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getAllVirtualMachinesStart,
  getAllVirtualMachinesReset,
} from '@redux/virtualMachineManager/virtualMachineManager.actions';
import { selectVirtualMachine } from '@redux/virtualMachineManager/virtualMachineManager.selectors';
import { selectUser } from '@redux/user/user.selectors';
import VirtualMachines from './VirtualMachines.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

const mapStateToProps = (state: IState) => {
  return {
    getAllVirtualMachinesError: selectVirtualMachine(state)
      .getAllVirtualMachinesError,
    getAllVirtualMachinesState: selectVirtualMachine(state)
      .getAllVirtualMachinesState,
    getAllVirtualMachinesData: selectVirtualMachine(state)
      .getAllVirtualMachinesData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getAllVirtualMachinesStart: () => dispatch(getAllVirtualMachinesStart()),
  getAllVirtualMachinesReset: () => dispatch(getAllVirtualMachinesReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  //@ts-ignore
  VirtualMachines
);
