import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.dataset_version_state import DatasetVersionState

if TYPE_CHECKING:
    from ..models.basic_object_info import BasicObjectInfo


T = TypeVar("T", bound="GetDatasetVersionOut")


@attr.s(auto_attribs=True)
class GetDatasetVersionOut:
    """
    Attributes:
        dataset_id (str):
        description (str):
        name (str):
        id (str):
        dataset_version_created_time (datetime.datetime):
        organization (BasicObjectInfo):
        state (DatasetVersionState): An enumeration.
        note (str):
    """

    dataset_id: str
    description: str
    name: str
    id: str
    dataset_version_created_time: datetime.datetime
    organization: "BasicObjectInfo"
    state: DatasetVersionState
    note: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dataset_id = self.dataset_id
        description = self.description
        name = self.name
        id = self.id
        dataset_version_created_time = self.dataset_version_created_time.isoformat()

        organization = self.organization.to_dict()

        state = self.state.value

        note = self.note

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset_id": dataset_id,
                "description": description,
                "name": name,
                "id": id,
                "dataset_version_created_time": dataset_version_created_time,
                "organization": organization,
                "state": state,
                "note": note,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.basic_object_info import BasicObjectInfo

        d = src_dict.copy()
        dataset_id = d.pop("dataset_id")

        description = d.pop("description")

        name = d.pop("name")

        id = d.pop("id")

        dataset_version_created_time = isoparse(d.pop("dataset_version_created_time"))

        organization = BasicObjectInfo.from_dict(d.pop("organization"))

        state = DatasetVersionState(d.pop("state"))

        note = d.pop("note")

        get_dataset_version_out = cls(
            dataset_id=dataset_id,
            description=description,
            name=name,
            id=id,
            dataset_version_created_time=dataset_version_created_time,
            organization=organization,
            state=state,
            note=note,
        )

        get_dataset_version_out.additional_properties = d
        return get_dataset_version_out

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
