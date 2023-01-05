import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.dataset_format import DatasetFormat
from ..models.dataset_state import DatasetState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.basic_object_info import BasicObjectInfo


T = TypeVar("T", bound="GetDatasetOut")


@attr.s(auto_attribs=True)
class GetDatasetOut:
    """
    Attributes:
        name (str):
        description (str):
        tags (str):
        format_ (DatasetFormat): An enumeration.
        id (str):
        organization (BasicObjectInfo):
        state (DatasetState): An enumeration.
        creation_time (Union[Unset, datetime.datetime]):
        note (Union[Unset, str]):
    """

    name: str
    description: str
    tags: str
    format_: DatasetFormat
    id: str
    organization: "BasicObjectInfo"
    state: DatasetState
    creation_time: Union[Unset, datetime.datetime] = UNSET
    note: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        tags = self.tags
        format_ = self.format_.value

        id = self.id
        organization = self.organization.to_dict()

        state = self.state.value

        creation_time: Union[Unset, str] = UNSET
        if not isinstance(self.creation_time, Unset):
            creation_time = self.creation_time.isoformat()

        note = self.note

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "tags": tags,
                "format": format_,
                "id": id,
                "organization": organization,
                "state": state,
            }
        )
        if creation_time is not UNSET:
            field_dict["creation_time"] = creation_time
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.basic_object_info import BasicObjectInfo

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        tags = d.pop("tags")

        format_ = DatasetFormat(d.pop("format"))

        id = d.pop("id")

        organization = BasicObjectInfo.from_dict(d.pop("organization"))

        state = DatasetState(d.pop("state"))

        _creation_time = d.pop("creation_time", UNSET)
        creation_time: Union[Unset, datetime.datetime]
        if isinstance(_creation_time, Unset):
            creation_time = UNSET
        else:
            creation_time = isoparse(_creation_time)

        note = d.pop("note", UNSET)

        get_dataset_out = cls(
            name=name,
            description=description,
            tags=tags,
            format_=format_,
            id=id,
            organization=organization,
            state=state,
            creation_time=creation_time,
            note=note,
        )

        get_dataset_out.additional_properties = d
        return get_dataset_out

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
