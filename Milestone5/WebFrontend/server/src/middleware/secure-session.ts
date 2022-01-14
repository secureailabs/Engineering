import catchAsync from '@utils/catchAsync';
import AppError from '@utils/appError';

export default function () {
  return catchAsync(async (req, res, next) => {
  if (req.session.Eosb && !(req.path == '/AuthenticationManager/User/Login' || req.path == '/AccountManager/RegisterUser')) {
    if (!(req.session.ip === req.ip && req.session.useragent === req.headers['user-agent'])) {
      // console.log("req.session.ip: " + req.session.ip + " req.ip: " + req.ip + " req.session.useragent: " + req.session.useragent + " req.headers['user-agent]: " + req.headers['user-agent'])
      throw new AppError('Please login again', 401);
    }
  } else {
    req.session.ip = req.ip;
    req.session.useragent = req.headers['user-agent'];
  }
  next();
})};


