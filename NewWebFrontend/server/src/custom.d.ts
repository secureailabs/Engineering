import { Session } from 'express-session'

declare module 'express-session' {
  interface SessionData {
    ip: string;
    Eosb?: string;
    jwt?: { access: string, refresh: string };
    useragent: string;
  }
}
