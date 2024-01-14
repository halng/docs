# Part 2: Redux Toolkit App Structure

* We can create a `Redux` store using the *Redux Toolkit* `configureStore` API
  * `configureStore` accepts a `reducer` function as a named argument
  * `configureStore` automatically sets up the store with good default settings

* Redux logic is typically organized into files called "slice"
  * A `slice` contains the reducer logic and actions related to a specific feature / section of Redux state
  * Redux Toolkit's `createSlice` API generates action creators and action types for each individual reducer function you provide.

* Redux reducer must follow specific rules
  * *Should only calculate a new state value based on the `state` and `action` arguments*
  * *Must make **immutable updates** by copying the existing state*
  * *Cannot contain any asynchronous logic or other **side effects***
  * *Redux Toolkit's `createSlice` API uses Immer to allow **mutating** immutable updates*

* Async logic is typically written in special functions called **thunks**
  * Thunks receive `dispatch` and `getState` as arguments
  * Redux Toolkit enables the `redux-thunk` middleware by default

* React-Redux allows React components to interact with a Redux store
  * Wrapping the app with `<Provider store={store} ></Provider>` enables all components to use the store
  * Global state should go in the Redux store, local state should stay in React component.
