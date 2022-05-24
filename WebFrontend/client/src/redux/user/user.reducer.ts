import { createReducer } from 'typesafe-actions';

import type { IUserData } from './user.typeDefs';

import {
  // SESSION
  checkUserSession,
  noUserSession,
  // SIGN IN START
  signInStart,
  signInSuccess,
  signInFailure,
  signInReset,
  // SIGN OUT
  signOutStart,
  signOutSuccess,
  signOutFailure,
  // SIGN UP
  signUpStart,
  signUpFailure,
  signUpReset,
  signUpSuccess,
} from './user.actions';

import { IDefaults } from '@app/redux/typedefs';

export interface IUserState {
  userData: IUserData;
  userError: IDefaults['error'];
  userState: IDefaults['state'] | 'noUserSession' | 'signup-success';
}

const INITIAL_STATE: IUserState = {
  // DELETE
  userData: null,
  userError: null,
  userState: null,
};

const userReducer = createReducer(INITIAL_STATE)
  // CHECK USER SESSION
  .handleAction(
    checkUserSession,
    (state: IUserState): IUserState => ({
      ...state,
      userData: null,
      userState: 'isLoading',
      userError: null,
    })
  )
  // NO USER SESSION
  .handleAction(
    noUserSession,
    (state: IUserState): IUserState => ({
      ...state,
      userData: null,
      userState: 'noUserSession',
      userError: null,
    })
  )

  //SIGN IN
  .handleAction(
    signInStart,
    (state: IUserState): IUserState => ({
      ...state,
      userData: null,
      userState: 'isLoading',
      userError: null,
    })
  )
  .handleAction(
    signInSuccess,
    (
      state: IUserState,
      action: { payload: IUserState['userData'] }
    ): IUserState => ({
      ...state,
      userData: action.payload,
      userState: 'success',
      userError: null,
    })
  )
  .handleAction(
    signInFailure,
    (
      state: IUserState,
      action: { payload: IDefaults['error'] }
    ): IUserState => ({
      ...state,
      userData: null,
      userState: 'failure',
      userError: action.payload,
    })
  )
  .handleAction(
    signInReset,
    (state: IUserState): IUserState => ({
      ...state,
      userData: null,
      userState: 'noUserSession',
      userError: null,
    })
  )

  //SIGN UP
  .handleAction(
    signUpStart,
    (state: IUserState): IUserState => ({
      ...state,
      userData: null,
      userState: 'isLoading',
      userError: null,
    })
  )
  .handleAction(
    signUpSuccess,
    (
      state: IUserState,
      action: { payload: IUserState['userData'] }
    ): IUserState => ({
      ...state,
      userState: 'signup-success',
      userError: null,
    })
  )
  .handleAction(
    signUpFailure,
    (
      state: IUserState,
      action: { payload: IDefaults['error'] }
    ): IUserState => ({
      ...state,
      userData: null,
      userState: 'failure',
      userError: action.payload,
    })
  )
  .handleAction(
    signUpReset,
    (state: IUserState): IUserState => ({
      ...state,
      userData: null,
      userState: 'noUserSession',
      userError: null,
    })
  )

  // SIGN OUT
  .handleAction(
    signOutStart,
    (state: IUserState): IUserState => ({
      ...state,
      userData: null,
      userState: 'isLoading',
      userError: null,
    })
  )
  .handleAction(
    signOutSuccess,
    (state: IUserState): IUserState => ({
      ...state,
      userData: null,
      userState: 'noUserSession',
      userError: null,
    })
  )
  .handleAction(
    signOutFailure,
    (
      state: IUserState,
      action: { payload: IDefaults['error'] }
    ): IUserState => ({
      ...state,
      userData: null,
      userState: 'failure',
      userError: action.payload,
    })
  );

export default userReducer;
