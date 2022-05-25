import axios, { AxiosResponse } from 'axios';
import { IDefaults } from '@app/redux/typedefs';
import { IUserData, IPostUserStart } from './user.typeDefs';
import { axiosProxy, formatData } from '@app/redux/utils';

// Setup config/headers and token
export const tokenConfig = (token: string) => {
  // Get token from localstorage
  // Headers
  const config = {
    headers: {
      'Content-type': 'application/json',
      authorization: '',
    },
  };

  // If token, add to headers
  if (token) {
    config.headers.authorization = token;
  }

  return config;
};

export const userLogin = (
  email: string,
  password: string
): Promise<
  AxiosResponse<{ data: { doc: IUserData } }> | IDefaults['error']
> => {
  return axios
    .post(
      `${axiosProxy()}/api/v1/login`,
      new URLSearchParams({
        username: email,
        password: password,
      }),
      { withCredentials: true }
    )
    .then((res) => {
      console.log(res);
      return res;
    })
    .catch((err) => {
      throw err;
    });
};

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

export const me = () =>
  axios
    .get(`${axiosProxy()}/api/v1/me`, { withCredentials: true })
    .then((res) => {
      if (res) {
        console.log(res)
        console.log(axiosProxy());
        return res;
      }
      throw new Error('Token expired');
    })
    .catch((err) => {
      throw err.response.data;
    });

export const logOut = () =>
  axios
    .delete(`${axiosProxy()}/api/v1/logout`, { withCredentials: true })
    .then((res) => {
      return res;
    })
    .catch((err) => {
      throw err.response.data;
    });
