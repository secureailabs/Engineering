from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.get_data_model_dataframe_out import GetDataModelDataframeOut


T = TypeVar("T", bound="GetMultipleDataModelDataframeOut")


@attr.s(auto_attribs=True)
class GetMultipleDataModelDataframeOut:
    """
    Attributes:
        data_model_dataframes (List['GetDataModelDataframeOut']):
    """

    data_model_dataframes: List["GetDataModelDataframeOut"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_model_dataframes = []
        for data_model_dataframes_item_data in self.data_model_dataframes:
            data_model_dataframes_item = data_model_dataframes_item_data.to_dict()

            data_model_dataframes.append(data_model_dataframes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_model_dataframes": data_model_dataframes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_data_model_dataframe_out import GetDataModelDataframeOut

        d = src_dict.copy()
        data_model_dataframes = []
        _data_model_dataframes = d.pop("data_model_dataframes")
        for data_model_dataframes_item_data in _data_model_dataframes:
            data_model_dataframes_item = GetDataModelDataframeOut.from_dict(data_model_dataframes_item_data)

            data_model_dataframes.append(data_model_dataframes_item)

        get_multiple_data_model_dataframe_out = cls(
            data_model_dataframes=data_model_dataframes,
        )

        get_multiple_data_model_dataframe_out.additional_properties = d
        return get_multiple_data_model_dataframe_out

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
