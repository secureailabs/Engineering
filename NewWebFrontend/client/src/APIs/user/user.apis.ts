import axios from 'axios';

import { axiosProxy } from '@APIs/utils';

import { IUserData } from './user.typeDefs';

export const checkUserSession = async (): Promise<IUserData> => {
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

export const logoutApi = async () => {
  await axios.delete(
    `${axiosProxy()}/api/v1/logout`,
    {
      withCredentials: true,
    });
}
