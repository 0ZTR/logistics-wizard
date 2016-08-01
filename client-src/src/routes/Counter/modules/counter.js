import { delay } from 'redux-saga';
import { take, put, select } from 'redux-saga/effects';
// ------------------------------------
// Constants
// ------------------------------------
export const COUNTER_INCREMENT = 'COUNTER_INCREMENT';
export const COUNTER_DOUBLE = 'COUNTER_DOUBLE';

// ------------------------------------
// Actions
// ------------------------------------
export const increment = (value = 1) => ({
  type: COUNTER_INCREMENT,
  payload: value,
});

export const double = () => ({
  type: COUNTER_DOUBLE,
});

export const actions = {
  increment,
  double,
};

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
  [COUNTER_INCREMENT]: (state, action) => state + action.payload,
};

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = 0;
export const counterReducer = (state = initialState, action) => {
  const handler = ACTION_HANDLERS[action.type];

  return handler ? handler(state, action) : state;
};
export default counterReducer;

// ------------------------------------
// Sagas
// ------------------------------------

export function *doubleAsync() {
  while (true) {
    yield take(COUNTER_DOUBLE);
    const state = yield select();
    yield delay(200); // Simulate an async call
    yield put(actions.increment(state.counter));
  }
}

export const sagas = [
  doubleAsync,
];
