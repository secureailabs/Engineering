// tslint:disable: no-null-null-union
import { createReducer } from 'typesafe-actions';

import {
  // GET ONE
  getVirtualMachineFailure,
  getVirtualMachineReset,
  getVirtualMachineStart,
  getVirtualMachineSuccess,
  // GET ALL
  getAllVirtualMachinesFailure,
  getAllVirtualMachinesReset,
  getAllVirtualMachinesStart,
  getAllVirtualMachinesSuccess,
  // PUT
  putVirtualMachineFailure,
  putVirtualMachineReset,
  putVirtualMachineStart,
  putVirtualMachineSuccess,
} from './virtualMachineManager.actions';

import type {
  TGetVirtualMachineSuccess,
  TPutVirtualMachineSuccess,
  TGetAllVirtualMachinesSuccess,
} from './virtualMachineManager.typeDefs';

import { IDefaults } from '@redux/typedefs';

export interface IVirtualMachineState {
  // GET ONE
  getVirtualMachineData: null | TGetVirtualMachineSuccess;
  getVirtualMachineError: IDefaults['errorMessage'];
  getVirtualMachineState: IDefaults['state'];

  // GET ALL
  getAllVirtualMachinesData: null | TGetAllVirtualMachinesSuccess;
  getAllVirtualMachinesError: IDefaults['errorMessage'];
  getAllVirtualMachinesState: IDefaults['state'];

  // PUT
  putVirtualMachineData: null | TPutVirtualMachineSuccess;
  putVirtualMachineError: IDefaults['errorMessage'];
  putVirtualMachineState: IDefaults['state'];
}

const INITIAL_STATE: IVirtualMachineState = {
  // GET ONE
  getVirtualMachineData: null,
  getVirtualMachineError: null,
  getVirtualMachineState: null,

  // GET ALL
  getAllVirtualMachinesData: null,
  getAllVirtualMachinesError: null,
  getAllVirtualMachinesState: null,

  // PUT
  putVirtualMachineData: null,
  putVirtualMachineError: null,
  putVirtualMachineState: null,
};

// tslint:disable-next-line: no-unsafe-any tslint:disable-next-line: typedef
const VirtualMachineReducer = createReducer(INITIAL_STATE)
  // GET ONE

  .handleAction(
    getVirtualMachineStart,
    (state: IVirtualMachineState): IVirtualMachineState => ({
      ...state,
      getVirtualMachineData: null,
      getVirtualMachineError: null,
      getVirtualMachineState: 'isLoading',
    })
  )
  .handleAction(
    getVirtualMachineSuccess,
    (
      state: IVirtualMachineState,
      action: { payload: TGetVirtualMachineSuccess }
    ): IVirtualMachineState => ({
      ...state,
      getVirtualMachineData: action.payload,
      getVirtualMachineError: null,
      getVirtualMachineState: 'success',
    })
  )
  .handleAction(
    getVirtualMachineFailure,
    (
      state: IVirtualMachineState,
      action: { payload: IDefaults['errorMessage'] }
    ): IVirtualMachineState => ({
      ...state,
      getVirtualMachineData: null,
      getVirtualMachineError: action.payload,
      getVirtualMachineState: 'failure',
    })
  )
  .handleAction(
    getVirtualMachineReset,
    (state: IVirtualMachineState): IVirtualMachineState => ({
      ...state,
      getVirtualMachineData: null,
      getVirtualMachineError: null,
      getVirtualMachineState: null,
    })
  )

  // GET ALL

  .handleAction(
    getAllVirtualMachinesStart,
    (state: IVirtualMachineState): IVirtualMachineState => ({
      ...state,
      getAllVirtualMachinesData: null,
      getAllVirtualMachinesError: null,
      getAllVirtualMachinesState: 'isLoading',
    })
  )
  .handleAction(
    getAllVirtualMachinesSuccess,
    (
      state: IVirtualMachineState,
      action: { payload: TGetAllVirtualMachinesSuccess }
    ): IVirtualMachineState => ({
      ...state,
      getAllVirtualMachinesData: action.payload,
      getAllVirtualMachinesError: null,
      getAllVirtualMachinesState: 'success',
    })
  )
  .handleAction(
    getAllVirtualMachinesFailure,
    (
      state: IVirtualMachineState,
      action: { payload: IDefaults['errorMessage'] }
    ): IVirtualMachineState => ({
      ...state,
      getAllVirtualMachinesData: null,
      getAllVirtualMachinesError: action.payload,
      getAllVirtualMachinesState: 'failure',
    })
  )
  .handleAction(
    getAllVirtualMachinesReset,
    (state: IVirtualMachineState): IVirtualMachineState => ({
      ...state,
      getAllVirtualMachinesData: null,
      getAllVirtualMachinesError: null,
      getAllVirtualMachinesState: null,
    })
  )
  // GET ONE

  .handleAction(
    getVirtualMachineStart,
    (state: IVirtualMachineState): IVirtualMachineState => ({
      ...state,
      getVirtualMachineData: null,
      getVirtualMachineError: null,
      getVirtualMachineState: 'isLoading',
    })
  )
  .handleAction(
    getVirtualMachineSuccess,
    (
      state: IVirtualMachineState,
      action: { payload: TGetVirtualMachineSuccess }
    ): IVirtualMachineState => ({
      ...state,
      getVirtualMachineData: action.payload,
      getVirtualMachineError: null,
      getVirtualMachineState: 'success',
    })
  )
  .handleAction(
    getVirtualMachineFailure,
    (
      state: IVirtualMachineState,
      action: { payload: IDefaults['errorMessage'] }
    ): IVirtualMachineState => ({
      ...state,
      getVirtualMachineData: null,
      getVirtualMachineError: action.payload,
      getVirtualMachineState: 'failure',
    })
  )
  .handleAction(
    getVirtualMachineReset,
    (state: IVirtualMachineState): IVirtualMachineState => ({
      ...state,
      getVirtualMachineData: null,
      getVirtualMachineError: null,
      getVirtualMachineState: null,
    })
  )

  // PUT

  .handleAction(
    putVirtualMachineStart,
    (state: IVirtualMachineState): IVirtualMachineState => ({
      ...state,
      putVirtualMachineData: null,
      putVirtualMachineError: null,
      putVirtualMachineState: 'isLoading',
    })
  )
  .handleAction(
    putVirtualMachineSuccess,
    (
      state: IVirtualMachineState,
      action: { payload: TPutVirtualMachineSuccess }
    ): IVirtualMachineState => ({
      ...state,
      putVirtualMachineData: action.payload,
      putVirtualMachineError: null,
      putVirtualMachineState: 'success',
    })
  )
  .handleAction(
    putVirtualMachineFailure,
    (
      state: IVirtualMachineState,
      action: { payload: IDefaults['errorMessage'] }
    ): IVirtualMachineState => ({
      ...state,
      putVirtualMachineData: null,
      putVirtualMachineError: action.payload,
      putVirtualMachineState: 'failure',
    })
  )
  .handleAction(
    putVirtualMachineReset,
    (state: IVirtualMachineState): IVirtualMachineState => ({
      ...state,
      putVirtualMachineData: null,
      putVirtualMachineError: null,
      putVirtualMachineState: null,
    })
  );

export default VirtualMachineReducer;
