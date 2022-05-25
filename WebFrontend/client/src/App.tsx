import React  from 'react';
import {AxiosError} from 'axios';
import { useQuery } from 'react-query';
import './sass/main.scss';
import AppRouter from '@routes/App.routes';
import { AppProps } from './App.types';
import TimeAgo from 'javascript-time-ago';
import { checkUserSession } from '@redux/user/user.apis';
import en from 'javascript-time-ago/locale/en.json';
import { IUserData } from '@app/redux/user/user.typeDefs';
TimeAgo.addLocale(en);
TimeAgo.setDefaultLocale('en');

const App: React.FC<AppProps> = ({
}) => {

  useQuery<IUserData, AxiosError>(['userData'], checkUserSession, { retry : false, refetchInterval: 600000 });

  return (
    <>
      <AppRouter />
    </>
  );
};

export default App;
