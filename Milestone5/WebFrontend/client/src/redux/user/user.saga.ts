import { takeLatest, put, all, call } from 'redux-saga/effects';

import {
  signInSuccess,
  signInFailure,
  signOutSuccess,
  signOutFailure,
  noUserSession,
  signInStart,
  checkUserSession,
  signOutStart,
  checkUserSessionAsync,
  // SIGN UP
  signUpFailure,
  signUpStart,
  signUpSuccess,
} from './user.actions';

import { userLogin, checkAuth, userSignup, logOut, me } from './user.apis';

import { setToken, removeToken, fetchToken } from './user.utils';

import { IUserData } from './user.typeDefs';
import { AxiosResponse } from 'axios';

// action gets passed it
export function* signUp({ payload }: ReturnType<typeof signUpStart>) {
  try {
    const {
      data: { data },
    } = (yield userSignup(payload)) as AxiosResponse<{
      data: { user: IUserData };
      token: string;
    }>;
    // The backend returns status 204 when the fields are valid but the org already exists

    yield put(signUpSuccess());
  } catch (error) {
    yield put(signUpFailure(error?.response?.data));
  }
}
export function* onSignUpStart() {
  yield takeLatest(signUpStart, signUp);
}

// action gets passed it
export function* signIn({
  payload: { email, password },
}: ReturnType<typeof signInStart>) {
  try {
    (yield userLogin(email, password)) as AxiosResponse<{
      data: { user: IUserData };
      token: string;
    }>;
    const { data } = yield checkAuth();
    yield put(signInSuccess(data));
  } catch (error) {
    console.log(error);
    yield put(signInFailure(error?.response?.data));
  }
}
export function* onSignInStart() {
  yield takeLatest(signInStart, signIn);
}

export function* isUserAuthenticatedAsync() {
  try {
    let { data } = yield me();
    yield put(signInSuccess(data));
  } catch (error) {
    yield put(noUserSession());
    //AND DON'T FORGET TO UNCOMMENT THE CODE BELOW
    yield removeToken();
  }
}

export function* isUserAuthenticated() {
  try {
    let { data } = yield me();
    yield put(signInSuccess(data));
  } catch (error) {
    yield put(noUserSession());
    //AND DON'T FORGET TO UNCOMMENT THE CODE BELOW
    yield removeToken();
  }
}

export function* onCheckUserSession() {
  yield takeLatest(checkUserSession, isUserAuthenticated);
}

export function* onCheckUserSessionAsync() {
  yield takeLatest(checkUserSessionAsync, isUserAuthenticatedAsync);
}

export function* signOut() {
  try {
    yield logOut();
    yield removeToken();
    yield put(signOutSuccess());
  } catch (error) {
    yield put(signOutFailure(error));
  }
}
export function* onSignOutStart() {
  yield takeLatest(signOutStart, signOut);
}

function* userSagas() {
  yield all([
    call(onSignInStart),
    call(onCheckUserSession),
    call(onSignOutStart),
    call(onSignUpStart),
    call(onSignOutStart),
    call(onCheckUserSessionAsync),
  ]);
}

export default userSagas;
