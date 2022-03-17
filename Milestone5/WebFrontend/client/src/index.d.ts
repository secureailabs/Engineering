declare global {
    interface Window {
        "__REDUX_DEVTOOLS_EXTENSION__":any;
    }
}

declare const window: Window &
   typeof globalThis & {

    "__REDUX_DEVTOOLS_EXTENSION__":any;
   }
