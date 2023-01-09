from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.get_secure_computation_node_out import GetSecureComputationNodeOut


T = TypeVar("T", bound="GetMultipleSecureComputationNodeOut")


@attr.s(auto_attribs=True)
class GetMultipleSecureComputationNodeOut:
    """
    Attributes:
        secure_computation_nodes (List['GetSecureComputationNodeOut']):
    """

    secure_computation_nodes: List["GetSecureComputationNodeOut"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        secure_computation_nodes = []
        for secure_computation_nodes_item_data in self.secure_computation_nodes:
            secure_computation_nodes_item = secure_computation_nodes_item_data.to_dict()

            secure_computation_nodes.append(secure_computation_nodes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "secure_computation_nodes": secure_computation_nodes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_secure_computation_node_out import GetSecureComputationNodeOut

        d = src_dict.copy()
        secure_computation_nodes = []
        _secure_computation_nodes = d.pop("secure_computation_nodes")
        for secure_computation_nodes_item_data in _secure_computation_nodes:
            secure_computation_nodes_item = GetSecureComputationNodeOut.from_dict(secure_computation_nodes_item_data)

            secure_computation_nodes.append(secure_computation_nodes_item)

        get_multiple_secure_computation_node_out = cls(
            secure_computation_nodes=secure_computation_nodes,
        )

        get_multiple_secure_computation_node_out.additional_properties = d
        return get_multiple_secure_computation_node_out

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
