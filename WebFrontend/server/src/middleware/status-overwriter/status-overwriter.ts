import { Request, Response, NextFunction } from 'express';

export default function () {
    return (req: Request, res: Response, next: NextFunction) => {
        if (res.body && res.body.Status) {
            res.status(res.body.Status)
        }
        next()
    }
}
