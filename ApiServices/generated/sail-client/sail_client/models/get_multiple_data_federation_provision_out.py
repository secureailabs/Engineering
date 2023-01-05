from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.get_data_federation_provision import GetDataFederationProvision


T = TypeVar("T", bound="GetMultipleDataFederationProvisionOut")


@attr.s(auto_attribs=True)
class GetMultipleDataFederationProvisionOut:
    """
    Attributes:
        data_federation_provisions (List['GetDataFederationProvision']):
    """

    data_federation_provisions: List["GetDataFederationProvision"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_federation_provisions = []
        for data_federation_provisions_item_data in self.data_federation_provisions:
            data_federation_provisions_item = data_federation_provisions_item_data.to_dict()

            data_federation_provisions.append(data_federation_provisions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_federation_provisions": data_federation_provisions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_data_federation_provision import GetDataFederationProvision

        d = src_dict.copy()
        data_federation_provisions = []
        _data_federation_provisions = d.pop("data_federation_provisions")
        for data_federation_provisions_item_data in _data_federation_provisions:
            data_federation_provisions_item = GetDataFederationProvision.from_dict(data_federation_provisions_item_data)

            data_federation_provisions.append(data_federation_provisions_item)

        get_multiple_data_federation_provision_out = cls(
            data_federation_provisions=data_federation_provisions,
        )

        get_multiple_data_federation_provision_out.additional_properties = d
        return get_multiple_data_federation_provision_out

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
