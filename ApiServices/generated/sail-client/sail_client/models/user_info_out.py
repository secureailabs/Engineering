from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.user_role import UserRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.basic_object_info import BasicObjectInfo


T = TypeVar("T", bound="UserInfoOut")


@attr.s(auto_attribs=True)
class UserInfoOut:
    """
    Attributes:
        name (str):
        email (str):
        job_title (str):
        role (UserRole): An enumeration.
        id (str):
        organization (BasicObjectInfo):
        avatar (Union[Unset, str]):
    """

    name: str
    email: str
    job_title: str
    role: UserRole
    id: str
    organization: "BasicObjectInfo"
    avatar: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        email = self.email
        job_title = self.job_title
        role = self.role.value

        id = self.id
        organization = self.organization.to_dict()

        avatar = self.avatar

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "email": email,
                "job_title": job_title,
                "role": role,
                "id": id,
                "organization": organization,
            }
        )
        if avatar is not UNSET:
            field_dict["avatar"] = avatar

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.basic_object_info import BasicObjectInfo

        d = src_dict.copy()
        name = d.pop("name")

        email = d.pop("email")

        job_title = d.pop("job_title")

        role = UserRole(d.pop("role"))

        id = d.pop("id")

        organization = BasicObjectInfo.from_dict(d.pop("organization"))

        avatar = d.pop("avatar", UNSET)

        user_info_out = cls(
            name=name,
            email=email,
            job_title=job_title,
            role=role,
            id=id,
            organization=organization,
            avatar=avatar,
        )

        user_info_out.additional_properties = d
        return user_info_out

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
