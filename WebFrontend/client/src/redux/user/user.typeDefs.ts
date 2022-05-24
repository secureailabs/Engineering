export type IUserData = {
  AccessRights: 1 | 2 | 3 | 4 | 5 | 6;
  OrganizationGuid: string;
  OrganizationName: string;
  UserGuid: string;
  Status: number;
  Username: string;
  PhoneNumber: string;
  Email: string;
  Title: string;
} | null;

export interface IEmailAndPassword {
  username: string;
  password: string;
}

export interface IPostUserStart {
  email: string;
  password: string;
  name: string;
  phoneNumber: string;
  title: string;
  organizationName: string;
  organizationAddress: string;
  primaryContactName: string;
  primaryContactTitle: string;
  primaryContactEmail: string;
  primaryContactPhoneNumber: string;
  secondaryContactName: string;
  secondaryContactTitle: string;
  secondaryContactEmail: string;
  secondaryContactPhoneNumber: string;
}
