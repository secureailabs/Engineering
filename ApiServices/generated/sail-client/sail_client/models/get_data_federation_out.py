import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.data_federation_data_format import DataFederationDataFormat
from ..models.data_federation_state import DataFederationState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.basic_object_info import BasicObjectInfo


T = TypeVar("T", bound="GetDataFederationOut")


@attr.s(auto_attribs=True)
class GetDataFederationOut:
    """
    Attributes:
        name (str):
        description (str):
        data_format (DataFederationDataFormat): An enumeration.
        data_model (str):
        id (str):
        organization (BasicObjectInfo):
        state (DataFederationState): An enumeration.
        data_submitter_organizations (List['BasicObjectInfo']):
        research_organizations (List['BasicObjectInfo']):
        datasets (List['BasicObjectInfo']):
        creation_time (Union[Unset, datetime.datetime]):
        data_submitter_organizations_invites_id (Union[Unset, List[str]]):
        research_organizations_invites_id (Union[Unset, List[str]]):
    """

    name: str
    description: str
    data_format: DataFederationDataFormat
    data_model: str
    id: str
    organization: "BasicObjectInfo"
    state: DataFederationState
    data_submitter_organizations: List["BasicObjectInfo"]
    research_organizations: List["BasicObjectInfo"]
    datasets: List["BasicObjectInfo"]
    creation_time: Union[Unset, datetime.datetime] = UNSET
    data_submitter_organizations_invites_id: Union[Unset, List[str]] = UNSET
    research_organizations_invites_id: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        data_format = self.data_format.value

        data_model = self.data_model
        id = self.id
        organization = self.organization.to_dict()

        state = self.state.value

        data_submitter_organizations = []
        for data_submitter_organizations_item_data in self.data_submitter_organizations:
            data_submitter_organizations_item = data_submitter_organizations_item_data.to_dict()

            data_submitter_organizations.append(data_submitter_organizations_item)

        research_organizations = []
        for research_organizations_item_data in self.research_organizations:
            research_organizations_item = research_organizations_item_data.to_dict()

            research_organizations.append(research_organizations_item)

        datasets = []
        for datasets_item_data in self.datasets:
            datasets_item = datasets_item_data.to_dict()

            datasets.append(datasets_item)

        creation_time: Union[Unset, str] = UNSET
        if not isinstance(self.creation_time, Unset):
            creation_time = self.creation_time.isoformat()

        data_submitter_organizations_invites_id: Union[Unset, List[str]] = UNSET
        if not isinstance(self.data_submitter_organizations_invites_id, Unset):
            data_submitter_organizations_invites_id = self.data_submitter_organizations_invites_id

        research_organizations_invites_id: Union[Unset, List[str]] = UNSET
        if not isinstance(self.research_organizations_invites_id, Unset):
            research_organizations_invites_id = self.research_organizations_invites_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "data_format": data_format,
                "data_model": data_model,
                "id": id,
                "organization": organization,
                "state": state,
                "data_submitter_organizations": data_submitter_organizations,
                "research_organizations": research_organizations,
                "datasets": datasets,
            }
        )
        if creation_time is not UNSET:
            field_dict["creation_time"] = creation_time
        if data_submitter_organizations_invites_id is not UNSET:
            field_dict["data_submitter_organizations_invites_id"] = data_submitter_organizations_invites_id
        if research_organizations_invites_id is not UNSET:
            field_dict["research_organizations_invites_id"] = research_organizations_invites_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.basic_object_info import BasicObjectInfo

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        data_format = DataFederationDataFormat(d.pop("data_format"))

        data_model = d.pop("data_model")

        id = d.pop("id")

        organization = BasicObjectInfo.from_dict(d.pop("organization"))

        state = DataFederationState(d.pop("state"))

        data_submitter_organizations = []
        _data_submitter_organizations = d.pop("data_submitter_organizations")
        for data_submitter_organizations_item_data in _data_submitter_organizations:
            data_submitter_organizations_item = BasicObjectInfo.from_dict(data_submitter_organizations_item_data)

            data_submitter_organizations.append(data_submitter_organizations_item)

        research_organizations = []
        _research_organizations = d.pop("research_organizations")
        for research_organizations_item_data in _research_organizations:
            research_organizations_item = BasicObjectInfo.from_dict(research_organizations_item_data)

            research_organizations.append(research_organizations_item)

        datasets = []
        _datasets = d.pop("datasets")
        for datasets_item_data in _datasets:
            datasets_item = BasicObjectInfo.from_dict(datasets_item_data)

            datasets.append(datasets_item)

        _creation_time = d.pop("creation_time", UNSET)
        creation_time: Union[Unset, datetime.datetime]
        if isinstance(_creation_time, Unset):
            creation_time = UNSET
        else:
            creation_time = isoparse(_creation_time)

        data_submitter_organizations_invites_id = cast(
            List[str], d.pop("data_submitter_organizations_invites_id", UNSET)
        )

        research_organizations_invites_id = cast(List[str], d.pop("research_organizations_invites_id", UNSET))

        get_data_federation_out = cls(
            name=name,
            description=description,
            data_format=data_format,
            data_model=data_model,
            id=id,
            organization=organization,
            state=state,
            data_submitter_organizations=data_submitter_organizations,
            research_organizations=research_organizations,
            datasets=datasets,
            creation_time=creation_time,
            data_submitter_organizations_invites_id=data_submitter_organizations_invites_id,
            research_organizations_invites_id=research_organizations_invites_id,
        )

        get_data_federation_out.additional_properties = d
        return get_data_federation_out

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
