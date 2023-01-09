from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.get_dataset_version_out import GetDatasetVersionOut


T = TypeVar("T", bound="GetMultipleDatasetVersionOut")


@attr.s(auto_attribs=True)
class GetMultipleDatasetVersionOut:
    """
    Attributes:
        dataset_versions (List['GetDatasetVersionOut']):
    """

    dataset_versions: List["GetDatasetVersionOut"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dataset_versions = []
        for dataset_versions_item_data in self.dataset_versions:
            dataset_versions_item = dataset_versions_item_data.to_dict()

            dataset_versions.append(dataset_versions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset_versions": dataset_versions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_dataset_version_out import GetDatasetVersionOut

        d = src_dict.copy()
        dataset_versions = []
        _dataset_versions = d.pop("dataset_versions")
        for dataset_versions_item_data in _dataset_versions:
            dataset_versions_item = GetDatasetVersionOut.from_dict(dataset_versions_item_data)

            dataset_versions.append(dataset_versions_item)

        get_multiple_dataset_version_out = cls(
            dataset_versions=dataset_versions,
        )

        get_multiple_dataset_version_out.additional_properties = d
        return get_multiple_dataset_version_out

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
