from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.get_invite_out import GetInviteOut


T = TypeVar("T", bound="GetMultipleInviteOut")


@attr.s(auto_attribs=True)
class GetMultipleInviteOut:
    """
    Attributes:
        invites (List['GetInviteOut']):
    """

    invites: List["GetInviteOut"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        invites = []
        for invites_item_data in self.invites:
            invites_item = invites_item_data.to_dict()

            invites.append(invites_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "invites": invites,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_invite_out import GetInviteOut

        d = src_dict.copy()
        invites = []
        _invites = d.pop("invites")
        for invites_item_data in _invites:
            invites_item = GetInviteOut.from_dict(invites_item_data)

            invites.append(invites_item)

        get_multiple_invite_out = cls(
            invites=invites,
        )

        get_multiple_invite_out.additional_properties = d
        return get_multiple_invite_out

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
