from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.basic_object_info import BasicObjectInfo


T = TypeVar("T", bound="DatasetBasicInformation")


@attr.s(auto_attribs=True)
class DatasetBasicInformation:
    """
    Attributes:
        dataset (BasicObjectInfo):
        version (BasicObjectInfo):
        data_owner (BasicObjectInfo):
    """

    dataset: "BasicObjectInfo"
    version: "BasicObjectInfo"
    data_owner: "BasicObjectInfo"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dataset = self.dataset.to_dict()

        version = self.version.to_dict()

        data_owner = self.data_owner.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset": dataset,
                "version": version,
                "data_owner": data_owner,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.basic_object_info import BasicObjectInfo

        d = src_dict.copy()
        dataset = BasicObjectInfo.from_dict(d.pop("dataset"))

        version = BasicObjectInfo.from_dict(d.pop("version"))

        data_owner = BasicObjectInfo.from_dict(d.pop("data_owner"))

        dataset_basic_information = cls(
            dataset=dataset,
            version=version,
            data_owner=data_owner,
        )

        dataset_basic_information.additional_properties = d
        return dataset_basic_information

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
