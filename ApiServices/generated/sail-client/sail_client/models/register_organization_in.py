from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisterOrganizationIn")


@attr.s(auto_attribs=True)
class RegisterOrganizationIn:
    """
    Attributes:
        name (str):
        description (str):
        admin_name (str):
        admin_job_title (str):
        admin_email (str):
        admin_password (str):
        avatar (Union[Unset, str]):
        admin_avatar (Union[Unset, str]):
    """

    name: str
    description: str
    admin_name: str
    admin_job_title: str
    admin_email: str
    admin_password: str
    avatar: Union[Unset, str] = UNSET
    admin_avatar: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        admin_name = self.admin_name
        admin_job_title = self.admin_job_title
        admin_email = self.admin_email
        admin_password = self.admin_password
        avatar = self.avatar
        admin_avatar = self.admin_avatar

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "admin_name": admin_name,
                "admin_job_title": admin_job_title,
                "admin_email": admin_email,
                "admin_password": admin_password,
            }
        )
        if avatar is not UNSET:
            field_dict["avatar"] = avatar
        if admin_avatar is not UNSET:
            field_dict["admin_avatar"] = admin_avatar

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        admin_name = d.pop("admin_name")

        admin_job_title = d.pop("admin_job_title")

        admin_email = d.pop("admin_email")

        admin_password = d.pop("admin_password")

        avatar = d.pop("avatar", UNSET)

        admin_avatar = d.pop("admin_avatar", UNSET)

        register_organization_in = cls(
            name=name,
            description=description,
            admin_name=admin_name,
            admin_job_title=admin_job_title,
            admin_email=admin_email,
            admin_password=admin_password,
            avatar=avatar,
            admin_avatar=admin_avatar,
        )

        register_organization_in.additional_properties = d
        return register_organization_in

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
