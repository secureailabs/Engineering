import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.secure_computation_node_state import SecureComputationNodeState
from ..models.secure_computation_node_type import SecureComputationNodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.basic_object_info import BasicObjectInfo


T = TypeVar("T", bound="GetSecureComputationNodeOut")


@attr.s(auto_attribs=True)
class GetSecureComputationNodeOut:
    """
    Attributes:
        id (str):
        data_federation (BasicObjectInfo):
        dataset (BasicObjectInfo):
        dataset_version (BasicObjectInfo):
        researcher_user (str):
        type (SecureComputationNodeType): An enumeration.
        timestamp (datetime.datetime):
        state (SecureComputationNodeState): An enumeration.
        researcher (Union[Unset, BasicObjectInfo]):
        data_owner (Union[Unset, BasicObjectInfo]):
        detail (Union[Unset, str]):
        ipaddress (Union[Unset, str]):
    """

    id: str
    data_federation: "BasicObjectInfo"
    dataset: "BasicObjectInfo"
    dataset_version: "BasicObjectInfo"
    researcher_user: str
    type: SecureComputationNodeType
    timestamp: datetime.datetime
    state: SecureComputationNodeState
    researcher: Union[Unset, "BasicObjectInfo"] = UNSET
    data_owner: Union[Unset, "BasicObjectInfo"] = UNSET
    detail: Union[Unset, str] = UNSET
    ipaddress: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        data_federation = self.data_federation.to_dict()

        dataset = self.dataset.to_dict()

        dataset_version = self.dataset_version.to_dict()

        researcher_user = self.researcher_user
        type = self.type.value

        timestamp = self.timestamp.isoformat()

        state = self.state.value

        researcher: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.researcher, Unset):
            researcher = self.researcher.to_dict()

        data_owner: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data_owner, Unset):
            data_owner = self.data_owner.to_dict()

        detail = self.detail
        ipaddress = self.ipaddress

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "data_federation": data_federation,
                "dataset": dataset,
                "dataset_version": dataset_version,
                "researcher_user": researcher_user,
                "type": type,
                "timestamp": timestamp,
                "state": state,
            }
        )
        if researcher is not UNSET:
            field_dict["researcher"] = researcher
        if data_owner is not UNSET:
            field_dict["data_owner"] = data_owner
        if detail is not UNSET:
            field_dict["detail"] = detail
        if ipaddress is not UNSET:
            field_dict["ipaddress"] = ipaddress

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.basic_object_info import BasicObjectInfo

        d = src_dict.copy()
        id = d.pop("id")

        data_federation = BasicObjectInfo.from_dict(d.pop("data_federation"))

        dataset = BasicObjectInfo.from_dict(d.pop("dataset"))

        dataset_version = BasicObjectInfo.from_dict(d.pop("dataset_version"))

        researcher_user = d.pop("researcher_user")

        type = SecureComputationNodeType(d.pop("type"))

        timestamp = isoparse(d.pop("timestamp"))

        state = SecureComputationNodeState(d.pop("state"))

        _researcher = d.pop("researcher", UNSET)
        researcher: Union[Unset, BasicObjectInfo]
        if isinstance(_researcher, Unset):
            researcher = UNSET
        else:
            researcher = BasicObjectInfo.from_dict(_researcher)

        _data_owner = d.pop("data_owner", UNSET)
        data_owner: Union[Unset, BasicObjectInfo]
        if isinstance(_data_owner, Unset):
            data_owner = UNSET
        else:
            data_owner = BasicObjectInfo.from_dict(_data_owner)

        detail = d.pop("detail", UNSET)

        ipaddress = d.pop("ipaddress", UNSET)

        get_secure_computation_node_out = cls(
            id=id,
            data_federation=data_federation,
            dataset=dataset,
            dataset_version=dataset_version,
            researcher_user=researcher_user,
            type=type,
            timestamp=timestamp,
            state=state,
            researcher=researcher,
            data_owner=data_owner,
            detail=detail,
            ipaddress=ipaddress,
        )

        get_secure_computation_node_out.additional_properties = d
        return get_secure_computation_node_out

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
