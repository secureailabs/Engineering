class AppError extends Error {
  statusCode: number;
  status: string;
  isOperational: boolean;
  constructor(message: string, statusCode: number) {
    //Built in error class takes in message
    super(message);
    this.statusCode = statusCode;
    this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
    this.isOperational = true;

    // Appends Stack trace to the object (details for devs)
    // becomes proprety .stack of the object
    Error.captureStackTrace(this, this.constructor);
  }
}

export default AppError;
