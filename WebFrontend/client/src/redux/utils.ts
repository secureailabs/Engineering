import { pascalCase } from 'change-case';

export const axiosProxy = () => {
  // console.log(import.meta.env);
  if (import.meta.env.MODE === 'development') {
    return import.meta.env.SNOWPACK_PUBLIC_API_URL_DEV;
  } else {
    return import.meta.env.SNOWPACK_PUBLIC_API_URL_PROD;
  }
};

export const formatData = (oldBody: any) => {
  let newBody: Record<string, string> = {};
  Object.entries(oldBody).map(([key, value]) => {
    if (typeof key === 'string' && typeof value === 'string') {
      newBody[pascalCase(key)] = value;
    }
  });
  return newBody;
};

export const fetchToken = () => {
  if (localStorage.token) {
    return `Bearer ${localStorage.token}`;
  }
  return '';
};

// Setup config/headers and token
export const tokenConfig = () => {
  // Get token from localstorage
  // Headers
  const config = {
    headers: {
      'Content-type': 'application/json',
      authorization: '',
    },
  };

  // If token, add to headers
  if (fetchToken()) {
    config.headers.authorization = fetchToken();
  }

  return config;
};