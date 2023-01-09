import datetime
from typing import Any, Dict, List, Type, TypeVar, cast

import attr
from dateutil.parser import isoparse

from ..models.secure_computation_node_size import SecureComputationNodeSize

T = TypeVar("T", bound="RegisterDataFederationProvisionOut")


@attr.s(auto_attribs=True)
class RegisterDataFederationProvisionOut:
    """
    Attributes:
        data_federation_id (str):
        secure_computation_nodes_size (SecureComputationNodeSize): An enumeration.
        id (str):
        creation_time (datetime.datetime):
        organization_id (str):
        smart_broker_id (str):
        secure_computation_nodes_id (List[str]):
    """

    data_federation_id: str
    secure_computation_nodes_size: SecureComputationNodeSize
    id: str
    creation_time: datetime.datetime
    organization_id: str
    smart_broker_id: str
    secure_computation_nodes_id: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_federation_id = self.data_federation_id
        secure_computation_nodes_size = self.secure_computation_nodes_size.value

        id = self.id
        creation_time = self.creation_time.isoformat()

        organization_id = self.organization_id
        smart_broker_id = self.smart_broker_id
        secure_computation_nodes_id = self.secure_computation_nodes_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_federation_id": data_federation_id,
                "secure_computation_nodes_size": secure_computation_nodes_size,
                "id": id,
                "creation_time": creation_time,
                "organization_id": organization_id,
                "smart_broker_id": smart_broker_id,
                "secure_computation_nodes_id": secure_computation_nodes_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data_federation_id = d.pop("data_federation_id")

        secure_computation_nodes_size = SecureComputationNodeSize(d.pop("secure_computation_nodes_size"))

        id = d.pop("id")

        creation_time = isoparse(d.pop("creation_time"))

        organization_id = d.pop("organization_id")

        smart_broker_id = d.pop("smart_broker_id")

        secure_computation_nodes_id = cast(List[str], d.pop("secure_computation_nodes_id"))

        register_data_federation_provision_out = cls(
            data_federation_id=data_federation_id,
            secure_computation_nodes_size=secure_computation_nodes_size,
            id=id,
            creation_time=creation_time,
            organization_id=organization_id,
            smart_broker_id=smart_broker_id,
            secure_computation_nodes_id=secure_computation_nodes_id,
        )

        register_data_federation_provision_out.additional_properties = d
        return register_data_federation_provision_out

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
