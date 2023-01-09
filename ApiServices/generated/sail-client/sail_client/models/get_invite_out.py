import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.invite_state import InviteState
from ..models.invite_type import InviteType

if TYPE_CHECKING:
    from ..models.basic_object_info import BasicObjectInfo


T = TypeVar("T", bound="GetInviteOut")


@attr.s(auto_attribs=True)
class GetInviteOut:
    """
    Attributes:
        id (str):
        data_federation (BasicObjectInfo):
        inviter_user (BasicObjectInfo):
        inviter_organization (BasicObjectInfo):
        state (InviteState): An enumeration.
        created_time (datetime.datetime):
        expiry_time (datetime.datetime):
        type (InviteType): An enumeration.
    """

    id: str
    data_federation: "BasicObjectInfo"
    inviter_user: "BasicObjectInfo"
    inviter_organization: "BasicObjectInfo"
    state: InviteState
    created_time: datetime.datetime
    expiry_time: datetime.datetime
    type: InviteType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        data_federation = self.data_federation.to_dict()

        inviter_user = self.inviter_user.to_dict()

        inviter_organization = self.inviter_organization.to_dict()

        state = self.state.value

        created_time = self.created_time.isoformat()

        expiry_time = self.expiry_time.isoformat()

        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "data_federation": data_federation,
                "inviter_user": inviter_user,
                "inviter_organization": inviter_organization,
                "state": state,
                "created_time": created_time,
                "expiry_time": expiry_time,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.basic_object_info import BasicObjectInfo

        d = src_dict.copy()
        id = d.pop("id")

        data_federation = BasicObjectInfo.from_dict(d.pop("data_federation"))

        inviter_user = BasicObjectInfo.from_dict(d.pop("inviter_user"))

        inviter_organization = BasicObjectInfo.from_dict(d.pop("inviter_organization"))

        state = InviteState(d.pop("state"))

        created_time = isoparse(d.pop("created_time"))

        expiry_time = isoparse(d.pop("expiry_time"))

        type = InviteType(d.pop("type"))

        get_invite_out = cls(
            id=id,
            data_federation=data_federation,
            inviter_user=inviter_user,
            inviter_organization=inviter_organization,
            state=state,
            created_time=created_time,
            expiry_time=expiry_time,
            type=type,
        )

        get_invite_out.additional_properties = d
        return get_invite_out

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
