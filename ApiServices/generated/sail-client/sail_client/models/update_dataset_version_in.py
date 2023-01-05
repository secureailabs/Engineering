from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dataset_version_state import DatasetVersionState
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateDatasetVersionIn")


@attr.s(auto_attribs=True)
class UpdateDatasetVersionIn:
    """
    Attributes:
        description (Union[Unset, str]):
        state (Union[Unset, DatasetVersionState]): An enumeration.
    """

    description: Union[Unset, str] = UNSET
    state: Union[Unset, DatasetVersionState] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, DatasetVersionState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = DatasetVersionState(_state)

        update_dataset_version_in = cls(
            description=description,
            state=state,
        )

        update_dataset_version_in.additional_properties = d
        return update_dataset_version_in

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
