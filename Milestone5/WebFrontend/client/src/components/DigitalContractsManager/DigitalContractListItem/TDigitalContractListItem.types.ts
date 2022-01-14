import { IUserData } from '@redux/user/user.typeDefs';

export type TDigitalContractListItem = {
    // The index is used to switch between white and whitesmoke bg colors
    index: number;
    guid: string;  
    title: string;
    versionNumber: string;
    stage: number;
    subscriptionDays: number;
    datasetGuid: string;
    datasetName: string;
    description: string;
    eula: string;
    dataOwnerOrganization: string;
    researcherOrganization: string;
    DOOName: string;
    ROName: string;
    lastActivity: number;
    legalAgreement: string;
    activationTime?: number;
    expirationTime?: number;
    userData: IUserData;
    onClick:() => void;
  };