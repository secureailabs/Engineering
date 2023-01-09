from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DatasetEncryptionKeyOut")


@attr.s(auto_attribs=True)
class DatasetEncryptionKeyOut:
    """
    Attributes:
        dataset_key (str):
    """

    dataset_key: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dataset_key = self.dataset_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset_key": dataset_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dataset_key = d.pop("dataset_key")

        dataset_encryption_key_out = cls(
            dataset_key=dataset_key,
        )

        dataset_encryption_key_out.additional_properties = d
        return dataset_encryption_key_out

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
