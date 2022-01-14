import { createReducer } from 'typesafe-actions';

import {
    // POST
    registerAzureTemplateStart,
    registerAzureTemplateSuccess,
    registerAzureTemplateFailure,
    registerAzureTemplateReset,

    // GET ALL
    listAzureTemplatesStart,
    listAzureTemplatesSuccess,
    listAzureTemplatesFailure,
    listAzureTemplatesReset,

    // GET ONE
    pullAzureTemplateStart,
    pullAzureTemplateSuccess,
    pullAzureTemplateFailure,
    pullAzureTemplateReset,

    // PUT UPDATE
    updateAzureTemplateStart,
    updateAzureTemplateSuccess,
    updateAzureTemplateFailure,
    updateAzureTemplateReset,

    // PUT UPDATE
    updateAzureSecretStart,
    updateAzureSecretSuccess,
    updateAzureSecretFailure,
    updateAzureSecretReset,

    // DELETE
    deleteAzureTemplateStart,
    deleteAzureTemplateSuccess,
    deleteAzureTemplateFailure,
    deleteAzureTemplateReset,
} from './azureTemplatesManager.actions'

import type {
    TRegisterAzureTemplateSuccess,
    TListAzureTemplatesSuccess,
    TPullAzureTemplateSuccess,
    TUpdateAzureTemplateSuccess,
    TDeleteAzureTemplateSuccess,
} from './azureTemplatesManager.typesDefs'

import { IDefaults } from '@redux/typedefs';

export interface IAzureTemplatesManagerState {
    // POST
    registerAzureTemplateData: TRegisterAzureTemplateSuccess | null;
    registerAzureTemplateError: IDefaults['error'];
    registerAzureTemplateState: IDefaults['state']

    // GET ALL
    listAzureTemplatesData: TListAzureTemplatesSuccess | null;
    listAzureTemplatesError: IDefaults['error'];
    listAzureTemplatesState: IDefaults['state'];

    // GET ONE
    pullAzureTemplateData: TPullAzureTemplateSuccess | null;
    pullAzureTemplateError: IDefaults['error'];
    pullAzureTemplateState: IDefaults['state'];

    // PUT UPDATE
    updateAzureTemplateData: TUpdateAzureTemplateSuccess | null;
    updateAzureTemplateError: IDefaults['error'];
    updateAzureTemplateState: IDefaults['state'];

    // PUT UPDATE SECRET
    updateAzureSecretData: TUpdateAzureTemplateSuccess | null;
    updateAzureSecretError: IDefaults['error'];
    updateAzureSecretState: IDefaults['state'];

    // DELETE
    deleteAzureTemplateData: TDeleteAzureTemplateSuccess | null;
    deleteAzureTemplateError: IDefaults['error'];
    deleteAzureTemplateState: IDefaults['state'];
}

const INITIAL_STATE: IAzureTemplatesManagerState = {
    // POST
    registerAzureTemplateData: null,
    registerAzureTemplateError: null,
    registerAzureTemplateState: null,

    // GET ALL
    listAzureTemplatesData: null,
    listAzureTemplatesError: null,
    listAzureTemplatesState: null,

    // GET ONE
    pullAzureTemplateData: null,
    pullAzureTemplateError: null,
    pullAzureTemplateState: null,

    // PUT UPDATE
    updateAzureTemplateData: null,
    updateAzureTemplateError: null,
    updateAzureTemplateState: null,

    // PUT UPDATE SECRET
    updateAzureSecretData: null,
    updateAzureSecretError: null,
    updateAzureSecretState: null,


    // DELETE
    deleteAzureTemplateData: null,
    deleteAzureTemplateError: null,
    deleteAzureTemplateState: null,
}

