export type IUserData = {
  username: string;
  email: string;
  job_title: string;
  role: 'ADMIN' | 'AUDITOR' | 'USER' | 'DIGITALCONTRACTADMIN' | 'DATASETADMIN' | 'SAILADMIN';
  avatar: string;
  id: string;
  organization: {
    id: string;
    name: string;
  }
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
