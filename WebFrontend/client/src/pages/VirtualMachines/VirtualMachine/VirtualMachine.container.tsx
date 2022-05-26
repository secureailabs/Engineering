// import { connect } from 'react-redux';
// import { compose, Dispatch } from 'redux';

// import {
//   getVirtualMachineStart,
//   getVirtualMachineReset,
// } from '@app/redux/virtualMachineManager/virtualMachineManager.actions';
// import { selectVirtualMachine } from '@app/redux/virtualMachineManager/virtualMachineManager.selectors';
// import { selectUser } from '@app/redux/user/user.selectors';
// import VirtualMachine from './VirtualMachine.component';
// import { IState } from '@app/redux/root-reducer';
// import { RootAction } from '@app/redux/root.types';
// import { TGetVirtualMachineStart } from '@app/redux/virtualMachineManager/virtualMachineManager.typeDefs';

// const mapStateToProps = (state: IState) => {
//   return {
//     getVirtualMachineError: selectVirtualMachine(state).getVirtualMachineError,
//     getVirtualMachineState: selectVirtualMachine(state).getVirtualMachineState,
//     getVirtualMachineData: selectVirtualMachine(state).getVirtualMachineData,
//     userData: selectUser(state).userData,
//   };
// };

// //trying to remove func from dispatch functions

// const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
//   getVirtualMachineStart: (data: TGetVirtualMachineStart) =>
//     dispatch(getVirtualMachineStart(data)),
//   getVirtualMachineReset: () => dispatch(getVirtualMachineReset()),
// });

// export default compose(connect(mapStateToProps, mapDispatchToProps))(
//   //@ts-ignore
//   VirtualMachine
// );

export {}