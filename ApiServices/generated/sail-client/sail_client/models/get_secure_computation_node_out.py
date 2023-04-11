import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.secure_computation_node_state import SecureComputationNodeState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.basic_object_info import BasicObjectInfo
    from ..models.dataset_basic_information import DatasetBasicInformation


T = TypeVar("T", bound="GetSecureComputationNodeOut")


@attr.s(auto_attribs=True)
class GetSecureComputationNodeOut:
    """
    Attributes:
        id (str):
        data_federation (BasicObjectInfo):
        datasets (List['DatasetBasicInformation']):
        researcher_user (str):
        timestamp (datetime.datetime):
        state (SecureComputationNodeState): An enumeration.
        researcher (Union[Unset, BasicObjectInfo]):
        detail (Union[Unset, str]):
        ipaddress (Union[Unset, str]):
    """

    id: str
    data_federation: "BasicObjectInfo"
    datasets: List["DatasetBasicInformation"]
    researcher_user: str
    timestamp: datetime.datetime
    state: SecureComputationNodeState
    researcher: Union[Unset, "BasicObjectInfo"] = UNSET
    detail: Union[Unset, str] = UNSET
    ipaddress: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        data_federation = self.data_federation.to_dict()

        datasets = []
        for datasets_item_data in self.datasets:
            datasets_item = datasets_item_data.to_dict()

            datasets.append(datasets_item)

        researcher_user = self.researcher_user
        timestamp = self.timestamp.isoformat()

        state = self.state.value

        researcher: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.researcher, Unset):
            researcher = self.researcher.to_dict()

        detail = self.detail
        ipaddress = self.ipaddress

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "data_federation": data_federation,
                "datasets": datasets,
                "researcher_user": researcher_user,
                "timestamp": timestamp,
                "state": state,
            }
        )
        if researcher is not UNSET:
            field_dict["researcher"] = researcher
        if detail is not UNSET:
            field_dict["detail"] = detail
        if ipaddress is not UNSET:
            field_dict["ipaddress"] = ipaddress

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.basic_object_info import BasicObjectInfo
        from ..models.dataset_basic_information import DatasetBasicInformation

        d = src_dict.copy()
        id = d.pop("id")

        data_federation = BasicObjectInfo.from_dict(d.pop("data_federation"))

        datasets = []
        _datasets = d.pop("datasets")
        for datasets_item_data in _datasets:
            datasets_item = DatasetBasicInformation.from_dict(datasets_item_data)

            datasets.append(datasets_item)

        researcher_user = d.pop("researcher_user")

        timestamp = isoparse(d.pop("timestamp"))

        state = SecureComputationNodeState(d.pop("state"))

        _researcher = d.pop("researcher", UNSET)
        researcher: Union[Unset, BasicObjectInfo]
        if isinstance(_researcher, Unset):
            researcher = UNSET
        else:
            researcher = BasicObjectInfo.from_dict(_researcher)

        detail = d.pop("detail", UNSET)

        ipaddress = d.pop("ipaddress", UNSET)

        get_secure_computation_node_out = cls(
            id=id,
            data_federation=data_federation,
            datasets=datasets,
            researcher_user=researcher_user,
            timestamp=timestamp,
            state=state,
            researcher=researcher,
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
