from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.get_data_model_out import GetDataModelOut


T = TypeVar("T", bound="GetMultipleDataModelOut")


@attr.s(auto_attribs=True)
class GetMultipleDataModelOut:
    """
    Attributes:
        data_models (List['GetDataModelOut']):
    """

    data_models: List["GetDataModelOut"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_models = []
        for data_models_item_data in self.data_models:
            data_models_item = data_models_item_data.to_dict()

            data_models.append(data_models_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_models": data_models,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_data_model_out import GetDataModelOut

        d = src_dict.copy()
        data_models = []
        _data_models = d.pop("data_models")
        for data_models_item_data in _data_models:
            data_models_item = GetDataModelOut.from_dict(data_models_item_data)

            data_models.append(data_models_item)

        get_multiple_data_model_out = cls(
            data_models=data_models,
        )

        get_multiple_data_model_out.additional_properties = d
        return get_multiple_data_model_out

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
