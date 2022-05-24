import {
  ActionType,
  createAction,
  EmptyActionCreator,
  PayloadAction,
} from 'typesafe-actions';

import type { IDefaults } from '@app/redux/typedefs';

import type {
  TPutVirtualMachineStart,
  TGetVirtualMachineSuccess,
  TGetVirtualMachineStart,
  TGetAllVirtualMachinesSuccess,
} from './virtualMachineManager.typeDefs';

export type VirtualMachineActions =
  // PUT
  | ActionType<typeof putVirtualMachineStart>
  | ActionType<typeof putVirtualMachineSuccess>
  | ActionType<typeof putVirtualMachineFailure>
  | ActionType<typeof putVirtualMachineReset>
  // GET
  | ActionType<typeof getVirtualMachineStart>
  | ActionType<typeof getVirtualMachineSuccess>
  | ActionType<typeof getVirtualMachineFailure>
  | ActionType<typeof getVirtualMachineReset>
  // GET ALL
  | ActionType<typeof getAllVirtualMachinesStart>
  | ActionType<typeof getAllVirtualMachinesSuccess>
  | ActionType<typeof getAllVirtualMachinesFailure>
  | ActionType<typeof getAllVirtualMachinesReset>;

// PUT

export const putVirtualMachineStart = createAction(
  // Type
  'VirtualMachine/PUT_VIRTUAL_MACHINE_START',
  // Payload
  (data: TPutVirtualMachineStart) => data
)();

export const putVirtualMachineSuccess: EmptyActionCreator<string> = createAction(
  'VirtualMachine/PUT_VIRTUAL_MACHINE_SUCCESS'
  // Payload
)();

export const putVirtualMachineFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'VirtualMachine/PUT_VIRTUAL_MACHINE_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const putVirtualMachineReset: EmptyActionCreator<string> = createAction(
  'VirtualMachine/PUT_VIRTUAL_MACHINE_RESET'
)();

// GET ONE

export const getVirtualMachineStart = createAction(
  // Type
  'VirtualMachine/GET_VIRTUAL_MACHINE_START',
  // Payload
  (data: TGetVirtualMachineStart) => data
)();
export const getVirtualMachineSuccess: (
  data: TGetVirtualMachineSuccess
) => PayloadAction<string, TGetVirtualMachineSuccess> = createAction(
  'VirtualMachine/GET_VIRTUAL_MACHINE_SUCCESS',
  // Payload
  (data: TGetVirtualMachineSuccess) => data
)();
export const getVirtualMachineFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'VirtualMachine/GET_VIRTUAL_MACHINE_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getVirtualMachineReset: EmptyActionCreator<string> = createAction(
  'VirtualMachine/GET_VIRTUAL_MACHINE_RESET'
)();

// GET ALL

export const getAllVirtualMachinesStart = createAction(
  // Type
  'VirtualMachine/GET_ALL_VIRTUAL_MACHINES_START'
)();
export const getAllVirtualMachinesSuccess: (
  data: TGetAllVirtualMachinesSuccess
) => PayloadAction<string, TGetAllVirtualMachinesSuccess> = createAction(
  'VirtualMachine/GET_ALL_VIRTUAL_MACHINES_SUCCESS',
  // Payload
  (data: TGetAllVirtualMachinesSuccess) => data
)();
export const getAllVirtualMachinesFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'VirtualMachine/GET_ALL_VIRTUAL_MACHINES_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getAllVirtualMachinesReset: EmptyActionCreator<string> = createAction(
  'VirtualMachine/GET_ALL_VIRTUAL_MACHINES_RESET'
)();
