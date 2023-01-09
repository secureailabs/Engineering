from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.user_account_state import UserAccountState
from ..models.user_role import UserRole

T = TypeVar("T", bound="UpdateUserIn")


@attr.s(auto_attribs=True)
class UpdateUserIn:
    """
    Attributes:
        job_title (str):
        role (UserRole): An enumeration.
        account_state (UserAccountState): An enumeration.
        avatar (str):
    """

    job_title: str
    role: UserRole
    account_state: UserAccountState
    avatar: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_title = self.job_title
        role = self.role.value

        account_state = self.account_state.value

        avatar = self.avatar

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_title": job_title,
                "role": role,
                "account_state": account_state,
                "avatar": avatar,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_title = d.pop("job_title")

        role = UserRole(d.pop("role"))

        account_state = UserAccountState(d.pop("account_state"))

        avatar = d.pop("avatar")

        update_user_in = cls(
            job_title=job_title,
            role=role,
            account_state=account_state,
            avatar=avatar,
        )

        update_user_in.additional_properties = d
        return update_user_in

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
