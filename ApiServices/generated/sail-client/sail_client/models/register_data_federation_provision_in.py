from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.secure_computation_node_size import SecureComputationNodeSize

T = TypeVar("T", bound="RegisterDataFederationProvisionIn")


@attr.s(auto_attribs=True)
class RegisterDataFederationProvisionIn:
    """
    Attributes:
        data_federation_id (str):
        secure_computation_nodes_size (SecureComputationNodeSize): An enumeration.
    """

    data_federation_id: str
    secure_computation_nodes_size: SecureComputationNodeSize
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_federation_id = self.data_federation_id
        secure_computation_nodes_size = self.secure_computation_nodes_size.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_federation_id": data_federation_id,
                "secure_computation_nodes_size": secure_computation_nodes_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data_federation_id = d.pop("data_federation_id")

        secure_computation_nodes_size = SecureComputationNodeSize(d.pop("secure_computation_nodes_size"))

        register_data_federation_provision_in = cls(
            data_federation_id=data_federation_id,
            secure_computation_nodes_size=secure_computation_nodes_size,
        )

        register_data_federation_provision_in.additional_properties = d
        return register_data_federation_provision_in

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
