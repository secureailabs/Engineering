import { Request, Response, NextFunction } from 'express';

export default (fn: (req: Request, res: Response, next: NextFunction) => Promise<void>) => {
  //this is the function that express will call
  return (req: Request, res: Response, next: NextFunction) => {
    fn(req, res, next).catch(next);
  };
};
