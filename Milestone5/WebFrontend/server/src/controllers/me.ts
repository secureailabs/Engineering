import express from 'express';

import axios from 'axios';

const router = express.Router();

// -- ME -- (check authentication)
router.get('/me', async (req, res) => {
  axios({
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    url: `${process.env.SAIL_API}/SAIL/AuthenticationManager/GetBasicUserInformation`,
    data: {
      Eosb: req.session.Eosb,
    },
  })
    .then((data) => {
      const new_body = data.data;
      delete new_body['Eosb'];
      res.send(new_body);
    })
    .catch((err) => {
      res.sendStatus(401);
    });
});
export default router;
