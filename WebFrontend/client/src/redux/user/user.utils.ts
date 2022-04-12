export const setToken = (token: string) => localStorage.setItem('token', token);

export const fetchToken = () => {
  if (localStorage.token) {
    return `Bearer ${localStorage.token}`;
  }
  return undefined;
};

export const removeToken = () => localStorage.removeItem('token');
