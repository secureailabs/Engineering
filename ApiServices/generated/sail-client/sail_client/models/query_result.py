from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.query_result_data import QueryResultData


T = TypeVar("T", bound="QueryResult")


@attr.s(auto_attribs=True)
class QueryResult:
    """
    Attributes:
        status (str):
        data (QueryResultData):
    """

    status: str
    data: "QueryResultData"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.query_result_data import QueryResultData

        d = src_dict.copy()
        status = d.pop("status")

        data = QueryResultData.from_dict(d.pop("data"))

        query_result = cls(
            status=status,
            data=data,
        )

        query_result.additional_properties = d
        return query_result

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
