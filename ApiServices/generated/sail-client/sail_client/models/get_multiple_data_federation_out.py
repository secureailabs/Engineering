from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_data_federation_out import GetDataFederationOut


T = TypeVar("T", bound="GetMultipleDataFederationOut")


@attr.s(auto_attribs=True)
class GetMultipleDataFederationOut:
    """
    Attributes:
        data_federations (Union[Unset, List['GetDataFederationOut']]):
    """

    data_federations: Union[Unset, List["GetDataFederationOut"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_federations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.data_federations, Unset):
            data_federations = []
            for data_federations_item_data in self.data_federations:
                data_federations_item = data_federations_item_data.to_dict()

                data_federations.append(data_federations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_federations is not UNSET:
            field_dict["data_federations"] = data_federations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_data_federation_out import GetDataFederationOut

        d = src_dict.copy()
        data_federations = []
        _data_federations = d.pop("data_federations", UNSET)
        for data_federations_item_data in _data_federations or []:
            data_federations_item = GetDataFederationOut.from_dict(data_federations_item_data)

            data_federations.append(data_federations_item)

        get_multiple_data_federation_out = cls(
            data_federations=data_federations,
        )

        get_multiple_data_federation_out.additional_properties = d
        return get_multiple_data_federation_out

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
