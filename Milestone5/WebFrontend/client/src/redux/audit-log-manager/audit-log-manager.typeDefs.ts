export interface IPostLeafEventsStart {
  email: string;
  message: string;
  name: string;
  phone: string;
  subject: string;
}

export interface IAuditLogManagerData {
  createdAt: string;
  email: string;
  id: string;
  _id: string;
  message: string;
  name: string;
  phone: string;
  subject: string;
}

export type IGetAllEventsStart = IAuditLogManagerData[];

export type IGetAllEventsSuccess = {};
