# Part 1: Redux Overview and Concepts

## Define

**Redux** is a pattern and library for managing and updating application state, using events called `actions`. It servers as a centralized store for state that needs to be used across your entire application, with rules ensuring that state can only be updated in a predictable fashion.

- Redux is more useful when:
  - Have large amounts of application state that are needed in many places in the app.
  - The app state is updated frequently over time.
  - The logic to update that state may be complex
  - The app has a medium or large-sized codebase, and might be worked on by many people.

- Redux libraries and tools
  - [React-Redux](https://react-redux.js.org/)
  - [Redux-toolkit](https://redux-toolkit.js.org/)
  - [Redux DevTools extension.](https://github.com/reduxjs/redux-devtools/tree/main/extension)

## Terms and Concepts

### State management

```js
const Counter = () => {
    const [count, setCount] = useState(0)

    const increment = () => {
        setCount(pre => pre + 1)
    }

    return(
        <div>
            value: {count}
            <button onClick={increment}>Increment</button>
        </div>
    )

}
```

> This is a self-contained app with:

- `state`: the source of truth that drives our app
- `view`: a declarative description of the UI based on the current state
- `actions`: the events that occur in the app based on user input and trigger update in the state

>This is a example of `one-way data flow`: view -> action -> state -> view

- One way to alternative lifting state up  is to extract the shared state from the components and put it into a centralized location outside the components tree.
- By defining and separating the concepts involved in state management and enforcing rules that maintain independence between view and states we give our code more structure and maintainability.

### Immutability

- Javascript object and arrays are all mutable by default. If I create an object, I can change the contents of its fields. If I create and array I can change the contents as well.
- In order to update values immutably, your code must make `copies` of existing object/arrays, and the modify the copies

```js
const obj = {
    a: {
        c: 3
    },
    b: 2
}

const obj2 = {
    // copy object
    ...obj,
    //overwrite
    a:{
        ...obj.a,
        c:42
    }
}


const arr = ['a', 'b']
// create a new copy of arr, with 'c' appended to the end
const arr2 = arr.concat('c')

// or make a copy of the origin array:
const arr3 = arr.slice()
arr3.push('c')
```

Redux expects that all state updates are done immutably.

### Terminology

#### Actions

> An `action` is a plain Javascript object that has a `type` field.

- The `type` field should be a string that gives this action a descriptive name like **"todos/todoAdded"** where the first part is the feature or category that this action belongs to. and the second part is the specific thing that happened.
- An action object can have other fields with additional info about what happened.

```js
const addTodoAction = {
    type: 'todos/todoAdded',
    payload: 'learn redux'
}
```

#### Action Creators

> An action creators is a function that creates and return an object. Typically use these so we don't have to write the action object by hand every time.

```js
const addTodo = (text) => {
    return {
        type: 'todos/todoAdded',
        payload: text
    }
}
```

#### Reducers

> A `reducer` is a function that receives the current `state` and `action` object, decide how to update the state if necessary, and return new state: `(state, action) => newState`

- `Reducer` must **always** follow some rules:
  - The should only calculate the new state value based on the `state` and `action` arguments
  - The are **not allowed** to modify the existing `state`,  Instead the must make **immutable updates** by copying the existing `state` and making changes to the copied values
  - They must not do any asynchronous logic, calculate random values, or cause other *side effects*

```js
function todoReducer(state, action) {
    // check to see if the reducer cares about this action
    if (action.type === 'todos/todoAdded'){
        // if so, make a copy of `state`
        return {
            ...state,
            // and update the copy with the new value
            value: action.payload
        }
    }
}
```

- `reducer` can use any kind of logic inside to decide what the new styate should be: `if/else`, `switch`, loop and so on.

#### Store

- The current Redux application state lives in an object called the `store`
- The store is created by passing in a reducer, and has a method called `getState` the returns the current state value.

```js
import {configureStore} from '@reduxjs/toolkit;

const store = configureStore({reducer: todoReducer})
console.log(store.getState())
```

#### Dispatch

- The Redux store has a method called `dispatch`. this is the only way to update state is to call `store.dispatch()` and pass in an action object.
- The tore will run its reducer and save the new state value inside, and we can call `getState()` to retrieve the updated value

```js
store.dispatch({type: 'todos/todoAdded'})
console.log(store.getState)
```

#### Selectors

- `Selectors` are functions that know how to extract specific pieces of information from a store state value. As an application grows bigger, this can help avoid repeating logic as different parts of the app need to read the same data:

```js
const selectCounterValue = state => state.value

const currentValue = selectCounterValue(store.getState())
console.log(currentValue)
// 2
```

### Redux data flow

- Here's what data flow looks like visually:
![img](https://redux.js.org/assets/images/ReduxDataFlowDiagram-49fa8c3968371d9ef6f2a1486bd40a26.gif)

> In `Redux`, can break step into more detail:
- Initial Setup:
    - A Redux store is created root reducer once function.
    - The store calls the root reducer once and saves the return value as its inital `state`
    - When the UI is first rendered, UI components access the current state of the Redux store, and use that data to decide what to render. They also subscribe to any future store updates so they can know if the state has changed.
- Updates
    - Something happends in the app, such as a user clicking a button
    - The app code dispatches an action to the Redux store, like `dispatch({type: 'todos/todoAdded'})`
    - The `store` run the **reducer function** again with the previous `state` and the current `action` and saves the return value as the new `state`
    -  The store notifies all parts of the UI that are subscribed that the store has been updated. 
    - Each UI component that needs data from the store checks to see if the parts of the state they need have changed.
    - Each component that seesd its data has changed forces a re-render with the new data, so it can update what's shown on the screen.