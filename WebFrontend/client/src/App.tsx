import React, { useState, useEffect } from 'react';
import axios, {AxiosError} from 'axios';
import { useQuery, useQueryClient } from 'react-query';
import { axiosProxy } from '@app/redux/utils';
import './sass/main.scss';
import { Routes, Route } from 'react-router-dom';
import AppRouter from '@routes/App.routes';
import { AppProps } from './App.types';
import Spinner from '@components/Spinner';
import Page from '@secureailabs/web-ui/layout/Page';
import TimeAgo from 'javascript-time-ago';

import en from 'javascript-time-ago/locale/en.json';
import { IUserData } from '@app/redux/user/user.typeDefs';
TimeAgo.addLocale(en);
TimeAgo.setDefaultLocale('en');

const App: React.FC<AppProps> = ({
}) => {

  const checkUserSession = async (): Promise<IUserData> => {
    try {
      const res = await axios.get<IUserData>
        (`${axiosProxy()}/api/v1/me`,
          {
            withCredentials: true,
          });
      return res.data;
    }
    catch {
      await axios.post
        (`${axiosProxy()}/api/v1/refresh-token`,
          {
            withCredentials: true,
          });
      const res = await axios.get<IUserData>
        (`${axiosProxy()}/api/v1/me`,
          {
            withCredentials: true,
          });
      return res.data;
    }
  }

  useQuery<IUserData, AxiosError>(['userData'], checkUserSession, { retry : false, refetchInterval: 600000 });

  return (
    <>
      <AppRouter />
    </>
  );
};

export default App;
