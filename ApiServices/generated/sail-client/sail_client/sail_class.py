from typing import Any, Union

from .api.default import (
    accept_or_reject_invite,
    add_data_model,
    add_dataset,
    deprovision_data_federation,
    drop_database,
    get_all_data_federation_provision_info,
    get_all_data_federations,
    get_all_dataset_versions,
    get_all_datasets,
    get_all_invites,
    get_all_organizations,
    get_all_secure_computation_nodes,
    get_current_user_info,
    get_data_federation,
    get_data_federation_provision_info,
    get_dataset,
    get_dataset_key,
    get_dataset_version,
    get_dataset_version_connection_string,
    get_existing_dataset_key,
    get_invite,
    get_organization,
    get_refresh_token,
    get_secure_computation_node,
    get_user,
    get_users,
    invite_data_submitter,
    invite_researcher,
    login,
    register_data_federation,
    register_data_federation_provision,
    register_data_submitter,
    register_dataset,
    register_dataset_version,
    register_organization,
    register_researcher,
    register_user,
    remove_dataset,
    soft_delete_data_federation,
    soft_delete_dataset,
    soft_delete_dataset_version,
    soft_delete_organization,
    soft_delete_user,
    update_data_federation,
    update_dataset,
    update_dataset_version,
    update_organization,
    update_secure_computation_node,
    update_user_info,
)
from .client import AuthenticatedClient, Client
from .models.add_data_model_data_model import AddDataModelDataModel
from .models.body_login import BodyLogin
from .models.dataset_encryption_key_out import DatasetEncryptionKeyOut
from .models.get_data_federation_out import GetDataFederationOut
from .models.get_data_federation_provision import GetDataFederationProvision
from .models.get_dataset_out import GetDatasetOut
from .models.get_dataset_version_connection_string_out import GetDatasetVersionConnectionStringOut
from .models.get_dataset_version_out import GetDatasetVersionOut
from .models.get_invite_out import GetInviteOut
from .models.get_multiple_data_federation_out import GetMultipleDataFederationOut
from .models.get_multiple_data_federation_provision_out import GetMultipleDataFederationProvisionOut
from .models.get_multiple_dataset_out import GetMultipleDatasetOut
from .models.get_multiple_dataset_version_out import GetMultipleDatasetVersionOut
from .models.get_multiple_invite_out import GetMultipleInviteOut
from .models.get_multiple_organizations_out import GetMultipleOrganizationsOut
from .models.get_multiple_secure_computation_node_out import GetMultipleSecureComputationNodeOut
from .models.get_multiple_users_out import GetMultipleUsersOut
from .models.get_organizations_out import GetOrganizationsOut
from .models.get_secure_computation_node_out import GetSecureComputationNodeOut
from .models.get_users_out import GetUsersOut
from .models.login_success_out import LoginSuccessOut
from .models.patch_invite_in import PatchInviteIn
from .models.refresh_token_in import RefreshTokenIn
from .models.register_data_federation_in import RegisterDataFederationIn
from .models.register_data_federation_out import RegisterDataFederationOut
from .models.register_data_federation_provision_in import RegisterDataFederationProvisionIn
from .models.register_data_federation_provision_out import RegisterDataFederationProvisionOut
from .models.register_dataset_in import RegisterDatasetIn
from .models.register_dataset_out import RegisterDatasetOut
from .models.register_dataset_version_in import RegisterDatasetVersionIn
from .models.register_dataset_version_out import RegisterDatasetVersionOut
from .models.register_organization_in import RegisterOrganizationIn
from .models.register_organization_out import RegisterOrganizationOut
from .models.register_user_in import RegisterUserIn
from .models.register_user_out import RegisterUserOut
from .models.update_data_federation_in import UpdateDataFederationIn
from .models.update_dataset_in import UpdateDatasetIn
from .models.update_dataset_version_in import UpdateDatasetVersionIn
from .models.update_organization_in import UpdateOrganizationIn
from .models.update_secure_computation_node_in import UpdateSecureComputationNodeIn
from .models.update_user_in import UpdateUserIn
from .models.user_info_out import UserInfoOut
from .types import UNSET, Unset


