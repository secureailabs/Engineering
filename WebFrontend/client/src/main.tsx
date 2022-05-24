import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';
import '@secureailabs/web-ui/css/style.css';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import { ReactQueryDevtools } from 'react-query/devtools';

import { BrowserRouter } from 'react-router-dom';

import { QueryClient, QueryClientProvider } from 'react-query';

const queryClient = new QueryClient()

ReactDOM.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
    {/* <Provider store={store}> */}
        <BrowserRouter>
          <App />
          {/* <ReactQueryDevtools initialIsOpen={false} /> */}
        </BrowserRouter>
    {/* </Provider> */}
    </QueryClientProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

// Hot Module Replacement (HMR) - Remove this snippet to remove HMR.
// Learn more: https://snowpack.dev/concepts/hot-module-replacement
if (import.meta.hot) {
  import.meta.hot.accept();
}
