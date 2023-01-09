from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.secure_computation_node_state import SecureComputationNodeState
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateSecureComputationNodeIn")


@attr.s(auto_attribs=True)
class UpdateSecureComputationNodeIn:
    """
    Attributes:
        state (Union[Unset, SecureComputationNodeState]): An enumeration.
    """

    state: Union[Unset, SecureComputationNodeState] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _state = d.pop("state", UNSET)
        state: Union[Unset, SecureComputationNodeState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = SecureComputationNodeState(_state)

        update_secure_computation_node_in = cls(
            state=state,
        )

        update_secure_computation_node_in.additional_properties = d
        return update_secure_computation_node_in

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
