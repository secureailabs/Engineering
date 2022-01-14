export type TPostAccountManagerStart = {
  Email: string;
  Password: string;
  Name: string;
  PhoneNumber: number;
  Title: string;
  AccessRights: string;
  OrganizationGuid: string;
};
export type TPostAccountManagerSuccess = null;

export type TDeleteAccountManagerStart = {
  UserGuid: string;
};
export type TDeleteAccountManagerSuccess = null;

export type TPutUpdateUserStart = {
  UserGuid: string;
  UserInformation: {
    Name: string;
    Title: string;
    PhoneNumber: string;
  };
};

export type TPutUpdateUserSuccess = null;

export type TPutUpdatePasswordStart = {
  Email: string;
  CurrentPassword: string;
  NewPassword: string;
};

export type TPutUpdatePasswordSuccess = null;

export type TPutUpdateAccessRightsStart = {
  UserGuid: string;
  AccessRights: number;
};

export type TPutUpdateAccessRightsSuccess = null;

export type TGetAllAccountManagersStart = {
  OrganizationGuid: string;
};

export type TGetAllAccountManagersSuccess = {
  OrganizationUsers: Record<
    string,
    TGetAccountManagerSuccess['AccountManager']
  >;
};

export type TGetAccountManagerSuccess = {
  AccountManager: {
    AccessRights: 1 | 2 | 3 | 4 | 5 | 6;
    AccountStatus: 0 | 1 | 2 | 3;
    Email: string;
    PhoneNumber: string;
    TimeOfAccountCreation: number;
    Title: string;
    UserGuid: string;
    Username: string;
  };
};

export type TGetAccountManagerStart = {
  AccountManagerGuid: string;
};

export type TPutAccountManagerSuccess = null;

export type TPutAccountManagerStart = {
  UserGuid: string;
};
