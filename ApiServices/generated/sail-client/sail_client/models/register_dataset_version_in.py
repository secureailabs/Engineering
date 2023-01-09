from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="RegisterDatasetVersionIn")


@attr.s(auto_attribs=True)
class RegisterDatasetVersionIn:
    """
    Attributes:
        dataset_id (str):
        description (str):
        name (str):
    """

    dataset_id: str
    description: str
    name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dataset_id = self.dataset_id
        description = self.description
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset_id": dataset_id,
                "description": description,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dataset_id = d.pop("dataset_id")

        description = d.pop("description")

        name = d.pop("name")

        register_dataset_version_in = cls(
            dataset_id=dataset_id,
            description=description,
            name=name,
        )

        register_dataset_version_in.additional_properties = d
        return register_dataset_version_in

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
