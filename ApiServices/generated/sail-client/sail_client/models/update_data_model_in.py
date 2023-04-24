from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.data_model_state import DataModelState
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateDataModelIn")


@attr.s(auto_attribs=True)
class UpdateDataModelIn:
    """
    Attributes:
        data_model_dataframe_to_add (Union[Unset, List[str]]): The data_model_dataframes to add to the data model
        data_model_dataframe_to_remove (Union[Unset, List[str]]): The data_model_dataframes to remove from the data
            model
        state (Union[Unset, DataModelState]): The state of the data model
    """

    data_model_dataframe_to_add: Union[Unset, List[str]] = UNSET
    data_model_dataframe_to_remove: Union[Unset, List[str]] = UNSET
    state: Union[Unset, DataModelState] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_model_dataframe_to_add: Union[Unset, List[str]] = UNSET
        if not isinstance(self.data_model_dataframe_to_add, Unset):
            data_model_dataframe_to_add = self.data_model_dataframe_to_add

        data_model_dataframe_to_remove: Union[Unset, List[str]] = UNSET
        if not isinstance(self.data_model_dataframe_to_remove, Unset):
            data_model_dataframe_to_remove = self.data_model_dataframe_to_remove

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_model_dataframe_to_add is not UNSET:
            field_dict["data_model_dataframe_to_add"] = data_model_dataframe_to_add
        if data_model_dataframe_to_remove is not UNSET:
            field_dict["data_model_dataframe_to_remove"] = data_model_dataframe_to_remove
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data_model_dataframe_to_add = cast(List[str], d.pop("data_model_dataframe_to_add", UNSET))

        data_model_dataframe_to_remove = cast(List[str], d.pop("data_model_dataframe_to_remove", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, DataModelState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = DataModelState(_state)

        update_data_model_in = cls(
            data_model_dataframe_to_add=data_model_dataframe_to_add,
            data_model_dataframe_to_remove=data_model_dataframe_to_remove,
            state=state,
        )

        update_data_model_in.additional_properties = d
        return update_data_model_in

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
