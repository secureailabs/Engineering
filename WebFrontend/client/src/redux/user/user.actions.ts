import { ActionType, createAction } from 'typesafe-actions';

import { IEmailAndPassword, IPostUserStart } from './user.typeDefs';

export type userAction =
  | ActionType<typeof checkUserSession>
  | ActionType<typeof checkUserSessionAsync>
  | ActionType<typeof noUserSession>
  // SIGN IN
  | ActionType<typeof signInStart>
  | ActionType<typeof signInSuccess>
  | ActionType<typeof signInFailure>
  | ActionType<typeof signInReset>
  // SIGN UP
  | ActionType<typeof signUpStart>
  | ActionType<typeof signUpSuccess>
  | ActionType<typeof signUpFailure>
  | ActionType<typeof signUpReset>
  // SIGN OUT
  | ActionType<typeof signOutStart>
  | ActionType<typeof signOutSuccess>
  | ActionType<typeof signOutFailure>;

// Used during /me request (checks if jwt is valid)
export const checkUserSession = createAction(
  // Type
  'user/CHECK_USER_SESSION'
)();
// Used during /me request (checks if jwt is valid)
export const checkUserSessionAsync = createAction(
  // Type
  'user/CHECK_USER_SESSION_ASYNC'
)();
// No user session (self exmplanatory)
export const noUserSession = createAction(
  // Type
  'user/NO_USER_SESSION'
)();

// EMAIL AND PASSWORD AUTHENTICATION

export const signInStart = createAction(
  'user/SIGN_IN_START',
  (data: IEmailAndPassword) => data
)();
export const signInSuccess = createAction(
  'user/SIGN_IN_SUCCESS',
  (data) => data
)();
export const signInFailure = createAction(
  'user/SIGN_IN_FAILURE',
  (error) => error
)();
export const signInReset = createAction('user/SIGN_IN_RESET')();

// SIGN UP

export const signUpStart = createAction(
  'user/SIGN_UP_START',
  (data: IPostUserStart) => data
)();
export const signUpSuccess = createAction('user/SIGN_UP_SUCCESS')();
export const signUpFailure = createAction(
  'user/SIGN_UP_FAILURE',
  (error) => error
)();
export const signUpReset = createAction('user/SIGN_UP_RESET')();

// REMOVES JWT TOKEN
export const signOutStart = createAction('user/SIGN_OUT_START')();
export const signOutSuccess = createAction('user/SIGN_OUT_SUCCESS')();
export const signOutFailure = createAction(
  'user/SIGN_OUT_FAILURE',
  (error) => error
)();
