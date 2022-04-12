import { EmptyActionCreator } from 'typesafe-actions';

export interface AppProps {
  checkUserSession(): EmptyActionCreator<'user/CHECK_USER_SESSION'>;
  checkUserSessionAsync(): EmptyActionCreator<'user/CHECK_USER_SESSION_ASYNC'>;
}
