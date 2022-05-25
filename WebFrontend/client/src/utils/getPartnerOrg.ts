import { IUserData } from '@APIs/user/user.typeDefs';

const getPartnerOrg = (
  userData: IUserData,
  dataOwnerOrganization: string,
  DOOName: string,
  ROName: string
): string => {
  return userData?.OrganizationGuid == dataOwnerOrganization ? ROName : DOOName;
};

export default getPartnerOrg;
