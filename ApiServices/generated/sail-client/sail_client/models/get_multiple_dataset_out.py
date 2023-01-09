from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_dataset_out import GetDatasetOut


T = TypeVar("T", bound="GetMultipleDatasetOut")


@attr.s(auto_attribs=True)
class GetMultipleDatasetOut:
    """
    Attributes:
        datasets (Union[Unset, List['GetDatasetOut']]):
    """

    datasets: Union[Unset, List["GetDatasetOut"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datasets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.datasets, Unset):
            datasets = []
            for datasets_item_data in self.datasets:
                datasets_item = datasets_item_data.to_dict()

                datasets.append(datasets_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if datasets is not UNSET:
            field_dict["datasets"] = datasets

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_dataset_out import GetDatasetOut

        d = src_dict.copy()
        datasets = []
        _datasets = d.pop("datasets", UNSET)
        for datasets_item_data in _datasets or []:
            datasets_item = GetDatasetOut.from_dict(datasets_item_data)

            datasets.append(datasets_item)

        get_multiple_dataset_out = cls(
            datasets=datasets,
        )

        get_multiple_dataset_out.additional_properties = d
        return get_multiple_dataset_out

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
