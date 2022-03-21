import express from 'express';
import session from 'express-session';
import bodyParser from 'body-parser';
import secureSession from '@middleware/secure-session';
import requestProxy from '@middleware/request-proxy';
import eosbManager from '@middleware/eosb-manager';
import statusOverwriter from '@middleware/status-overwriter';
const router = express.Router();

// REMOVE IN PRODUCTION
if (process.env.NODE_ENV != 'production') {
  process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
}

// These modules only apply when we proxy API requests
router.use(session({ secret: 'Luis is watching you...', rolling: true, resave: false, saveUninitialized: false }));
router.use(secureSession())
router.use(bodyParser.json());

// -------------------- Authentication Manager --------------------

// -- Login --
router.post(
  '/AuthenticationManager/User/Login',
  requestProxy({ path: 'AuthenticationManager/User/Login', method: 'POST' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// // -- EndSession -- (not implemented in REST Portal?)
// router.delete(
//   '/AuthenticationManager/User/EOSB',
//   eosbManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AuthenticationManager/User/EOSB', method: 'DELETE' }),
//   eosbManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -- Change Password --
router.patch(
  '/AuthenticationManager/User/Password',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AuthenticationManager/User/Password', method: 'PATCH' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- GetBasicUserInformation --
router.get(
  '/AuthenticationManager/GetBasicUserInformation',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AuthenticationManager/GetBasicUserInformation', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -------------------- Account Manager --------------------
// -- RegisterOrganizationAndSuperUser --
router.post(
  '/AccountManager/RegisterUser',
  requestProxy({ path: 'AccountManager/RegisterUser', method: 'POST' }),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- RegisterUser --
router.post(
  '/AccountManager/Admin/RegisterUser',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AccountManager/Admin/RegisterUser', method: 'POST' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- UpdateUserInformation --
router.put(
  '/AccountManager/Update/User',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AccountManager/Update/User', method: 'PUT' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- UpdateUserAccessInformation --
router.put(
  '/AccountManager/Update/AccessRight',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AccountManager/Update/AccessRight', method: 'PUT' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- ListOrganizationUsers -
router.get(
  '/AccountManager/Organization/Users',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AccountManager/Organization/Users', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- ListOrganizations -
router.get(
  '/AccountManager/Organizations',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AccountManager/Organizations', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- Organization Information -
router.get(
  '/AccountManager/Organization/Information',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AccountManager/Organization/Information', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- UPDATE Organization Information -
router.put(
  '/AccountManager/Update/Organization',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AccountManager/Update/Organization', method: 'PUT' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- DeleteOrganization --
router.delete(
  '/AccountManager/Remove/Organization',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AccountManager/Remove/Organization', method: 'DELETE' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- DeleteUser --
router.delete(
  '/AccountManager/Remove/User',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AccountManager/Remove/User', method: 'DELETE' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- RecoverUser --
router.put(
  '/AccountManager/Update/RecoverUser',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AccountManager/Update/RecoverUser', method: 'PUT' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -------------------- Dataset Manager --------------------
// -- ListDatasets --
router.get(
  '/DatasetManager/ListDatasets',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'DatasetManager/ListDatasets', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- ListDatasets --
router.get(
  '/DatasetManager/PullDataset',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'DatasetManager/PullDataset', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -------------------- Digital Contract Manager --------------------
// -- RegisterDigitalContract --
router.post(
  '/DigitalContractManager/Applications',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'DigitalContractManager/Applications', method: 'POST' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- AcceptDigitalContract --
router.patch(
  '/DigitalContractManager/DataOwner/Accept',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'DigitalContractManager/DataOwner/Accept', method: 'PATCH' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- ActivateDigitalContract --
router.patch(
  '/DigitalContractManager/Researcher/Activate',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'DigitalContractManager/Researcher/Activate', method: 'PATCH' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- ListDigitalContracts --
router.get(
  '/DigitalContractManager/DigitalContracts',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'DigitalContractManager/DigitalContracts', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- PullDigitalContract --
router.get(
  '/DigitalContractManager/PullDigitalContract',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'DigitalContractManager/PullDigitalContract', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- GetProvisioningStatus --
router.get(
  '/DigitalContractManager/GetProvisioningStatus',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'DigitalContractManager/GetProvisioningStatus', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- AssociateWithAzureTemplate --
router.patch(
  '/DigitalContractManager/AssociateWithAzureTemplate',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'DigitalContractManager/AssociateWithAzureTemplate', method: 'PATCH' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- ProvisionDigitalContract --
router.post(
  '/DigitalContractManager/Provision',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'DigitalContractManager/Provision', method: 'POST' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- DeprovisionDigitalContract --
router.post(
  '/DigitalContractManager/Deprovision',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'DigitalContractManager/Deprovision', method: 'POST' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -------------------- Virtual Machine Manager --------------------
// -- RegisterVirtualMachine -- (not tested)
router.post(
  '/VirtualMachineManager/RegisterVM',
  eosbManager({ order: 'pre-request', token: 'Eosb' }),
  requestProxy({ path: 'VirtualMachineManager/RegisterVM', method: 'POST' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- RegisterVmAfterDataUpload -- (not tested)
router.post(
  '/VirtualMachineManager/DataOwner/RegisterVM',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'VirtualMachineManager/DataOwner/RegisterVM', method: 'POST' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- RegisterVmForComputation -- (not tested)
router.post(
  '/VirtualMachineManager/Researcher/RegisterVM',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'VirtualMachineManager/Researcher/RegisterVM', method: 'POST' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -------------------- Cryptographic Manager --------------------
// -- GetIEosb -- (tested but gives IEosb to browser)
router.get(
  '/CryptographicManager/User/GetIEosb',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'CryptographicManager/User/GetIEosb', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -------------------- Audit Log Manager --------------------
// -- RegisterLeafEvents -- (not tested)
router.post(
  '/AuditLogManager/LeafEvents',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AuditLogManager/LeafEvents', method: 'POST' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- GetListOfEvents -- (not tested)
router.get(
  '/AuditLogManager/GetListOfEvents',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AuditLogManager/GetListOfEvents', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// GetRemoteAttestationCertificate

// -- ShutdownPortal -- (not tested)
// router.post(
//   '/AuthenticationManager/ShutdownPortal',
//   eosbManager({ order: 'pre-request' }),
//   requestProxy({ path: 'AuthenticationManager/ShutdownPortal', method: 'POST' }),
//   eosbManager(),
//   statusOverwriter(),
//   (req, res) => {
//     res.send(res.body);
//   }
// );

// -------------------- Azure Manager --------------------
// -- RegisterAzureTemplate --
router.post(
  '/AzureManager/RegisterTemplate',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AzureManager/RegisterTemplate', method: 'POST' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- ListAzureTemplates --
router.get(
  '/AzureManager/ListTemplates',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AzureManager/ListTemplates', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- PullAzureTemplate --
router.get(
  '/AzureManager/PullTemplate',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AzureManager/PullTemplate', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -- UpdateAzureTemplate --
router.put(
  '/AzureManager/UpdateTemplate',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AzureManager/UpdateTemplate', method: 'PUT' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    console.log(req.body);
    res.send(res.body);
  }
);

// -- DeleteAzureTemplate --
router.delete(
  '/AzureManager/DeleteTemplate',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'AzureManager/DeleteTemplate', method: 'DELETE' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

// -------------------- Virtual Machine -----------------

router.get(
  '/VirtualMachineManager/ListVirtualMachines',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'VirtualMachineManager/ListVirtualMachines', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
  (req, res) => {
    res.send(res.body);
  }
);

router.get(
  '/VirtualMachineManager/PullVirtualMachine',
  eosbManager({ order: 'pre-request' }),
  requestProxy({ path: 'VirtualMachineManager/PullVirtualMachine', method: 'GET' }),
  eosbManager(),
  statusOverwriter(),
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
