import { createReducer } from 'typesafe-actions';

import {
  // POST
  postAzureTemplateStart,
  postAzureTemplateSuccess,
  postAzureTemplateFailure,
  postAzureTemplateReset,

  // GET ALL
  getAllAzureTemplatesStart,
  getAllAzureTemplatesSuccess,
  getAllAzureTemplatesFailure,
  getAllAzureTemplatesReset,

  // GET ONE
  getAzureTemplateStart,
  getAzureTemplateSuccess,
  getAzureTemplateFailure,
  getAzureTemplateReset,

  // PUT UPDATE
  putUpdateAzureTemplateStart,
  putUpdateAzureTemplateSuccess,
  putUpdateAzureTemplateFailure,
  putUpdateAzureTemplateReset,

  // PUT UPDATE SECRET
  putUpdateAzureSecretStart,
  putUpdateAzureSecretSuccess,
  putUpdateAzureSecretFailure,
  putUpdateAzureSecretReset,

  // DELETE
  deleteAzureTemplateStart,
  deleteAzureTemplateSuccess,
  deleteAzureTemplateFailure,
  deleteAzureTemplateReset,
} from './azureTemplate.actions';

import type {
  TPostAzureTemplateSuccess,
  TGetAllAzureTemplatesSuccess,
  TGetAzureTemplateSuccess,
  TPutUpdateAzureTemplateSuccess,
  TDeleteAzureTemplateSuccess,
} from './azureTemplate.typesDefs';

import { IDefaults } from '@redux/typedefs';

export interface IAzureTemplateState {
  // POST
  postAzureTemplateData: TPostAzureTemplateSuccess | null;
  postAzureTemplateError: IDefaults['error'];
  postAzureTemplateState: IDefaults['state'];

  // GET ALL
  getAllAzureTemplatesData: TGetAllAzureTemplatesSuccess | null;
  getAllAzureTemplatesError: IDefaults['error'];
  getAllAzureTemplatesState: IDefaults['state'];

  // GET ONE
  getAzureTemplateData: TGetAzureTemplateSuccess | null;
  getAzureTemplateError: IDefaults['error'];
  getAzureTemplateState: IDefaults['state'];

  // PUT PUTUPDATE
  putUpdateAzureTemplateData: TPutUpdateAzureTemplateSuccess | null;
  putUpdateAzureTemplateError: IDefaults['error'];
  putUpdateAzureTemplateState: IDefaults['state'];

  // PUT PUTUPDATE SECRET
  putUpdateAzureSecretData: TPutUpdateAzureTemplateSuccess | null;
  putUpdateAzureSecretError: IDefaults['error'];
  putUpdateAzureSecretState: IDefaults['state'];

  // DELETE
  deleteAzureTemplateData: TDeleteAzureTemplateSuccess | null;
  deleteAzureTemplateError: IDefaults['error'];
  deleteAzureTemplateState: IDefaults['state'];
}

const INITIAL_STATE: IAzureTemplateState = {
  // POST
  postAzureTemplateData: null,
  postAzureTemplateError: null,
  postAzureTemplateState: null,

  // GET ALL
  getAllAzureTemplatesData: null,
  getAllAzureTemplatesError: null,
  getAllAzureTemplatesState: null,

  // GET ONE
  getAzureTemplateData: null,
  getAzureTemplateError: null,
  getAzureTemplateState: null,

  // PUT PUTUPDATE
  putUpdateAzureTemplateData: null,
  putUpdateAzureTemplateError: null,
  putUpdateAzureTemplateState: null,

  // PUT PUTUPDATE SECRET
  putUpdateAzureSecretData: null,
  putUpdateAzureSecretError: null,
  putUpdateAzureSecretState: null,

  // DELETE
  deleteAzureTemplateData: null,
  deleteAzureTemplateError: null,
  deleteAzureTemplateState: null,
};

