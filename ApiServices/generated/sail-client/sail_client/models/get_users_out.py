from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

from ..models.user_role import UserRole

if TYPE_CHECKING:
    from ..models.basic_object_info import BasicObjectInfo


T = TypeVar("T", bound="GetUsersOut")


@attr.s(auto_attribs=True)
class GetUsersOut:
    """
    Attributes:
        name (str):
        email (str):
        job_title (str):
        role (UserRole): An enumeration.
        avatar (str):
        id (str):
        organization (BasicObjectInfo):
    """

    name: str
    email: str
    job_title: str
    role: UserRole
    avatar: str
    id: str
    organization: "BasicObjectInfo"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        email = self.email
        job_title = self.job_title
        role = self.role.value

        avatar = self.avatar
        id = self.id
        organization = self.organization.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "email": email,
                "job_title": job_title,
                "role": role,
                "avatar": avatar,
                "id": id,
                "organization": organization,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.basic_object_info import BasicObjectInfo

        d = src_dict.copy()
        name = d.pop("name")

        email = d.pop("email")

        job_title = d.pop("job_title")

        role = UserRole(d.pop("role"))

        avatar = d.pop("avatar")

        id = d.pop("id")

        organization = BasicObjectInfo.from_dict(d.pop("organization"))

        get_users_out = cls(
            name=name,
            email=email,
            job_title=job_title,
            role=role,
            avatar=avatar,
            id=id,
            organization=organization,
        )

        get_users_out.additional_properties = d
        return get_users_out

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