class SyncAuthenticatedOperations:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def get_current_user_info(
        self,
    ) -> UserInfoOut:
        """Get Current User Info

         Get the current user information

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[UserInfoOut]
        """

        response = get_current_user_info.sync(
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, UserInfoOut)
        return response

    def get_all_organizations(
        self,
    ) -> GetMultipleOrganizationsOut:
        """Get All Organizations

         Get list of all the organizations

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetMultipleOrganizationsOut]
        """

        response = get_all_organizations.sync(
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetMultipleOrganizationsOut)
        return response

    def get_organization(
        self,
        organization_id: str,
    ) -> GetOrganizationsOut:
        """Get Organization

         Get the information about a organization

        Args:
            organization_id (str): UUID of the requested organization

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetOrganizationsOut]
        """

        response = get_organization.sync(
            organization_id=organization_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetOrganizationsOut)
        return response

    def update_organization(
        self,
        organization_id: str,
        json_body: UpdateOrganizationIn,
    ) -> None:
        """Update Organization

         Update organization information

        Args:
            organization_id (str): UUID of the requested organization
            json_body (UpdateOrganizationIn): Organization details to update

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        update_organization.sync(
            organization_id=organization_id,
            client=self._client,
            json_body=json_body,
        )

    def soft_delete_organization(
        self,
        organization_id: str,
    ) -> None:
        """Soft Delete Organization

         Disable the organization and all the users

        Args:
            organization_id (str): UUID of the organization to be deleted

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        soft_delete_organization.sync(
            organization_id=organization_id,
            client=self._client,
        )

    def get_users(
        self,
        organization_id: str,
    ) -> GetMultipleUsersOut:
        """Get Users

         Get all users in the organization

        Args:
            organization_id (str): UUID of the organization

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetMultipleUsersOut]
        """

        response = get_users.sync(
            organization_id=organization_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetMultipleUsersOut)
        return response

    def register_user(
        self,
        organization_id: str,
        json_body: RegisterUserIn,
    ) -> RegisterUserOut:
        """Register User

         Add new user to organization

        Args:
            organization_id (str): UUID of the organization to add the user to
            json_body (RegisterUserIn): User details to register with the organization

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[RegisterUserOut]
        """

        response = register_user.sync(
            organization_id=organization_id,
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, RegisterUserOut)
        return response

    def get_user(
        self,
        organization_id: str,
        user_id: str,
    ) -> GetUsersOut:
        """Get User

         Get information about a user

        Args:
            organization_id (str): UUID of the organization
            user_id (str): UUID of the user

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetUsersOut]
        """

        response = get_user.sync(
            organization_id=organization_id,
            user_id=user_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetUsersOut)
        return response

    def update_user_info(
        self,
        organization_id: str,
        user_id: str,
        json_body: UpdateUserIn,
    ) -> None:
        """Update User Info

         Update user information

        Args:
            organization_id (str): UUID of the organization
            user_id (str): UUID of the user
            json_body (UpdateUserIn): User information to update

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        update_user_info.sync(
            organization_id=organization_id,
            user_id=user_id,
            client=self._client,
            json_body=json_body,
        )

    def soft_delete_user(
        self,
        organization_id: str,
        user_id: str,
    ) -> None:
        """Soft Delete User

         Soft Delete user

        Args:
            organization_id (str): UUID of the organization
            user_id (str): UUID of the user

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        soft_delete_user.sync(
            organization_id=organization_id,
            user_id=user_id,
            client=self._client,
        )

    def get_all_data_federations(
        self,
        data_submitter_id: Union[Unset, None, str] = UNSET,
        researcher_id: Union[Unset, None, str] = UNSET,
        dataset_id: Union[Unset, None, str] = UNSET,
    ) -> GetMultipleDataFederationOut:
        """Get All Data Federations

         Get list of all the data federations

        Args:
            data_submitter_id (Union[Unset, None, str]): UUID of Data Submitter in the data federation
            researcher_id (Union[Unset, None, str]): UUID of Researcher in the data federation
            dataset_id (Union[Unset, None, str]): UUID of Dataset in the data federation

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetMultipleDataFederationOut]
        """

        response = get_all_data_federations.sync(
            client=self._client,
            data_submitter_id=data_submitter_id,
            researcher_id=researcher_id,
            dataset_id=dataset_id,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetMultipleDataFederationOut)
        return response

    def register_data_federation(
        self,
        json_body: RegisterDataFederationIn,
    ) -> RegisterDataFederationOut:
        """Register Data Federation

         Register new data federation

        Args:
            json_body (RegisterDataFederationIn): Data Federation details to be registered

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[RegisterDataFederationOut]
        """

        response = register_data_federation.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, RegisterDataFederationOut)
        return response

    def get_data_federation(
        self,
        data_federation_id: str,
    ) -> GetDataFederationOut:
        """Get Data Federation

         Get the information about a data federation

        Args:
            data_federation_id (str): UUID of the data federation

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetDataFederationOut]
        """

        response = get_data_federation.sync(
            data_federation_id=data_federation_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetDataFederationOut)
        return response

    def update_data_federation(
        self,
        data_federation_id: str,
        json_body: UpdateDataFederationIn,
    ) -> None:
        """Update Data Federation

         Update data federation information

        Args:
            data_federation_id (str): UUID of the data federation
            json_body (UpdateDataFederationIn): Updated Data federation information

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        update_data_federation.sync(
            data_federation_id=data_federation_id,
            client=self._client,
            json_body=json_body,
        )

    def soft_delete_data_federation(
        self,
        data_federation_id: str,
    ) -> None:
        """Soft Delete Data Federation

         Disable the data federation

        Args:
            data_federation_id (str): UUID of the data federation to be deprovisioned

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        soft_delete_data_federation.sync(
            data_federation_id=data_federation_id,
            client=self._client,
        )

    def invite_researcher(
        self,
        data_federation_id: str,
        researcher_organization_id: str,
    ) -> None:
        """Invite Researcher

         Invite a researcher to join a data federation

        Args:
            data_federation_id (str): UUID of the data federation
            researcher_organization_id (str): UUID of the researcher organization to be invited

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        invite_researcher.sync(
            data_federation_id=data_federation_id,
            researcher_organization_id=researcher_organization_id,
            client=self._client,
        )

    def register_researcher(
        self,
        data_federation_id: str,
        researcher_organization_id: str,
    ) -> None:
        """Register Researcher

         Automatically add a researcher to the data federation, bypassing an invite path

        Args:
            data_federation_id (str): UUID of the data federation
            researcher_organization_id (str): UUID of the researcher organization to be added

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        register_researcher.sync(
            data_federation_id=data_federation_id,
            researcher_organization_id=researcher_organization_id,
            client=self._client,
        )

    def invite_data_submitter(
        self,
        data_federation_id: str,
        data_submitter_organization_id: str,
    ) -> None:
        """Invite Data Submitter

         Invite a data submitter to join a data federation

        Args:
            data_federation_id (str): UUID of the data federation
            data_submitter_organization_id (str): UUID of the data submitter organization to be
                invited

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        invite_data_submitter.sync(
            data_federation_id=data_federation_id,
            data_submitter_organization_id=data_submitter_organization_id,
            client=self._client,
        )

    def register_data_submitter(
        self,
        data_federation_id: str,
        data_submitter_organization_id: str,
    ) -> None:
        """Register Data Submitter

         Automatically add a data submitter to the data federation, bypassing an invite path

        Args:
            data_federation_id (str): UUID of the data federation
            data_submitter_organization_id (str): UUID of the data submitter organization to be
                invited

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        register_data_submitter.sync(
            data_federation_id=data_federation_id,
            data_submitter_organization_id=data_submitter_organization_id,
            client=self._client,
        )

    def add_data_model(
        self,
        data_federation_id: str,
        json_body: AddDataModelDataModel,
    ) -> None:
        """Add Data Model

         Add a data model to a data federation

        Args:
            data_federation_id (str): UUID of the data federation
            json_body (AddDataModelDataModel): Data model(json) to be added

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        add_data_model.sync(
            data_federation_id=data_federation_id,
            client=self._client,
            json_body=json_body,
        )

    def get_all_invites(
        self,
        organization_id: str,
    ) -> GetMultipleInviteOut:
        """Get All Invites

         Get list of all the pending invites received. Only ADMIN roles have access.

        Args:
            organization_id (str): UUID of the organization for which to list all the invited

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetMultipleInviteOut]
        """

        response = get_all_invites.sync(
            organization_id=organization_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetMultipleInviteOut)
        return response

    def get_invite(
        self,
        organization_id: str,
        invite_id: str,
    ) -> GetInviteOut:
        """Get Invite

         Get the information about an invite

        Args:
            organization_id (str): UUID of the invired organization
            invite_id (str): UUID of the invite to be fetched

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetInviteOut]
        """

        response = get_invite.sync(
            organization_id=organization_id,
            invite_id=invite_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetInviteOut)
        return response

    def accept_or_reject_invite(
        self,
        organization_id: str,
        invite_id: str,
        json_body: PatchInviteIn,
    ) -> Any:
        """Accept Or Reject Invite

         Accept or reject an invite

        Args:
            organization_id (str): UUID of the invited organization
            invite_id (str): UUID of the invite to be approved to rejected
            json_body (PatchInviteIn): The accpet or reject information

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Any]
        """

        response = accept_or_reject_invite.sync(
            organization_id=organization_id,
            invite_id=invite_id,
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, Any)
        return response

    def add_dataset(
        self,
        data_federation_id: str,
        dataset_id: str,
    ) -> None:
        """Add Dataset

         Add a dataset to a data federation

        Args:
            data_federation_id (str): UUID of the Data federation to which the dataset is being added
            dataset_id (str): UUID of the dataset that is being added to the data federation

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        add_dataset.sync(
            data_federation_id=data_federation_id,
            dataset_id=dataset_id,
            client=self._client,
        )

    def remove_dataset(
        self,
        data_federation_id: str,
        dataset_id: str,
    ) -> None:
        """Remove Dataset

         Remove a dataset from a data federation

        Args:
            data_federation_id (str): UUID of the Data federation from which the dataset is being
                removed
            dataset_id (str): UUID of the dataset that is being removed from the data federation

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        remove_dataset.sync(
            data_federation_id=data_federation_id,
            dataset_id=dataset_id,
            client=self._client,
        )

    def get_existing_dataset_key(
        self,
        data_federation_id: str,
        dataset_id: str,
    ) -> DatasetEncryptionKeyOut:
        """Get Existing Dataset Key

         Return a dataset encryption key by either retrieving and unwrapping

        Args:
            data_federation_id (str): UUID of the Data federation to which the dataset belongs
            dataset_id (str): UUID of the dataset for which the key is being requested

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[DatasetEncryptionKeyOut]
        """

        response = get_existing_dataset_key.sync(
            data_federation_id=data_federation_id,
            dataset_id=dataset_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, DatasetEncryptionKeyOut)
        return response

    def get_dataset_key(
        self,
        data_federation_id: str,
        dataset_id: str,
        create_if_not_found: Union[Unset, None, bool] = True,
    ) -> DatasetEncryptionKeyOut:
        """Get Dataset Key

         Return a dataset encryption key by either retrieving and unwrapping, or creating

        Args:
            data_federation_id (str): UUID of the Data federation to which the dataset belongs
            dataset_id (str): UUID of the dataset for which the key is being requested
            create_if_not_found (Union[Unset, None, bool]):  Default: True.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[DatasetEncryptionKeyOut]
        """

        response = get_dataset_key.sync(
            data_federation_id=data_federation_id,
            dataset_id=dataset_id,
            client=self._client,
            create_if_not_found=create_if_not_found,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, DatasetEncryptionKeyOut)
        return response

    def register_data_federation_provision(
        self,
        json_body: RegisterDataFederationProvisionIn,
    ) -> RegisterDataFederationProvisionOut:
        """Provision Data Federation

         Provision data federation SCNs

        Args:
            json_body (RegisterDataFederationProvisionIn): Information required for provsioning

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[RegisterDataFederationProvisionOut]
        """

        response = register_data_federation_provision.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, RegisterDataFederationProvisionOut)
        return response

    def get_data_federation_provision_info(
        self,
        provision_id: str,
    ) -> GetDataFederationProvision:
        """Get Data Federation Provision Info

         Get data federation provision SCNs

        Args:
            provision_id (str): Data Federation Provision Id

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetDataFederationProvision]
        """

        response = get_data_federation_provision_info.sync(
            provision_id=provision_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetDataFederationProvision)
        return response

    def get_all_data_federation_provision_info(
        self,
    ) -> GetMultipleDataFederationProvisionOut:
        """Get All Data Federation Provision Info

         Get all data federation provision SCNs

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetMultipleDataFederationProvisionOut]
        """

        response = get_all_data_federation_provision_info.sync(
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetMultipleDataFederationProvisionOut)
        return response

    def deprovision_data_federation(
        self,
        provision_id: str,
    ) -> None:
        """Deprovision Data Federation

         Deprovision data federation SCNs

        Args:
            provision_id (str): Data Federation Provision Id to deprovision

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        deprovision_data_federation.sync(
            provision_id=provision_id,
            client=self._client,
        )

    def get_all_datasets(
        self,
    ) -> GetMultipleDatasetOut:
        """Get All Datasets

         Get list of all the datasets for the current organization

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetMultipleDatasetOut]
        """

        response = get_all_datasets.sync(
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetMultipleDatasetOut)
        return response

    def register_dataset(
        self,
        json_body: RegisterDatasetIn,
    ) -> RegisterDatasetOut:
        """Register Dataset

         Register new dataset

        Args:
            json_body (RegisterDatasetIn): information required to register a dataset

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[RegisterDatasetOut]
        """

        response = register_dataset.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, RegisterDatasetOut)
        return response

    def get_dataset(
        self,
        dataset_id: str,
    ) -> GetDatasetOut:
        """Get Dataset

         Get the information about a dataset

        Args:
            dataset_id (str): UUID of the dataset being fetched

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetDatasetOut]
        """

        response = get_dataset.sync(
            dataset_id=dataset_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetDatasetOut)
        return response

    def update_dataset(
        self,
        dataset_id: str,
        json_body: UpdateDatasetIn,
    ) -> None:
        """Update Dataset

         Update dataset information

        Args:
            dataset_id (str): UUID of the dataset being updated
            json_body (UpdateDatasetIn): Updated dataset information

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        update_dataset.sync(
            dataset_id=dataset_id,
            client=self._client,
            json_body=json_body,
        )

    def soft_delete_dataset(
        self,
        dataset_id: str,
    ) -> None:
        """Soft Delete Dataset

         Disable the dataset

        Args:
            dataset_id (str): UUID of the dataset being soft deleted

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        soft_delete_dataset.sync(
            dataset_id=dataset_id,
            client=self._client,
        )

    def get_all_dataset_versions(
        self,
        json_body: str,
    ) -> GetMultipleDatasetVersionOut:
        """Get All Dataset Versions

         Get list of all the dataset-versions for the dataset

        Args:
            json_body (str): UUID of the dataset

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetMultipleDatasetVersionOut]
        """

        response = get_all_dataset_versions.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetMultipleDatasetVersionOut)
        return response

    def register_dataset_version(
        self,
        json_body: RegisterDatasetVersionIn,
    ) -> RegisterDatasetVersionOut:
        """Register Dataset Version

         Register new dataset-version

        Args:
            json_body (RegisterDatasetVersionIn): Dataset Version information to register

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[RegisterDatasetVersionOut]
        """

        response = register_dataset_version.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, RegisterDatasetVersionOut)
        return response

    def get_dataset_version(
        self,
        dataset_version_id: str,
    ) -> GetDatasetVersionOut:
        """Get Dataset Version

         Get the information about a dataset

        Args:
            dataset_version_id (str): UUID of the dataset version

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetDatasetVersionOut]
        """

        response = get_dataset_version.sync(
            dataset_version_id=dataset_version_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetDatasetVersionOut)
        return response

    def update_dataset_version(
        self,
        dataset_version_id: str,
        json_body: UpdateDatasetVersionIn,
    ) -> None:
        """Update Dataset Version

         Update dataset information

        Args:
            dataset_version_id (str): UUID of the dataset version
            json_body (UpdateDatasetVersionIn): Object containing the information to be updated

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        update_dataset_version.sync(
            dataset_version_id=dataset_version_id,
            client=self._client,
            json_body=json_body,
        )

    def soft_delete_dataset_version(
        self,
        dataset_version_id: str,
    ) -> None:
        """Soft Delete Dataset Version

         Disable a dataset version

        Args:
            dataset_version_id (str): UUID of the dataset version

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        soft_delete_dataset_version.sync(
            dataset_version_id=dataset_version_id,
            client=self._client,
        )

    def get_dataset_version_connection_string(
        self,
        dataset_version_id: str,
    ) -> GetDatasetVersionConnectionStringOut:
        """Get Dataset Version Connection String

         Get the write only connection string for the dataset version upload

        Args:
            dataset_version_id (str): UUID of the dataset version

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetDatasetVersionConnectionStringOut]
        """

        response = get_dataset_version_connection_string.sync(
            dataset_version_id=dataset_version_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetDatasetVersionConnectionStringOut)
        return response

    def get_all_secure_computation_nodes(
        self,
        data_federation_provision_id: str,
    ) -> GetMultipleSecureComputationNodeOut:
        """Get All Secure Computation Nodes

         Get list of all the secure_computation_node for the current user and federation provision

        Args:
            data_federation_provision_id (str): Data federation provision id

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetMultipleSecureComputationNodeOut]
        """

        response = get_all_secure_computation_nodes.sync(
            client=self._client,
            data_federation_provision_id=data_federation_provision_id,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetMultipleSecureComputationNodeOut)
        return response

    def get_secure_computation_node(
        self,
        secure_computation_node_id: str,
    ) -> GetSecureComputationNodeOut:
        """Get Secure Computation Node

         Get the information about a secure computation node

        Args:
            secure_computation_node_id (str): UUID of Secure Computation Node

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[GetSecureComputationNodeOut]
        """

        response = get_secure_computation_node.sync(
            secure_computation_node_id=secure_computation_node_id,
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, GetSecureComputationNodeOut)
        return response

    def update_secure_computation_node(
        self,
        secure_computation_node_id: str,
        json_body: UpdateSecureComputationNodeIn,
    ) -> None:
        """Update Secure Computation Node

         Update secure computation node information

        Args:
            secure_computation_node_id (str): UUID of Secure Computation Node
            json_body (UpdateSecureComputationNodeIn): Updated Secure Computation Node information

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        update_secure_computation_node.sync(
            secure_computation_node_id=secure_computation_node_id,
            client=self._client,
            json_body=json_body,
        )


class SyncOperations:
    def __init__(self, client: Client) -> None:
        self._client = client

    def login(
        self,
        form_data: BodyLogin,
    ) -> LoginSuccessOut:
        """Login For Access Token

         User login with email and password

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[LoginSuccessOut]
        """

        response = login.sync(
            client=self._client,
            form_data=form_data,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, LoginSuccessOut)
        return response

    def get_refresh_token(
        self,
        json_body: RefreshTokenIn,
    ) -> LoginSuccessOut:
        """Refresh For Access Token

         Refresh the JWT token for the user

        Args:
            json_body (RefreshTokenIn): Refresh token request

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[LoginSuccessOut]
        """

        response = get_refresh_token.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, LoginSuccessOut)
        return response

    def register_organization(
        self,
        json_body: RegisterOrganizationIn,
    ) -> RegisterOrganizationOut:
        """Register Organization

         Register new organization and the admin user

        Args:
            json_body (RegisterOrganizationIn): Organization details

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[RegisterOrganizationOut]
        """

        response = register_organization.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, RegisterOrganizationOut)
        return response

    def drop_database(
        self,
    ) -> None:
        """Register Dataset

         Drop the database

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[None]
        """

        drop_database.sync(
            client=self._client,
        )