const azureTemplateReducer = createReducer(INITIAL_STATE)
  // POST

  .handleAction(postAzureTemplateStart, (state: IAzureTemplateState) => ({
    ...state,
    postAzureTemplateData: null,
    postAzureTemplateError: null,
    postAzureTemplateState: 'isLoading',
  }))
  .handleAction(
    postAzureTemplateSuccess,
    (
      state: IAzureTemplateState,
      action: { payload: TPostAzureTemplateSuccess }
    ) => ({
      ...state,
      postAzureTemplateData: action.payload,
      postAzureTemplateError: null,
      postAzureTemplateState: 'success',
    })
  )
  .handleAction(
    postAzureTemplateFailure,
    (state: IAzureTemplateState, action: { payload: IDefaults['error'] }) => ({
      ...state,
      postAzureTemplateData: null,
      postAzureTemplateError: action.payload,
      postAzureTemplateState: 'failure',
    })
  )
  .handleAction(postAzureTemplateReset, (state: IAzureTemplateState) => ({
    ...state,
    postAzureTemplateData: null,
    postAzureTemplateError: null,
    postAzureTemplateState: null,
  }))

  // GET ALL

  .handleAction(getAllAzureTemplatesStart, (state: IAzureTemplateState) => ({
    ...state,
    getAllAzureTemplatesData: null,
    getAllAzureTemplatesError: null,
    getAllAzureTemplatesState: 'isLoading',
  }))
  .handleAction(
    getAllAzureTemplatesSuccess,
    (
      state: IAzureTemplateState,
      action: { payload: TGetAllAzureTemplatesSuccess }
    ) => ({
      ...state,
      getAllAzureTemplatesData: action.payload,
      getAllAzureTemplatesError: null,
      getAllAzureTemplatesState: 'success',
    })
  )
  .handleAction(
    getAllAzureTemplatesFailure,
    (state: IAzureTemplateState, action: { payload: IDefaults['error'] }) => ({
      ...state,
      getAllAzureTemplatesData: null,
      getAllAzureTemplatesError: action.payload,
      getAllAzureTemplatesState: 'failure',
    })
  )
  .handleAction(getAllAzureTemplatesReset, (state: IAzureTemplateState) => ({
    ...state,
    getAllAzureTemplatesData: null,
    getAllAzureTemplatesError: null,
    getAllAzureTemplatesState: null,
  }))

  // GET ONE

  .handleAction(getAzureTemplateStart, (state: IAzureTemplateState) => ({
    ...state,
    getAzureTemplateData: null,
    getAzureTemplateError: null,
    getAzureTemplateState: 'isLoading',
  }))
  .handleAction(
    getAzureTemplateSuccess,
    (
      state: IAzureTemplateState,
      action: { payload: TGetAzureTemplateSuccess }
    ) => ({
      ...state,
      getAzureTemplateData: action.payload,
      getAzureTemplateError: null,
      getAzureTemplateState: 'success',
    })
  )
  .handleAction(
    getAzureTemplateFailure,
    (state: IAzureTemplateState, action: { payload: IDefaults['error'] }) => ({
      ...state,
      getAzureTemplateData: null,
      getAzureTemplateError: action.payload,
      getAzureTemplateState: 'failure',
    })
  )
  .handleAction(getAzureTemplateReset, (state: IAzureTemplateState) => ({
    ...state,
    getAzureTemplateData: null,
    getAzureTemplateError: null,
    getAzureTemplateState: null,
  }))

  // PUT PUTUPDATE TEMPLATE

  .handleAction(
    putUpdateAzureTemplateStart,
    (state: IAzureTemplateState): IAzureTemplateState => ({
      ...state,
      putUpdateAzureTemplateData: null,
      putUpdateAzureTemplateError: null,
      putUpdateAzureTemplateState: 'isLoading',
    })
  )
  .handleAction(
    putUpdateAzureTemplateSuccess,
    (
      state: IAzureTemplateState,
      action: { payload: TPutUpdateAzureTemplateSuccess }
    ): IAzureTemplateState => ({
      ...state,
      putUpdateAzureTemplateData: action.payload,
      putUpdateAzureTemplateError: null,
      putUpdateAzureTemplateState: 'success',
    })
  )
  .handleAction(
    putUpdateAzureTemplateFailure,
    (
      state: IAzureTemplateState,
      action: { payload: IDefaults['error'] }
    ): IAzureTemplateState => ({
      ...state,
      putUpdateAzureTemplateData: null,
      putUpdateAzureTemplateError: action.payload,
      putUpdateAzureTemplateState: 'failure',
    })
  )
  .handleAction(
    putUpdateAzureTemplateReset,
    (state: IAzureTemplateState): IAzureTemplateState => ({
      ...state,
      putUpdateAzureTemplateData: null,
      putUpdateAzureTemplateError: null,
      putUpdateAzureTemplateState: null,
    })
  )

  // PUT PUTUPDATE SECRET

  .handleAction(
    putUpdateAzureSecretStart,
    (state: IAzureTemplateState): IAzureTemplateState => ({
      ...state,
      putUpdateAzureSecretData: null,
      putUpdateAzureSecretError: null,
      putUpdateAzureSecretState: 'isLoading',
    })
  )
  .handleAction(
    putUpdateAzureSecretSuccess,
    (
      state: IAzureTemplateState,
      action: { payload: TPutUpdateAzureTemplateSuccess }
    ): IAzureTemplateState => ({
      ...state,
      putUpdateAzureSecretData: action.payload,
      putUpdateAzureSecretError: null,
      putUpdateAzureSecretState: 'success',
    })
  )
  .handleAction(
    putUpdateAzureSecretFailure,
    (
      state: IAzureTemplateState,
      action: { payload: IDefaults['error'] }
    ): IAzureTemplateState => ({
      ...state,
      putUpdateAzureSecretData: null,
      putUpdateAzureSecretError: action.payload,
      putUpdateAzureSecretState: 'failure',
    })
  )
  .handleAction(
    putUpdateAzureSecretReset,
    (state: IAzureTemplateState): IAzureTemplateState => ({
      ...state,
      putUpdateAzureSecretData: null,
      putUpdateAzureSecretError: null,
      putUpdateAzureSecretState: null,
    })
  )

  // DELETE

  .handleAction(
    deleteAzureTemplateStart,
    (state: IAzureTemplateState): IAzureTemplateState => ({
      ...state,
      deleteAzureTemplateData: null,
      deleteAzureTemplateError: null,
      deleteAzureTemplateState: 'isLoading',
    })
  )
  .handleAction(
    deleteAzureTemplateSuccess,
    (
      state: IAzureTemplateState,
      action: { payload: TDeleteAzureTemplateSuccess }
    ): IAzureTemplateState => ({
      ...state,
      deleteAzureTemplateData: action.payload,
      deleteAzureTemplateError: null,
      deleteAzureTemplateState: 'success',
    })
  )
  .handleAction(
    deleteAzureTemplateFailure,
    (
      state: IAzureTemplateState,
      action: { payload: IDefaults['error'] }
    ): IAzureTemplateState => ({
      ...state,
      deleteAzureTemplateData: null,
      deleteAzureTemplateError: action.payload,
      deleteAzureTemplateState: 'failure',
    })
  )
  .handleAction(
    deleteAzureTemplateReset,
    (state: IAzureTemplateState): IAzureTemplateState => ({
      ...state,
      deleteAzureTemplateData: null,
      deleteAzureTemplateError: null,
      deleteAzureTemplateState: null,
    })
  );

export default azureTemplateReducer;
