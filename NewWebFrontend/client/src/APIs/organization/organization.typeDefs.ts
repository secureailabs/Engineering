export type TPutOrganizationStart = {
  OrganizationGuid: string;
  OrganizationInformation: {
    OrganizationName: string;
    OrganizationAddress: string;
    PrimaryContactName: string;
    PrimaryContactTitle: string;
    PrimaryContactEmail: string;
    PrimaryContactPhoneNumber: string;
    SecondaryContactName: string;
    SecondaryContactTitle: string;
    SecondaryContactEmail: string;
    SecondaryContactPhoneNumber: string;
  };
};

export type TPutOrganizationSuccess = null;

export type TGetOrganizationSuccess = {
  OrganizationName: string;
  OrganizationAddress: string;
  PrimaryContactName: string;
  PrimaryContactTitle: string;
  PrimaryContactEmail: string;
  PrimaryContactPhoneNumber: string;
  SecondaryContactName: string;
  SecondaryContactTitle: string;
  SecondaryContactEmail: string;
  SecondaryContactPhoneNumber: string;
};

export type TGetOrganizationStart = null;
