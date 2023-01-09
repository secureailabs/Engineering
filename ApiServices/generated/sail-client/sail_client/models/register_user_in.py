from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.user_role import UserRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisterUserIn")


@attr.s(auto_attribs=True)
class RegisterUserIn:
    """
    Attributes:
        name (str):
        email (str):
        job_title (str):
        role (UserRole): An enumeration.
        password (str):
        avatar (Union[Unset, str]):
    """

    name: str
    email: str
    job_title: str
    role: UserRole
    password: str
    avatar: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        email = self.email
        job_title = self.job_title
        role = self.role.value

        password = self.password
        avatar = self.avatar

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "email": email,
                "job_title": job_title,
                "role": role,
                "password": password,
            }
        )
        if avatar is not UNSET:
            field_dict["avatar"] = avatar

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        email = d.pop("email")

        job_title = d.pop("job_title")

        role = UserRole(d.pop("role"))

        password = d.pop("password")

        avatar = d.pop("avatar", UNSET)

        register_user_in = cls(
            name=name,
            email=email,
            job_title=job_title,
            role=role,
            password=password,
            avatar=avatar,
        )

        register_user_in.additional_properties = d
        return register_user_in

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
