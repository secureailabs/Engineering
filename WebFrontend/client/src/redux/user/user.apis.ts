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

export const userSignup = (
  data: IPostUserStart
): Promise<
  AxiosResponse<{ data: { doc: IUserData } }> | IDefaults['error']
> => {
  // console.log("/#>#>#>#>#>#>#>#>#>#>#>#>#>#>#>#>/")
  // console.log(formatData(data))
  return axios
    .post(
      `${axiosProxy()}/api/v1/AccountManager/RegisterUser`,
      formatData(data)
    )
    .then((res) => {
      // The backend sometimes returns status 200 or 204 even when the org couldnt be created
      console.log(res);
      if (res.status != 201) {
        throw new Error('Backend didnt return 201');
      }
      return res;
    })
    .catch((err) => {
      throw err;
    });
};

export const checkAuth = () =>
  axios
    .get(
      `${axiosProxy()}/api/v1/me`,
      { withCredentials: true }
    )
    .then((res) => {
      if (res) {
        console.log(axiosProxy());
        return res;
      }
      throw new Error('Token expired');
    })
    .catch((err) => {
      throw err.response.data;
    });

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
