from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="GetDatasetVersionConnectionStringOut")


@attr.s(auto_attribs=True)
class GetDatasetVersionConnectionStringOut:
    """
    Attributes:
        id (str):
        connection_string (str):
    """

    id: str
    connection_string: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        connection_string = self.connection_string

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "connection_string": connection_string,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        connection_string = d.pop("connection_string")

        get_dataset_version_connection_string_out = cls(
            id=id,
            connection_string=connection_string,
        )

        get_dataset_version_connection_string_out.additional_properties = d
        return get_dataset_version_connection_string_out

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
