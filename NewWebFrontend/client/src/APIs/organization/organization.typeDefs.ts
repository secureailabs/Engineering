export type TGetOrganizationSuccess = {
  name: string;
  description: string;
  avatar: string | any; // Should be string only in prod
  id: string;
};

export type TGetOrganizationStart = {
  organization_id: string;
};

export type TGetAllOrganizationsSuccess = {
  organizations: Array<TGetOrganizationStart>
}

export type TGetAllOrganizationsStart = null
