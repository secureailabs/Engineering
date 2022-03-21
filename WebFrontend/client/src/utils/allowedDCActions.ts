import { TDigitalContractInfo } from '@components/DigitalContractsManager/DigitalContractInfo/DigitalContractInfo.types';
import getDCStage from '@utils/getDCStage';

const allowedDCActions = (
  // ContractStage: Exclude<
  //   TDigitalContractInfo['getDigitalContractData'],
  //   null
  // >['DigitalContract']['ContractStage'],
  contract: Exclude<
          TDigitalContractInfo['getDigitalContractData'],
          null
            >,
  userData: TDigitalContractInfo['userData']
): [boolean, boolean, boolean, boolean, boolean] => {
  // @ts-ignore we'll have to make 2 separate types or ask Shabana to standardize them
  // console.log(contract)
  // console.log(userData)
  // console.log(contract.DigitalContract.ProvisioningStatus.ProvisioningStatus == 0)
  // console.log(contract.DigitalContract.AzureTemplateGuid != undefined)
  // console.log(contract.DigitalContract.ResearcherOrganization == userData?.OrganizationGuid)
  // console.log(contract.DigitalContract.ResearcherOrganization)
  switch (getDCStage(contract.DigitalContract?.ContractStage, contract.DigitalContract.ExpirationTime)) {
    case 1: {
  // @ts-ignore we'll have to make 2 separate types or ask Shabana to standardize them
      const canAcceptDigitalContract = (userData?.OrganizationGuid == contract.DataOwnerOrganization) && (userData?.AccessRights == 5 || userData?.AccessRights == 1)
      return [canAcceptDigitalContract, false, false, false, false];
    }
    case 2: {
   // @ts-ignore we'll have to make 2 separate types or ask Shabana to standardize them
      const canActivateDigitalContract = (userData?.OrganizationGuid == contract.ResearcherOrganization) && (userData?.AccessRights == 4 || userData?.AccessRights == 1)
      return [false, canActivateDigitalContract, false, false, false];
    }
    case 3: {
      const canSelectAzureTemplate = ((
        contract.DigitalContract.HostForVirtualMachines == 'Researcher'
          &&
        // @ts-ignore
        contract.ResearcherOrganization == userData?.OrganizationGuid)
      ||
      (
        contract.DigitalContract.HostForVirtualMachines == 'Data Owner'
          &&
        // @ts-ignore
        contract.DataOwnerOrganization == userData?.OrganizationGuid)
      )

      const canProvisionDigitalContract = (
        ((contract.DigitalContract.ProvisioningStatus == 3 || contract.DigitalContract.ProvisioningStatus == 4)
        &&
        (contract.DigitalContract.AzureTemplateGuid != undefined))
        // &&
        // // @ts-ignore
        // (contract.ResearcherOrganization == userData?.OrganizationGuid)
      )

      const canDeprovisionDigitalContract = contract.DigitalContract.ProvisioningStatus == 2

      return [false, false, canSelectAzureTemplate, canProvisionDigitalContract, canDeprovisionDigitalContract]
    }
    default: {
      const canDeprovisionDigitalContract = contract.DigitalContract.ProvisioningStatus == 2
      return [false, false, false, false, canDeprovisionDigitalContract];
    }
  }
};

export default allowedDCActions;
