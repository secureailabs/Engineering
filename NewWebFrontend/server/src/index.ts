import express from 'express';
import path from 'path';
import helmet from 'helmet';
import cors from 'cors';
import https from 'https';
import fs from 'fs';

import apiRoutes from '@routes/api.routes';
import logout from '@controllers/logout';

const app = express();

app.use(helmet());
require('dotenv').config();
const port = 3000;
app.use(cors({ credentials: true, origin: process.env.CLIENT ? process.env.CLIENT : 'http://127.0.0.1:3001' }));

app.use('/api/v1/', apiRoutes);
app.use('/api/v1/', logout);

// Removed for testing
// if (process.env.NODE_ENV === 'production') {
// console.log("here");
//serves the react app in production
app.use(express.static(path.join(__dirname, '../../client/dist')));

//for any url that is not covered by future routes, sends the react app
app.get('*', function (req, res) {
  res.sendFile(path.join(__dirname, '../../client/dist', 'index.html'));
});

if (process.env.NODE_ENV === 'production') {
  const privateKey = fs.readFileSync('./ssl.key');
  const certificate = fs.readFileSync('./ssl.crt');
  https
    .createServer(
      {
        key: privateKey,
        cert: certificate,
      },
      app
    )
    .listen(port);
} else {
  app.listen(port, () => {
    console.log('server listening on port 3000');
  });
}
