export type RequestProxyOptionTypes = {
  method?: 'GET' | 'POST' | 'PATCH' | 'DELETE' | 'PUT';
  contentType?: 'application/x-www-form-urlencoded' | 'application/json';
  path?: string;
};
