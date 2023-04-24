import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.data_federation_provision_state import DataFederationProvisionState
from ..models.secure_computation_node_size import SecureComputationNodeSize
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetDataFederationProvision")


@attr.s(auto_attribs=True)
class GetDataFederationProvision:
    """
    Attributes:
        data_federation_id (str):
        secure_computation_nodes_size (SecureComputationNodeSize): An enumeration.
        id (str):
        organization_id (str):
        secure_computation_node_id (str):
        state (DataFederationProvisionState): An enumeration.
        creation_time (Union[Unset, datetime.datetime]):
    """

    data_federation_id: str
    secure_computation_nodes_size: SecureComputationNodeSize
    id: str
    organization_id: str
    secure_computation_node_id: str
    state: DataFederationProvisionState
    creation_time: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_federation_id = self.data_federation_id
        secure_computation_nodes_size = self.secure_computation_nodes_size.value

        id = self.id
        organization_id = self.organization_id
        secure_computation_node_id = self.secure_computation_node_id
        state = self.state.value

        creation_time: Union[Unset, str] = UNSET
        if not isinstance(self.creation_time, Unset):
            creation_time = self.creation_time.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_federation_id": data_federation_id,
                "secure_computation_nodes_size": secure_computation_nodes_size,
                "id": id,
                "organization_id": organization_id,
                "secure_computation_node_id": secure_computation_node_id,
                "state": state,
            }
        )
        if creation_time is not UNSET:
            field_dict["creation_time"] = creation_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data_federation_id = d.pop("data_federation_id")

        secure_computation_nodes_size = SecureComputationNodeSize(d.pop("secure_computation_nodes_size"))

        id = d.pop("id")

        organization_id = d.pop("organization_id")

        secure_computation_node_id = d.pop("secure_computation_node_id")

        state = DataFederationProvisionState(d.pop("state"))

        _creation_time = d.pop("creation_time", UNSET)
        creation_time: Union[Unset, datetime.datetime]
        if isinstance(_creation_time, Unset):
            creation_time = UNSET
        else:
            creation_time = isoparse(_creation_time)

        get_data_federation_provision = cls(
            data_federation_id=data_federation_id,
            secure_computation_nodes_size=secure_computation_nodes_size,
            id=id,
            organization_id=organization_id,
            secure_computation_node_id=secure_computation_node_id,
            state=state,
            creation_time=creation_time,
        )

        get_data_federation_provision.additional_properties = d
        return get_data_federation_provision

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
