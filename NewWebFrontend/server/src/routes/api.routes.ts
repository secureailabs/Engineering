import express from 'express';
import session from 'express-session';
import secureSession from '@middleware/secure-session';
import requestProxy from '@middleware/request-proxy';
import jwtManager from '@middleware/jwt-manager/jwt-manager';
import statusOverwriter from '@middleware/status-overwriter';
const router = express.Router();

// REMOVE IN PRODUCTION
if (process.env.NODE_ENV != 'production') {
  process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
}

// These modules only apply when we proxy API requests
router.use(session({ secret: 'Luis is watching you...', rolling: true, resave: false, saveUninitialized: false, cookie: process.env.NODE_ENV == 'production' ? { secure: true, sameSite: 'none' } : {} }));
router.use(secureSession())
router.use(express.urlencoded({ extended: true }));

// -------------------- Authentication Manager --------------------

// -- Login --
router.post(
  '/login',
  requestProxy({ method: 'POST' }),
  jwtManager(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- Refresh Token --
router.post(
  '/refresh-token',
  jwtManager({ order: 'pre-request', token: 'refresh' }),
  requestProxy({ method: 'POST', contentType: 'application/json' }),
  jwtManager(),
  (req, res) => {
    res.send(res.body);
  }
);

// // -- EndSession -- (not implemented in REST Portal?)
// router.delete(
//   '/AuthenticationManager/User/EOSB',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AuthenticationManager/User/EOSB', method: 'DELETE' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- Change Password --
// router.patch(
//   '/AuthenticationManager/User/Password',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ method: 'PATCH' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- GetBasicUserInformation --
router.get(
  '/me',
  jwtManager({ order: 'pre-request' }),
  requestProxy({ method: 'GET' }),
  (req, res) => {
    res.send(res.body);
  }
);

// -------------------- Account Manager --------------------
// -- RegisterOrganizationAndSuperUser --
// router.post(
//   '/AccountManager/RegisterUser',
//   requestProxy({ path: 'AccountManager/RegisterUser', method: 'POST' }),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- RegisterUser --
// router.post(
//   '/AccountManager/Admin/RegisterUser',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AccountManager/Admin/RegisterUser', method: 'POST' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- UpdateUserInformation --
// router.put(
//   '/AccountManager/Update/User',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AccountManager/Update/User', method: 'PUT' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- UpdateUserAccessInformation --
// router.put(
//   '/AccountManager/Update/AccessRight',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AccountManager/Update/AccessRight', method: 'PUT' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- ListOrganizationUsers -
// router.get(
//   '/AccountManager/Organization/Users',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AccountManager/Organization/Users', method: 'GET' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- ListOrganizations -
// router.get(
//   '/AccountManager/Organizations',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AccountManager/Organizations', method: 'GET' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- Organization Information -
// router.get(
//   '/AccountManager/Organization/Information',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AccountManager/Organization/Information', method: 'GET' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- UPDATE Organization Information -
// router.put(
//   '/AccountManager/Update/Organization',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AccountManager/Update/Organization', method: 'PUT' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- DeleteOrganization --
// router.delete(
//   '/AccountManager/Remove/Organization',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AccountManager/Remove/Organization', method: 'DELETE' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- DeleteUser --
// router.delete(
//   '/AccountManager/Remove/User',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AccountManager/Remove/User', method: 'DELETE' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- RecoverUser --
// router.put(
//   '/AccountManager/Update/RecoverUser',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AccountManager/Update/RecoverUser', method: 'PUT' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -------------------- Dataset Manager --------------------
// -- ListDatasets --
router.get(
  '/dataset-versions',
  jwtManager({ order: 'pre-request' }),
  requestProxy({ method: 'GET' }),
  (req, res) => {
    res.send(res.body);
  }
);

// -- PullDataset --
router.get(
  '/dataset-versions/*',
  jwtManager({ order: 'pre-request' }),
  requestProxy({ method: 'GET' }),
  (req, res) => {
    res.send(res.body);
  }
);

// -------------------- Digital Contract Manager --------------------
// -- RegisterDigitalContract --
// router.post(
//   '/DigitalContractManager/Applications',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'DigitalContractManager/Applications', method: 'POST' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- AcceptDigitalContract --
// router.patch(
//   '/DigitalContractManager/DataOwner/Accept',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'DigitalContractManager/DataOwner/Accept', method: 'PATCH' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- ActivateDigitalContract --
// router.patch(
//   '/DigitalContractManager/Researcher/Activate',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'DigitalContractManager/Researcher/Activate', method: 'PATCH' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- ListDigitalContracts --
// router.get(
//   '/digital-contracts',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'digital-contracts', method: 'GET' }),
//   // jwtManager(),
//   // statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- PullDigitalContract --
// router.get(
//   '/DigitalContractManager/PullDigitalContract',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'DigitalContractManager/PullDigitalContract', method: 'GET' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- GetProvisioningStatus --
// router.get(
//   '/DigitalContractManager/GetProvisioningStatus',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'DigitalContractManager/GetProvisioningStatus', method: 'GET' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- ProvisionDigitalContract --
// router.post(
//   '/DigitalContractManager/Provision',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'DigitalContractManager/Provision', method: 'POST' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- DeprovisionDigitalContract --
// router.post(
//   '/DigitalContractManager/Deprovision',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'DigitalContractManager/Deprovision', method: 'POST' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -------------------- Virtual Machine Manager --------------------
// -- RegisterVirtualMachine -- (not tested)
// router.post(
//   '/VirtualMachineManager/RegisterVM',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'VirtualMachineManager/RegisterVM', method: 'POST' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- RegisterVmAfterDataUpload -- (not tested)
// router.post(
//   '/VirtualMachineManager/DataOwner/RegisterVM',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'VirtualMachineManager/DataOwner/RegisterVM', method: 'POST' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- RegisterVmForComputation -- (not tested)
// router.post(
//   '/VirtualMachineManager/Researcher/RegisterVM',
//   jwtManager({ order: 'pre-request' }),
//   requestProxy({ path: 'VirtualMachineManager/Researcher/RegisterVM', method: 'POST' }),
//   jwtManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -------------------- Virtual Machine -----------------

router.get(
  '/secure-computation-node',
  jwtManager({ order: 'pre-request' }),
  requestProxy({ method: 'GET' }),
  (req, res) => {
    res.send(res.body);
  }
);

router.get(
  '/VirtualMachineManager/PullVirtualMachine',
  jwtManager({ order: 'pre-request' }),
  requestProxy({ method: 'GET' }),
  (req, res) => {
    res.send(res.body);
  }
);

// -------------------- Utils --------------------

// // -- LogOut -- (destroy session)
// router.delete('/logout', (req, res) => {
//   req.session.destroy(() => res.sendStatus(200));
// });

export default router;
