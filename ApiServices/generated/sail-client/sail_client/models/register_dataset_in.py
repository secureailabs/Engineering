from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.dataset_format import DatasetFormat

T = TypeVar("T", bound="RegisterDatasetIn")


@attr.s(auto_attribs=True)
class RegisterDatasetIn:
    """
    Attributes:
        name (str):
        description (str):
        tags (str):
        format_ (DatasetFormat): An enumeration.
    """

    name: str
    description: str
    tags: str
    format_: DatasetFormat
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        tags = self.tags
        format_ = self.format_.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "tags": tags,
                "format": format_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        tags = d.pop("tags")

        format_ = DatasetFormat(d.pop("format"))

        register_dataset_in = cls(
            name=name,
            description=description,
            tags=tags,
            format_=format_,
        )

        register_dataset_in.additional_properties = d
        return register_dataset_in

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
