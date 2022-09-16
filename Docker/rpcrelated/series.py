from typing import Any, Callable, Dict, Hashable, List, Literal, Optional, Type, Union

import numpy as np
import pandas as pd
from pandas._libs.lib import no_default

from custom_typing import ArrayLike, Axis, Frequency, IndexLabel, Level, Scalar
from zero import ProxyObject, SecretObject


class RemoteSeries:
    def __init__(
        self,
        d=None,
        ind=None,
        typ=None,
        na=None,
    ):
        if d is None or isinstance(d, pd.Series):
            self.series = d
        else:
            self.series = pd.Series(data=d, index=ind, dtype=typ, name=na)
        if self.series is not None:
            self.index = self.series.index
            self.values = ProxyObject(self.series.values)
            self.dtypes = self.series.dtypes
            self.shape = self.series.shape
            self.nbytes = self.series.nbytes
            self.ndim = self.series.ndim
            self.size = self.series.size
            self.hasnans = self.series.hasnans
            self.empty = self.series.empty
            self.name = self.series.name

    @property
    def at(self):
        return ProxyObject(self.frame.at)

    @property
    def iat(self):
        return ProxyObject(self.frame.iat)

    @property
    def loc(self):
        return ProxyObject(self.frame.loc)

    @property
    def iloc(self):
        return ProxyObject(self.frame.iloc)

    def ravel(
        self,
        order: str = "C",
    ) -> Type[ProxyObject]:
        ans = self.series.ravel(order)
        return ProxyObject(ans)

    def repeat(
        self,
        repeats: Union[int, List[int]],
        axis=None,
    ) -> Type[ProxyObject]:
        ans = self.series.repeat(repeats, axis)
        return ProxyObject(ans)

    def reset_index(
        self,
        level: Optional[Union[int, str, tuple, list]] = None,
        drop: bool = False,
        name: Optional[str] = no_default,
        inplace: bool = False,
    ) -> Type[ProxyObject]:
        ans = self.series.reset_index(level, drop, name, inplace)
        return ProxyObject(ans)

    # def items(self) -> 'Iterable[tuple[Hashable, Any]]':
    #     ans = self.series.items()

    # def iteritems(self) -> 'Iterable[tuple[Hashable, Any]]':
    #     ans = self.series.iteritems()

    def keys(self) -> ArrayLike:
        ans = self.series.keys()
        return ans

    def to_dict(
        self,
        into=dict,
    ) -> dict:
        ans = self.series.to_dict(into)
        return ProxyObject(ans)

    def to_series(
        self,
        name: "Hashable" = no_default,
    ) -> Type[ProxyObject]:
        ans = self.series.to_series(name)
        return ProxyObject(ans)

    # ?
    def groupby(
        self,
        by: IndexLabel = None,
        axis: Axis = 0,
        level: Optional[Level] = None,
        as_index: bool = True,
        sort: bool = True,
        group_keys: bool = True,
        squeeze: Optional[bool] = no_default,
        observed: bool = False,
        dropna: bool = True,
    ) -> Type[ProxyObject]:
        ans = self.series.groupby(by, axis, level, as_index, sort, group_keys, squeeze, observed, dropna)
        return ProxyObject(ans)

    def count(
        self,
        level: Optional[Level] = None,
    ) -> Union[int, pd.Series]:
        ans = self.series.count(level)
        return ans

    # ?
    def mode(
        self,
        dropna: "bool" = True,
    ) -> pd.Series:
        ans = self.series.mode(dropna)
        return ans

    def unique(
        self,
    ) -> "ArrayLike":
        ans = self.series.unique()
        return ans

    def drop_duplicates(
        self,
        keep: str = "first",
        inplace: bool = False,
    ) -> Type[ProxyObject]:
        ans = self.series.drop_duplicates(keep, inplace)
        return ProxyObject(ans)

    def duplicated(
        self,
        keep: str = "first",
    ) -> Type[ProxyObject]:
        ans = self.series.duplicated(keep)
        return ProxyObject(ans)

    def idxmin(
        self,
        axis: Axis = 0,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> IndexLabel:
        ans = self.series.idxmin(axis, skipna, *args, **kwargs)
        return ans

    def idxmax(
        self,
        axis: Axis = 0,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> IndexLabel:
        ans = self.series.idxmax(axis, skipna, *args, **kwargs)
        return ans

    def round(
        self,
        decimals=0,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.round(decimals, *args, **kwargs)
        return ProxyObject[ans]

    def quantile(
        self,
        q: float = 0.5,
        interpolation: str = "linear",
    ) -> Union[float, pd.Series]:
        ans = self.series.quantile(q, interpolation)
        return ans

    def corr(
        self,
        other: pd.Series,
        method: str = "pearson",
        min_periods: Optional[int] = None,
    ) -> "float":
        ans = self.series.corr(other, method, min_periods)
        return ans

    def cov(self, other: pd.Series, min_periods: "int | None" = None, ddof: "int | None" = 1) -> "float":
        ans = self.series.cov(other, min_periods, ddof)
        return ans

    def diff(self, periods: "int" = 1) -> Type[ProxyObject]:
        ans = self.series.diff(periods)
        return ProxyObject(ans)

    def autocorr(
        self,
        lag: int = 1,
    ) -> "float":
        ans = self.series.autocorr(lag)
        return ans

    def dot(
        self,
        other: ArrayLike,
    ) -> Type[ProxyObject]:
        ans = self.series.dot(other)
        return ProxyObject(ans)

    # ?
    def searchsorted(
        self,
        value: Union[ArrayLike, Scalar],
        side: Literal["left", "right"] = "left",
        sorter: Optional[ArrayLike] = None,
    ) -> Union[int, List[int]]:
        ans = self.series.searchsorted(value, side, sorter)
        return ans

    def compare(
        self,
        other: pd.Series,
        align_axis: "Axis" = 1,
        keep_shape: "bool" = False,
        keep_equal: "bool" = False,
    ) -> Type[ProxyObject]:
        ans = self.series.compare(other, align_axis, keep_shape, keep_equal)
        return ProxyObject(ans)

    def combine(
        self,
        other: Union[Scalar, pd.Series],
        func: Callable,
        fill_value: Optional[Scalar] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.combine(other, func, fill_value)
        return ProxyObject(ans)

    def combine_first(
        self,
        other: pd.Series,
    ) -> Type[ProxyObject]:
        ans = self.series.combine_first(other)
        return ProxyObject(ans)

    def update(
        self,
        other: pd.Series,
    ) -> "None":
        ans = self.series.update(other)

    def sort_values(
        self,
        axis: Axis = 0,
        ascending: Union[bool, int] = True,
        inplace: bool = False,
        kind: str = "quicksort",
        na_position: str = "last",
        ignore_index: bool = False,
        key: Optional[Callable] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.sort_values(axis, ascending, inplace, kind, na_position, ignore_index, key)
        return ProxyObject(ans)

    def sort_index(
        self,
        axis: Axis = 0,
        ascending: Union[bool, int] = True,
        inplace: bool = False,
        kind: str = "quicksort",
        na_position: str = "last",
        ignore_index: bool = False,
        key: Optional[Callable] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.sort_index(
            axis, level, ascending, inplace, kind, na_position, sort_remaining, ignore_index, key
        )
        return ProxyObject(ans)

    def argsort(
        self,
        axis: Axis = 0,
        kind: str = "quicksort",
        order: None = None,
    ) -> Type[ProxyObject]:
        ans = self.series.argsort(axis, kind, order)
        return ProxyObject(ans)

    def nlargest(
        self,
        n: int = 5,
        keep: str = "first",
    ) -> Type[ProxyObject]:
        ans = self.series.nlargest(n, keep)
        return ProxyObject(ans)

    def nsmallest(
        self,
        n: "int" = 5,
        keep: "str" = "first",
    ) -> Type[ProxyObject]:
        ans = self.series.nsmallest(n, keep)
        return ProxyObject(ans)

    def swaplevel(
        self,
        i: int = -2,
        j: int = -1,
        copy: bool = True,
    ) -> Type[ProxyObject]:
        ans = self.series.swaplevel(i, j, copy)
        return ProxyObject(ans)

    def reorder_levels(
        self,
        order: List[int],
    ) -> Type[ProxyObject]:
        ans = self.series.reorder_levels(order)
        return ProxyObject(ans)

    def explode(
        self,
        ignore_index: "bool" = False,
    ) -> Type[ProxyObject]:
        ans = self.series.explode(ignore_index)
        return ProxyObject(ans)

    def unstack(
        self,
        level: int = -1,
        fill_value: Optional[Scalar] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.unstack(level, fill_value)
        return ProxyObject(ans)

    def map(
        self,
        arg: Callable,
        na_action: Optional[str] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.map(arg, na_action)
        return ProxyObject(ans)

    def aggregate(
        self,
        func: Callable = None,
        axis: Axis = 0,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.aggregate(func, axis, *args, **kwargs)
        return ProxyObject(ans)

    def transform(
        self,
        func: Callable,
        axis: "Axis" = 0,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.transform(func, axis, *args, **kwargs)
        return ProxyObject(ans)

    def apply(
        self,
        func: Callable,
        convert_dtype: "bool" = True,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.apply(func, convert_dtype, *args, **kwargs)
        return ProxyObject(ans)

    def align(
        self,
        other: Union[pd.DataFrame, pd.Series],
        join: str = "outer",
        axis: Union[Axis, None] = None,
        level: Union[Level, None] = None,
        copy: bool = True,
        fill_value=None,
        method: Union[str, None] = None,
        limit=None,
        fill_axis: Axis = 0,
        broadcast_axis: Union[Axis, None] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.align(other, join, axis, level, copy, fill_value, method, limit, fill_axis, broadcast_axis)
        return ProxyObject(ans)

    def rename(
        self,
        index: Union[Scalar, Hashable, dict, Callable] = None,
        *,
        axis: Optional[Axis] = None,
        copy: bool = True,
        inplace: bool = False,
        level: Optional[Level] = None,
        errors: str = "ignore",
    ) -> Type[ProxyObject]:
        ans = self.series.rename(index, axis, copy, inplace, level, errors)
        return ProxyObject(ans)

    def set_axis(
        self,
        labels: IndexLabel,
        axis: "Axis" = 0,
        inplace: "bool" = False,
    ) -> Type[ProxyObject]:
        ans = self.series.set_axis(labels, axis, inplace)
        return ProxyObject(ans)

    def reindex(
        self,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.reindex(args, **kwargs)
        return ProxyObject(ans)

    def drop(
        self,
        labels: Optional[IndexLabel] = None,
        axis: Axis = 0,
        index: Optional[IndexLabel] = None,
        columns: Optional[IndexLabel] = None,
        level: Optional[Level] = None,
        inplace: bool = False,
        errors: str = "raise",
    ) -> Type[ProxyObject]:
        ans = self.series.drop(labels, axis, index, columns, level, inplace, errors)
        return ProxyObject(ans)

    def fillna(
        self,
        value: Optional[Union[Scalar, ArrayLike]] = None,
        method: Optional[str] = None,
        axis: Axis = None,
        inplace: bool = False,
        limit: Optional[int] = None,
        downcast: Optional[dict] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.fillna(value, method, axis, inplace, limit, downcast)
        return ProxyObject(ans)

    def pop(
        self,
        item: "Hashable",
    ) -> Type[ProxyObject]:
        ans = self.series.pop(item)
        return ProxyObject(ans)

    def replace(
        self,
        to_replace: Optional[Union[Scalar, pd.Series]] = None,
        value: Optional[Union[Scalar, list, dict]] = no_default,
        inplace: Optional[bool] = False,
        limit: Optional[int] = None,
        regex: bool = False,
        method: Optional[str] = no_default,
    ) -> Type[ProxyObject]:
        ans = self.series.replace(to_replace, value, inplace, limit, regex, method)
        return ProxyObject(ans)

    def shift(
        self,
        periods: int = 1,
        freq: Optional[Frequency] = None,
        axis: Axis = 0,
        fill_value: Optional[Scalar] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.shift(periods, freq, axis, fill_value)
        return ProxyObject(ans)

    def memory_usage(
        self,
        index: "bool" = True,
        deep: "bool" = False,
    ) -> "int":
        ans = self.series.memory_usage(index, deep)
        return ans

    def isin(
        self,
        values: Union[set, list],
    ) -> Type[ProxyObject]:
        ans = self.series.isin(values)
        return ProxyObject(ans)

    def between(
        self,
        left: Union[Scalar, list],
        right: Union[Scalar, list],
        inclusive: str = "both",
    ) -> Type[ProxyObject]:
        ans = self.series.between(left, right, inclusive)
        return ProxyObject(ans)

    def isna(
        self,
    ) -> Type[ProxyObject]:
        ans = self.series.isna()
        return ProxyObject(ans)

    def isnull(
        self,
    ) -> Type[ProxyObject]:
        ans = self.series.isnull()
        return ProxyObject(ans)

    def notna(
        self,
    ) -> Type[ProxyObject]:
        ans = self.series.notna()
        return ProxyObject(ans)

    def notnull(
        self,
    ) -> Type[ProxyObject]:
        ans = self.series.notnull()
        return ProxyObject(ans)

    def dropna(
        self,
        axis: Axis = 0,
        inplace: bool = False,
        how: Optional[str] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.dropna(axis, inplace, how)
        return ProxyObject(ans)

    def asfreq(
        self,
        freq: Frequency,
        method: Optional[str] = None,
        how: "str | None" = None,
        normalize: "bool" = False,
        fill_value: Scalar = None,
    ) -> Type[ProxyObject]:
        ans = self.series.asfreq(freq, method, how, normalize, fill_value)
        return ProxyObject(ans)

    # ? todo
    def resample(
        self,
        rule,
        axis=0,
        closed: "str | None" = None,
        label: "str | None" = None,
        convention: "str" = "start",
        kind: "str | None" = None,
        loffset=None,
        base: "int | None" = None,
        on=None,
        level=None,
        origin: "str | TimestampConvertibleTypes" = "start_day",
        offset: "TimedeltaConvertibleTypes | None" = None,
    ) -> "Resampler":
        ans = self.series.resample(
            rule, axis, closed, label, convention, kind, loffset, base, on, level, origin, offset
        )
        return ProxyObject(ans)

    def to_timestamp(
        self,
        freq: Optional[Frequency] = None,
        how: str = "start",
        copy: bool = True,
    ) -> Type[ProxyObject]:
        ans = self.series.to_timestamp(freq, how, copy)
        return ProxyObject(ans)

    def to_period(
        self,
        freq: Optional[Frequency] = None,
        copy: bool = True,
    ) -> Type[ProxyObject]:
        ans = self.series.to_period(freq, copy)
        return ProxyObject(ans)

    def ffill(
        self,
        axis: "None | Axis" = None,
        inplace: "bool" = False,
        limit: "None | int" = None,
        downcast: Optional[dict] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.ffill(axis, inplace, limit, downcast)
        return ProxyObject(ans)

    def bfill(
        self,
        axis: "None | Axis" = None,
        inplace: "bool" = False,
        limit: "None | int" = None,
        downcast: Optional[dict] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.bfill(axis, inplace, limit, downcast)
        return ProxyObject(ans)

    def clip(
        self,
        lower: Optional[Union[float, ArrayLike]] = None,
        upper: Optional[Union[float, ArrayLike]] = None,
        axis: "Axis | None" = None,
        inplace: "bool" = False,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.clip(lower, upper, axis, inplace, *args, **kwargs)
        return ProxyObject(ans)

    def interpolate(
        self,
        method: "str" = "linear",
        axis: "Axis" = 0,
        limit: "int | None" = None,
        inplace: "bool" = False,
        limit_direction: "str | None" = None,
        limit_area: "str | None" = None,
        downcast: "str | None" = None,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.interpolate(method, axis, limit, inplace, limit_direction, limit_area, downcast, **kwargs)
        return ProxyObject(ans)

    def where(
        self,
        cond: Union[bool, ArrayLike, Callable],
        other: Union[ArrayLike, Callable] = no_default,
        inplace: bool = False,
        axis: Optional[int] = None,
        level: Optional[int] = None,
        errors: str = "raise",
        try_cast: Optional[bool] = no_default,
    ) -> Type[ProxyObject]:
        ans = self.series.where(cond, other, inplace, axis, level, errors, try_cast)
        return ProxyObject(ans)

    def mask(
        self,
        cond: Union[bool, ArrayLike, Callable],
        other: Union[ArrayLike, Callable] = no_default,
        inplace: bool = False,
        axis: Optional[int] = None,
        level: Optional[int] = None,
        errors: str = "raise",
        try_cast: Optional[bool] = no_default,
    ) -> Type[ProxyObject]:
        ans = self.series.mask(cond, other, inplace, axis, level, errors, try_cast)
        return ProxyObject(ans)

    def any(
        self,
        axis: Axis = 0,
        bool_only: Optional[bool] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.any(axis, bool_only, skipna, level, **kwargs)
        return ans

    def all(
        self,
        axis: Axis = 0,
        bool_only: Optional[bool] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.all(axis, bool_only, skipna, level, **kwargs)
        return ans

    def mad(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.mad(axis, skipna, level)
        return ans

    def sem(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        ddof: int = 1,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.sem(axis, skipna, level, ddof, numeric_only, **kwargs)
        return ans

    def var(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        ddof: int = 1,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.var(axis, skipna, level, ddof, numeric_only, **kwargs)
        return ans

    def std(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        ddof: int = 1,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.std(axis, skipna, level, ddof, numeric_only, **kwargs)
        return ans

    def cummin(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.cummin(axis, skipna, *args, **kwargs)
        return ans

    def cummax(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.cummax(axis, skipna, *args, **kwargs)
        return ans

    def cumsum(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.cumsum(axis, skipna, *args, **kwargs)
        return ans

    def cumprod(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.cumprod(axis, skipna, *args, **kwargs)
        return ans

    def sum(
        self,
        axis: Axis = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        min_count: int = 0,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.sum(axis, skipna, level, numeric_only, min_count, **kwargs)
        return ans

    def prod(
        self,
        axis: Axis = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        min_count: int = 0,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.prod(axis, skipna, level, numeric_only, min_count, **kwargs)
        return ans

    def prod(
        self,
        axis: Axis = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        min_count: int = 0,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.prod(axis, skipna, level, numeric_only, min_count, **kwargs)
        return ans

    def mean(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.mean(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def skew(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.skew(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def kurt(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.kurt(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def median(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.median(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def max(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.max(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def min(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.min(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def add(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.add(other, level, fill_value, axis)
        return ProxyObject(ans)

    def radd(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.radd(other, level, fill_value, axis)
        return ProxyObject(ans)

    def sub(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.sub(other, level, fill_value, axis)
        return ProxyObject(ans)

    def mul(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.mul(other, level, fill_value, axis)
        return ProxyObject(ans)

    def truediv(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.truediv(other, level, fill_value, axis)
        return ProxyObject(ans)

    def floordiv(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.floordiv(other, level, fill_value, axis)
        return ProxyObject(ans)

    def mod(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.mod(other, level, fill_value, axis)
        return ProxyObject(ans)

    def pow(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.pow(other, level, fill_value, axis)
        return ProxyObject(ans)

    def rmul(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rmul(other, level, fill_value, axis)
        return ProxyObject(ans)

    def rsub(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rsub(other, level, fill_value, axis)
        return ProxyObject(ans)

    def rtruediv(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rtruediv(other, level, fill_value, axis)
        return ProxyObject(ans)

    def rfloordiv(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rfloordiv(other, level, fill_value, axis)
        return ProxyObject(ans)

    def rpow(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rpow(other, level, fill_value, axis)
        return ProxyObject(ans)

    def rmod(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rmod(other, level, fill_value, axis)
        return ProxyObject(ans)

    def truediv(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.truediv(other, level, fill_value, axis)
        return ProxyObject(ans)

    def rtruediv(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rtruediv(other, level, fill_value, axis)
        return ProxyObject(ans)

    def divmod(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.divmod(other, level, fill_value, axis)
        return ProxyObject(ans)

    def rdivmod(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rdivmod(other, level, fill_value, axis)
        return ProxyObject(ans)

    def eq(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.eq(other, level, fill_value, axis)
        return ProxyObject(ans)

    def ne(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.ne(other, level, fill_value, axis)
        return ProxyObject(ans)

    def lt(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.lt(other, level, fill_value, axis)
        return ProxyObject(ans)

    def gt(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.gt(other, level, fill_value, axis)
        return ProxyObject(ans)

    def le(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.le(other, level, fill_value, axis)
        return ProxyObject(ans)

    def ge(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.ge(other, level, fill_value, axis)
        return ProxyObject(ans)

    def mul(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.mul(other, level, fill_value, axis)
        return ProxyObject(ans)

    def sub(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.sub(other, level, fill_value, axis)
        return ProxyObject(ans)

    def truediv(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.truediv(other, level, fill_value, axis)
        return ProxyObject(ans)
