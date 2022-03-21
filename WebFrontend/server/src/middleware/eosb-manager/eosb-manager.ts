// This middleware saves the eosb token to the session store
// and removes it from the response so the browser never has access to it.
// It also adds the eosb token to the request when needed
import type { EOSBManagerOptionsType } from './eosb-manager.types';

import catchAsync from '@utils/catchAsync';

export default (options?: EOSBManagerOptionsType) => {
  // When we execute it before the request, we add the session's eosb
  // or we deny the request
  if (options && options.order && options.order == 'pre-request') {
    if (options.token && options.token == 'IEosb') {
      return catchAsync(async (req, res, next) => {
        if (req.session.Eosb) {
          req.body.IEosb = req.session.Eosb;
        }
        next();
      });
    } else {
      return catchAsync(async (req, res, next) => {
        if (req.session.Eosb) {
          req.body.Eosb = req.session.Eosb;
        }
        next();
      });
    }
  }
  // If we execute it after the request, we store the eosb in the session's state
  // and we remove it from the response so we don't expose it to the browser.
  // we don't throw an error if we don't receive an eosb because it can sometimes be expected
  // E.g. : bad login credentials
  else {
    return catchAsync(async (req, res, next) => {
      if (res?.body?.Eosb) {
        req.session.Eosb = res?.body?.Eosb;
        delete res?.body?.Eosb;
      }
      next();
    });
  }
};