const azureTemplatesManagerReducer = createReducer(INITIAL_STATE)
    // POST

    .handleAction(
        registerAzureTemplateStart,
    (state: IAzureTemplatesManagerState) => ({
        ...state,
        registerAzureTemplateData: null,
        registerAzureTemplateError: null,
        registerAzureTemplateState: 'isLoading'
      })
    )
    .handleAction(
        registerAzureTemplateSuccess,
        (
          state: IAzureTemplatesManagerState,
          action: { payload: TRegisterAzureTemplateSuccess }
        ) => ({
            ...state,
            registerAzureTemplateData: action.payload,
            registerAzureTemplateError: null,
            registerAzureTemplateState: 'success'
          })
    )
    .handleAction(
        registerAzureTemplateFailure,
        (
          state: IAzureTemplatesManagerState,
          action: { payload: IDefaults['error'] }
          ) => ({
              ...state,
              registerAzureTemplateData: null,
              registerAzureTemplateError: action.payload,
              registerAzureTemplateState: 'failure'
            })
    )
    .handleAction(
        registerAzureTemplateReset,
        (state: IAzureTemplatesManagerState) => ({
            ...state,
            registerAzureTemplateData: null,
            registerAzureTemplateError: null,
            registerAzureTemplateState: null
          })
    )

    // GET ALL

    .handleAction(
        listAzureTemplatesStart,
    (state: IAzureTemplatesManagerState) => ({
        ...state,
        listAzureTemplatesData: null,
        listAzureTemplatesError: null,
        listAzureTemplatesState: 'isLoading'
      })
    )
    .handleAction(
        listAzureTemplatesSuccess,
        (
          state: IAzureTemplatesManagerState,
          action: { payload: TListAzureTemplatesSuccess }
        ) => ({
            ...state,
            listAzureTemplatesData: action.payload,
            listAzureTemplatesError: null,
            listAzureTemplatesState: 'success'
          })
    )
    .handleAction(
        listAzureTemplatesFailure,
        (
          state: IAzureTemplatesManagerState,
          action: { payload: IDefaults['error'] }
          ) => ({
              ...state,
              listAzureTemplatesData: null,
              listAzureTemplatesError: action.payload,
              listAzureTemplatesState: 'failure'
            })
    )
    .handleAction(
        listAzureTemplatesReset,
        (state: IAzureTemplatesManagerState) => ({
            ...state,
            listAzureTemplatesData: null,
            listAzureTemplatesError: null,
            listAzureTemplatesState: null
          })
    )

    // GET ONE

    .handleAction(
      pullAzureTemplateStart,
  (state: IAzureTemplatesManagerState) => ({
      ...state,
      pullAzureTemplateData: null,
      pullAzureTemplateError: null,
      pullAzureTemplateState: 'isLoading'
    })
  )
  .handleAction(
      pullAzureTemplateSuccess,
      (
        state: IAzureTemplatesManagerState,
        action: { payload: TPullAzureTemplateSuccess }
      ) => ({
          ...state,
          pullAzureTemplateData: action.payload,
          pullAzureTemplateError: null,
          pullAzureTemplateState: 'success'
        })
  )
  .handleAction(
      pullAzureTemplateFailure,
      (
        state: IAzureTemplatesManagerState,
        action: { payload: IDefaults['error'] }
        ) => ({
            ...state,
            pullAzureTemplateData: null,
            pullAzureTemplateError: action.payload,
            pullAzureTemplateState: 'failure'
          })
  )
  .handleAction(
      pullAzureTemplateReset,
      (state: IAzureTemplatesManagerState) => ({
          ...state,
          pullAzureTemplateData: null,
          pullAzureTemplateError: null,
          pullAzureTemplateState: null
        })
  )

  // PUT UPDATE TEMPLATE

  .handleAction(
    updateAzureTemplateStart,
    (state: IAzureTemplatesManagerState): IAzureTemplatesManagerState => ({
      ...state,
      updateAzureTemplateData: null,
      updateAzureTemplateError: null,
      updateAzureTemplateState: 'isLoading',
    })
  )
  .handleAction(
    updateAzureTemplateSuccess,
    (
      state: IAzureTemplatesManagerState,
      action: { payload: TUpdateAzureTemplateSuccess }
    ): IAzureTemplatesManagerState => ({
      ...state,
      updateAzureTemplateData: action.payload,
      updateAzureTemplateError: null,
      updateAzureTemplateState: 'success',
    })
  )
  .handleAction(
    updateAzureTemplateFailure,
    (
      state: IAzureTemplatesManagerState,
      action: { payload: IDefaults['error'] }
    ): IAzureTemplatesManagerState => ({
      ...state,
      updateAzureTemplateData: null,
      updateAzureTemplateError: action.payload,
      updateAzureTemplateState: 'failure',
    })
  )
  .handleAction(
    updateAzureTemplateReset,
    (state: IAzureTemplatesManagerState): IAzureTemplatesManagerState => ({
      ...state,
      updateAzureTemplateData: null,
      updateAzureTemplateError: null,
      updateAzureTemplateState: null,
    })
  )

  // PUT UPDATE SECRET

  .handleAction(
    updateAzureSecretStart,
    (state: IAzureTemplatesManagerState): IAzureTemplatesManagerState => ({
      ...state,
      updateAzureSecretData: null,
      updateAzureSecretError: null,
      updateAzureSecretState: 'isLoading',
    })
  )
  .handleAction(
    updateAzureSecretSuccess,
    (
      state: IAzureTemplatesManagerState,
      action: { payload: TUpdateAzureTemplateSuccess }
    ): IAzureTemplatesManagerState => ({
      ...state,
      updateAzureSecretData: action.payload,
      updateAzureSecretError: null,
      updateAzureSecretState: 'success',
    })
  )
  .handleAction(
    updateAzureSecretFailure,
    (
      state: IAzureTemplatesManagerState,
      action: { payload: IDefaults['error'] }
    ): IAzureTemplatesManagerState => ({
      ...state,
      updateAzureSecretData: null,
      updateAzureSecretError: action.payload,
      updateAzureSecretState: 'failure',
    })
  )
  .handleAction(
    updateAzureSecretReset,
    (state: IAzureTemplatesManagerState): IAzureTemplatesManagerState => ({
      ...state,
      updateAzureSecretData: null,
      updateAzureSecretError: null,
      updateAzureSecretState: null,
    })
  )

  // DELETE

  .handleAction(
    deleteAzureTemplateStart,
    (state: IAzureTemplatesManagerState): IAzureTemplatesManagerState => ({
      ...state,
      deleteAzureTemplateData: null,
      deleteAzureTemplateError: null,
      deleteAzureTemplateState: 'isLoading',
    })
  )
  .handleAction(
    deleteAzureTemplateSuccess,
    (
      state: IAzureTemplatesManagerState,
      action: { payload: TDeleteAzureTemplateSuccess }
    ): IAzureTemplatesManagerState => ({
      ...state,
      deleteAzureTemplateData: action.payload,
      deleteAzureTemplateError: null,
      deleteAzureTemplateState: 'success',
    })
  )
  .handleAction(
    deleteAzureTemplateFailure,
    (
      state: IAzureTemplatesManagerState,
      action: { payload: IDefaults['error'] }
    ): IAzureTemplatesManagerState => ({
      ...state,
      deleteAzureTemplateData: null,
      deleteAzureTemplateError: action.payload,
      deleteAzureTemplateState: 'failure',
    })
  )
  .handleAction(
    deleteAzureTemplateReset,
    (state: IAzureTemplatesManagerState): IAzureTemplatesManagerState => ({
      ...state,
      deleteAzureTemplateData: null,
      deleteAzureTemplateError: null,
      deleteAzureTemplateState: null,
    })
  )

export default azureTemplatesManagerReducer