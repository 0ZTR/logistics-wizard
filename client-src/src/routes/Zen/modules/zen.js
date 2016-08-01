import { call, take, put } from 'redux-saga/effects';
// ------------------------------------
// Constants
// ------------------------------------
export const REQUEST_ZEN = 'REQUEST_ZEN';
export const RECEIVE_ZEN = 'RECEIVE_ZEN';
export const SAVE_CURRENT_ZEN = 'SAVE_CURRENT_ZEN';

// ------------------------------------
// Actions
// ------------------------------------
export const requestZen = () => ({
  type: REQUEST_ZEN,
});

let availableId = 0;
export const receiveZen = (value) => ({
  type: RECEIVE_ZEN,
  payload: {
    value,
    id: availableId++,
  },
});

export const saveCurrentZen = () => ({
  type: SAVE_CURRENT_ZEN,
});

export const actions = {
  requestZen,
  receiveZen,
  saveCurrentZen,
};

// ------------------------------------
// Action Handlers
// ------------------------------------
const ZEN_ACTION_HANDLERS = {
  [RECEIVE_ZEN]: (state, action) => ({
    ...state,
    zens: state.zens.concat(action.payload),
    current: action.payload.id,
  }),
  [SAVE_CURRENT_ZEN]: (state) => (
    state.current != null
      ? ({ ...state, saved: state.saved.concat(state.current) })
      : state
  ),
};

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  current: null,
  zens: [],
  saved: [],
};

const zenReducer = (state = initialState, action) => {
  const handler = ZEN_ACTION_HANDLERS[action.type];

  return handler ? handler(state, action) : state;
};
export default zenReducer;

// ------------------------------------
// Sagas
// ------------------------------------

const fetchZen = () =>
  fetch('https://api.github.com/zen')
    .then(data => data.text());

export function *fetchZenAsync() {
  while (true) {
    yield take(REQUEST_ZEN);
    const text = yield call(fetchZen);
    yield put(actions.receiveZen(text));
  }
}

export const sagas = [
  fetchZenAsync,
];
