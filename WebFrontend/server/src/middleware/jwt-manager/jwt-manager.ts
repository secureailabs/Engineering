// This middleware saves the jwt token to the session store
// and removes it from the response so the browser never has access to it.
// It also adds the jwt token to the request when needed
import type { JWTManagerOptionsType } from './jwt-manager.types';

import catchAsync from '@utils/catchAsync';

export default (options?: JWTManagerOptionsType) => {
  // When we execute it before the request, we add the session's jwt
  // or we deny the request
  if (options && options.order && options.order == 'pre-request') {
    if (options.token && options.token == 'refresh') {
      return catchAsync(async (req, res, next) => {
        if (req.session.jwt) {
          req.body.refresh_token = req.session.jwt.refresh;
        }
        next();
      });
    } else {
      return catchAsync(async (req, res, next) => {
        if (req.session.jwt) {
          req.headers.authorization = 'Bearer ' + (req.session.jwt['access'])
        }
        next();
      });
    }
  }
  // If we execute it after the request, we store the jwt in the session's state
  // and we remove it from the response so we don't expose it to the browser.
  // we don't throw an error if we don't receive an jwt because it can sometimes be expected
  // E.g. : bad login credentials
  else {
    return catchAsync(async (req, res, next) => {
      if (res?.body?.access_token) {
        req.session.jwt = { access: res?.body?.access_token, refresh: res?.body?.refresh_token };
        delete res?.body?.access_token;
        delete res?.body?.refresh_token;
      }
      next();
    });
  }
};
