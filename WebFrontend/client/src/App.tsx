import React, { useState, useEffect } from 'react';
import './sass/main.scss';
import { Routes, Route } from 'react-router-dom';
import AppRouter from '@routes/App.routes';
import { AppProps } from './App.types';
import Spinner from '@components/Spinner';
import Page from '@secureailabs/web-ui/layout/Page';
import TimeAgo from 'javascript-time-ago';

import en from 'javascript-time-ago/locale/en.json';
TimeAgo.addLocale(en);
TimeAgo.setDefaultLocale('en');

const App: React.FC<AppProps> = ({
  checkUserSession,
  checkUserSessionAsync,
}) => {
  useEffect(() => {
    // Necessary to check user auth when clicking browser arrows to navigate history
    // history.listen(() => {
    //   if (performance.navigation.type == 2) {
    //     checkUserSession();
    //   }
    // });

    checkUserSession();
    // setInterval(() => checkUserSessionAsync(), 30000);
  }, []);
  // Return the App component.
  //
  //
  return (
    <>
      <AppRouter />
    </>
  );
};

export default App;
