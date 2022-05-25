import { TGetAllDigitalContractsSuccess } from '@APIs/digitalContract/digitalContract.typeDefs';

const getDCStage = (
  stage: Exclude<
    TGetAllDigitalContractsSuccess,
    null
  >['DigitalContracts'][1]['ContractStage'],
  expirationTime: Exclude<
    TGetAllDigitalContractsSuccess,
    null
  >['DigitalContracts'][1]['ExpirationTime']
): 1 | 2 | 3 | 4 => {
  switch (stage) {
    case 1: {
      return 1;
    }
    case 2: {
      return 2;
    }
    case 3: {
      return expirationTime * 1000 > new Date().getTime() ? 3 : 4;
    }
    default: {
      return 1;
    }
  }
};

export default getDCStage;
