import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import createSagaMiddleware from 'redux-saga';

import { persistStore } from 'redux-persist';

import rootSaga from './root-saga';

import rootReducer from './root-reducer';

const sagaMiddleware = createSagaMiddleware();

const middleware = [thunk, sagaMiddleware];

const dev = () => {
  if (import.meta.env.MODE === 'development') {
    return compose(
      applyMiddleware(...middleware),
      //@ts-ignore
      window.__REDUX_DEVTOOLS_EXTENSION__ &&
        //@ts-ignore
        window.__REDUX_DEVTOOLS_EXTENSION__()
    );
  }
  return applyMiddleware(...middleware);
};

export const store = createStore(rootReducer, dev());
sagaMiddleware.run(rootSaga);

export const persistor = persistStore(store);

export default { store, persistor };
