import pandas as pd
import numpy as np
from zero import SecretObject, ProxyObject
from custom_typing import ArrayLike, Scalar, Axis, Level, IndexLabel, Renamer, Frequency, Suffixes
import numpy.typing as npt
from pandas._libs.lib import no_default
from typing import Union, List, Hashable, Type, Optional, Any, Literal, Callable, Dict


class RemoteDataFrame:
    def __init__(
        self,
        d=None,
        ind=None,
        cols=None,
        type=None,
    ):
        if d is None or isinstance(d, pd.DataFrame):
            self.frame = d
        else:
            self.frame = pd.DataFrame(data=d, index=ind, columns=cols, dtype=type)
        if self.frame is not None:
            self.index = self.frame.index
            self.dtyps = self.frame.dtypes
            self.info = self.frame.info
            self.values = SecretObject(self.frame.values)
            self.axes = self.frame.axes
            self.ndim = self.frame.ndim
            self.size = self.frame.size
            self.shape = self.frame.shape
            self.empty = self.frame.empty

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

    # def to_string(self, buf: 'FilePath | WriteBuffer[str] | None' = None, columns: 'Sequence[str] | None' = None, col_space: 'int | list[int] | dict[Hashable, int] | None' = None, header: 'bool | Sequence[str]' = True, index: 'bool' = True, na_rep: 'str' = 'NaN', formatters: 'fmt.FormattersType | None' = None, float_format: 'fmt.FloatFormatType | None' = None, sparsify: 'bool | None' = None, index_names: 'bool' = True, justify: 'str | None' = None, max_rows: 'int | None' = None, max_cols: 'int | None' = None, show_dimensions: 'bool' = False, decimal: 'str' = '.', line_width: 'int | None' = None, min_rows: 'int | None' = None, max_colwidth: 'int | None' = None, encoding: 'str | None' = None,) -> 'str | None':
    #     ans = self.frame.to_string(buf, columns, col_space, header, index, na_rep, formatters, float_format, sparsify, index_names, justify, max_rows, max_cols, show_dimensions, decimal, line_width, min_rows, max_colwidth, encoding)

    # def items(self,) -> 'Iterable[tuple[Hashable, Series]]':
    #     ans = self.frame.items()

    # def iteritems(self,) -> 'Iterable[tuple[Hashable, Series]]':
    #     ans = self.frame.iteritems()

    # def iterrows(self,) -> 'Iterable[tuple[Hashable, Series]]':
    #     ans = self.frame.iterrows()

    # def itertuples(self, index: 'bool' = True, name: 'str | None' = 'Pandas',) -> 'Iterable[tuple[Any, ...]]':
    #     ans = self.frame.itertuples(index, name)

    def dot(
        self,
        other: ArrayLike,
    ) -> Type[ProxyObject]:
        ans = self.frame.dot(other)
        return ProxyObject(ans)

    def to_numpy(
        self,
        dtype: Union[npt.DTypeLike, None] = None,
        copy: bool = False,
        na_value=no_default,
    ) -> Type[ProxyObject]:
        ans = self.frame.to_numpy(dtype, copy, na_value)
        return ProxyObject(ans)

    # type of into
    def to_dict(
        self,
        orient: str = "dict",
        into=dict,
    ) -> Type[ProxyObject]:
        ans = self.frame.to_dict(orient, into)
        return ProxyObject(ans)

    def memory_usage(
        self,
        index: bool = True,
        deep: bool = False,
    ) -> pd.Series:
        ans = self.frame.memory_usage(index, deep)
        return ans

    def transpose(
        self,
    ) -> Type[ProxyObject]:
        ans = self.frame.transpose()
        return ProxyObject(ans)

    def query(
        self,
        expr: str,
        inplace: bool = False,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.frame.query(expr, inplace, **kwargs)
        return ProxyObject(ans)

    def eval(
        self,
        expr: str,
        inplace: bool = False,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.frame.eval(expr, inplace, **kwargs)
        return ProxyObject(ans)

    def select_dtypes(
        self,
        include: List[str] = None,
        exclude: List[str] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.select_dtypes(include, exclude)
        return ProxyObject(ans)

    def insert(
        self,
        loc: int,
        column: Hashable,
        value: Union[Scalar, ArrayLike],
        allow_duplicates: bool = False,
    ) -> None:
        self.frame.insert(loc, column, value, allow_duplicates)

    def assign(
        self,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.frame.assign(kwargs)
        return ProxyObject(ans)

    # def lookup(self, row_labels: 'Sequence[IndexLabel]', col_labels: 'Sequence[IndexLabel]',) -> 'np.ndarray':
    #     ans = self.frame.lookup(row_labels, col_labels)

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
        ans = self.frame.align(other, join, axis, level, copy, fill_value, method, limit, fill_axis, broadcast_axis)
        return ProxyObject(ans)

    def set_axis(
        self,
        labels: List,
        axis: Axis = 0,
        inplace: bool = False,
    ) -> Type[ProxyObject]:
        ans = self.frame.set_axis(labels, axis, inplace)
        return ProxyObject(ans)

    def reindex(
        self,
        labels: Optional[IndexLabel] = None,
        index: Optional[IndexLabel] = None,
        columns: Optional[IndexLabel] = None,
        axis: Optional[Axis] = None,
        method: Union[str, None] = None,
        copy: bool = True,
        level: Level = None,
        fill_value: Union[Scalar, float] = np.nan,
        limit: int = None,
        tolerance: Optional[Scalar] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.reindex(labels, index, columns, axis, method, copy, level, fill_value, limit, tolerance)
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
        ans = self.frame.drop(labels, axis, index, columns, level, inplace, errors)
        return ProxyObject(ans)

    # ? var args
    def rename(
        self,
        mapper: Optional[Renamer] = None,
        *,
        index: Optional[Renamer] = None,
        columns: Optional[Renamer] = None,
        axis: Optional[Axis] = None,
        copy: bool = True,
        inplace: bool = False,
        level: Optional[Level] = None,
        errors: str = "ignore",
    ) -> Type[ProxyObject]:
        ans = self.frame.rename(mapper, index, columns, axis, copy, inplace, level, errors)
        return ProxyObject(ans)

    def fillna(
        self,
        value: Optional[Any] = None,
        method: Optional[str] = None,
        axis: Optional[Axis] = None,
        inplace: bool = False,
        limit: Optional[int] = None,
        downcast: Optional[dict] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.fillna(value, method, axis, inplace, limit, downcast)
        return ProxyObject(ans)

    def pop(
        self,
        item: Hashable,
    ) -> Type[ProxyObject]:
        ans = self.frame.pop(item)
        return ProxyObject(ans)

    def replace(
        self,
        to_replace: Union[str, list, dict, pd.Series, int, float] = None,
        value: Union[Scalar, dict, list, str] = no_default,
        inplace: bool = False,
        limit: Optional[int] = None,
        regex: bool = False,
        method: Optional[str] = no_default,
    ) -> Type[ProxyObject]:
        ans = self.frame.replace(to_replace, value, inplace, limit, regex, method)
        return ProxyObject(ans)

    def shift(
        self,
        periods: int = 1,
        freq: Optional[Frequency] = None,
        axis: Axis = 0,
        fill_value: Scalar = no_default,
    ) -> Type[ProxyObject]:
        ans = self.frame.shift(periods, freq, axis, fill_value)
        return ProxyObject(ans)

    def set_index(
        self,
        keys: IndexLabel,
        drop: bool = True,
        append: bool = False,
        inplace: bool = False,
        verify_integrity: bool = False,
    ) -> Type[ProxyObject]:
        ans = self.frame.set_index(keys, drop, append, inplace, verify_integrity)
        return ProxyObject(ans)

    def reset_index(
        self,
        level: Optional[IndexLabel] = None,
        drop: bool = False,
        inplace: bool = False,
        col_level: Hashable = 0,
        col_fill: Hashable = "",
    ) -> Type[ProxyObject]:
        ans = self.frame.reset_index(level, drop, inplace, col_level, col_fill)
        return ProxyObject(ans)

    def isna(
        self,
    ) -> Type[ProxyObject]:
        ans = self.frame.isna()
        return ProxyObject(ans)

    def isnull(
        self,
    ) -> Type[ProxyObject]:
        ans = self.frame.isnull()
        return ProxyObject(ans)

    def notna(
        self,
    ) -> Type[ProxyObject]:
        ans = self.frame.notna()
        return ProxyObject(ans)

    def notnull(
        self,
    ) -> Type[ProxyObject]:
        ans = self.frame.notnull()
        return ProxyObject(ans)

    def dropna(
        self,
        axis: Axis = 0,
        how: str = "any",
        thresh: Optional[int] = None,
        subset: IndexLabel = None,
        inplace: bool = False,
    ) -> Type[ProxyObject]:
        ans = self.frame.dropna(axis, how, thresh, subset, inplace)
        return ProxyObject(ans)

    def drop_duplicates(
        self,
        subset: Optional[IndexLabel] = None,
        keep: Union[Literal["first"], Literal["last"], Literal[False]] = "first",
        inplace: bool = False,
        ignore_index: bool = False,
    ) -> Type[ProxyObject]:
        ans = self.frame.drop_duplicates(subset, keep, inplace, ignore_index)
        return ProxyObject(ans)

    def duplicated(
        self,
        subset: Optional[IndexLabel] = None,
        keep: Union[Literal["first"], Literal["last"], Literal[False]] = "first",
    ) -> Type[ProxyObject]:
        ans = self.frame.duplicated(subset, keep)
        return ProxyObject(ans)

    def sort_values(
        self,
        by: IndexLabel,
        axis: Axis = 0,
        ascending: bool = True,
        inplace: bool = False,
        kind: str = "quicksort",
        na_position: str = "last",
        ignore_index: bool = False,
        key: Optional[Callable] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.sort_values(by, axis, ascending, inplace, kind, na_position, ignore_index, key)
        return ProxyObject(ans)

    def sort_index(
        self,
        axis: Axis = 0,
        level: Optional[Level] = None,
        ascending: Union[bool, int, List[bool]] = True,
        inplace: bool = False,
        kind: str = "quicksort",
        na_position: str = "last",
        sort_remaining: bool = True,
        ignore_index: bool = False,
        key: Optional[Callable] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.sort_index(
            axis, level, ascending, inplace, kind, na_position, sort_remaining, ignore_index, key
        )
        return ProxyObject(ans)

    def value_counts(
        self,
        subset: Optional[List[Hashable]] = None,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        dropna: bool = True,
    ) -> pd.Series:
        ans = self.frame.value_counts(subset, normalize, sort, ascending, dropna)

    def nlargest(
        self,
        n: int,
        columns: IndexLabel,
        keep: str = "first",
    ) -> Type[ProxyObject]:
        ans = self.frame.nlargest(n, columns, keep)
        return ProxyObject(ans)

    def nsmallest(
        self,
        n: int,
        columns: IndexLabel,
        keep: str = "first",
    ) -> Type[ProxyObject]:
        ans = self.frame.nsmallest(n, columns, keep)
        return ProxyObject(ans)

    def swaplevel(
        self,
        i: Axis = -2,
        j: Axis = -1,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.frame.swaplevel(i, j, axis)
        return ProxyObject(ans)

    def reorder_levels(
        self,
        order: List[Axis],
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.frame.reorder_levels(order, axis)
        return ProxyObject(ans)

    def compare(
        self,
        other: pd.DataFrame,
        align_axis: Axis = 1,
        keep_shape: bool = False,
        keep_equal: bool = False,
    ) -> Type[ProxyObject]:
        ans = self.frame.compare(other, align_axis, keep_shape, keep_equal)
        return ProxyObject(ans)

    def combine(
        self,
        other: pd.DataFrame,
        func: Callable,
        fill_value: Scalar = None,
        overwrite: bool = True,
    ) -> Type[ProxyObject]:
        ans = self.frame.combine(other, func, fill_value, overwrite)
        return ProxyObject(ans)

    def combine_first(
        self,
        other: pd.DataFrame,
    ) -> Type[ProxyObject]:
        ans = self.frame.combine_first(other)
        return ProxyObject(ans)

    def update(
        self,
        other: pd.DataFrame,
        join: str = "left",
        overwrite: bool = True,
        filter_func: Optional[Callable] = None,
        errors: str = "ignore",
    ) -> None:
        ans = self.frame.update(other, join, overwrite, filter_func, errors)

    # ? need to implement return class
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
        ans = self.frame.groupby(by, axis, level, as_index, sort, group_keys, squeeze, observed, dropna)
        return ProxyObject(ans)

    def pivot(
        self,
        index: Optional[IndexLabel] = None,
        columns: Optional[IndexLabel] = None,
        values: Optional[IndexLabel] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.pivot(index, columns, values)
        return ProxyObject(ans)

    # def pivot_table(self, values=None, index=None, columns=None, aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All', observed=False, sort=True,) -> 'DataFrame':
    #     ans = self.frame.pivot_table(values, index, columns, aggfunc, fill_value, margins, dropna, margins_name, observed, sort)

    def stack(
        self,
        level: Level = -1,
        dropna: bool = True,
    ) -> Type[ProxyObject]:
        ans = self.frame.stack(level, dropna)
        return ProxyObject(ans)

    def explode(
        self,
        column: "IndexLabel",
        ignore_index: "bool" = False,
    ) -> Type[ProxyObject]:
        ans = self.frame.explode(column, ignore_index)
        return ProxyObject(ans)

    def unstack(self, level: "Level" = -1, fill_value: Union[int, str, dict] = None) -> Type[ProxyObject]:
        ans = self.frame.unstack(level, fill_value)
        return ProxyObject(ans)

    def melt(
        self,
        id_vars: Optional[ArrayLike] = None,
        value_vars: Optional[ArrayLike] = None,
        var_name: Scalar = None,
        value_name: Scalar = "value",
        col_level: Optional[Level] = None,
        ignore_index: "bool" = True,
    ) -> Type[ProxyObject]:
        ans = self.frame.melt(id_vars, value_vars, var_name, value_name, col_level, ignore_index)
        return ProxyObject(ans)

    # ?
    def diff(
        self,
        periods: "int" = 1,
        axis: "Axis" = 0,
    ) -> Type[ProxyObject]:
        ans = self.frame.diff(periods, axis)
        return ProxyObject(ans)

    def aggregate(self, func: Union[Callable, str, dict, list] = None, axis: Axis = 0, *args, **kwargs):
        ans = self.frame.aggregate(func, axis, *args, **kwargs)
        return ProxyObject(ans)

    def transform(
        self,
        func: Union[Callable, str, list, dict],
        axis: "Axis" = 0,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.frame.transform(func, axis, *args, **kwargs)
        return ProxyObject(ans)

    def apply(
        self,
        func: Callable,
        axis: "Axis" = 0,
        raw: "bool" = False,
        result_type: Optional[str] = None,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.frame.apply(func, axis, raw, result_type, args, kwargs)
        return ProxyObject(ans)

    def applymap(
        self,
        func: Callable,
        na_action: Optional[str] = None,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.frame.applymap(func, na_action, kwargs)
        return ProxyObject(ans)

    # def append(
    #     self,
    #     other,
    #     ignore_index: 'bool' = False,
    #     verify_integrity: 'bool' = False,
    #     sort: 'bool' = False,
    # ) -> Type[ProxyObject]:
    #     ans = self.frame.append(other, ignore_index, verify_integrity, sort)
    #     return ProxyObject(ans)

    def join(
        self,
        other: Union[pd.DataFrame, pd.Series],
        on: Optional[IndexLabel] = None,
        how: "str" = "left",
        lsuffix: "str" = "",
        rsuffix: "str" = "",
        sort: "bool" = False,
    ) -> Type[ProxyObject]:
        ans = self.frame.join(other, on, how, lsuffix, rsuffix, sort)
        return ProxyObject(ans)

    def merge(
        self,
        right: Union[pd.DataFrame, pd.Series],
        how: "str" = "inner",
        on: Optional[IndexLabel] = None,
        left_on: Optional[IndexLabel] = None,
        right_on: Optional[IndexLabel] = None,
        left_index: "bool" = False,
        right_index: "bool" = False,
        sort: "bool" = False,
        suffixes: "Suffixes" = ("_x", "_y"),
        copy: "bool" = True,
        indicator: "bool" = False,
        validate: "str | None" = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.merge(
            right, how, on, left_on, right_on, left_index, right_index, sort, suffixes, copy, indicator, validate
        )
        return ProxyObject(ans)

    def round(
        self,
        decimals: Union[int, Dict[IndexLabel, int], pd.Series] = 0,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.frame.round(decimals, *args, **kwargs)
        return ProxyObject(ans)

    # no callable
    def corr(
        self,
        method: str = "pearson",
        min_periods: "int" = 1,
    ) -> pd.DataFrame:
        ans = self.frame.corr(method, min_periods)
        return ans

    def cov(
        self,
        min_periods: Optional[int] = None,
        ddof: Optional[int] = 1,
    ) -> pd.DataFrame:
        ans = self.frame.cov(min_periods, ddof)
        return ans

    def corrwith(
        self,
        other: Union[pd.DataFrame, pd.Series],
        axis: "Axis" = 0,
        drop: bool = False,
        method: str = "pearson",
    ) -> pd.Series:
        ans = self.frame.corrwith(other, axis, drop, method)
        return ans

    def count(
        self,
        axis: "Axis" = 0,
        level: Optional[Union[int, str]] = None,
        numeric_only: "bool" = False,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.count(axis, level, numeric_only)
        return ans

    def nunique(
        self,
        axis: "Axis" = 0,
        dropna: "bool" = True,
    ) -> pd.Series:
        ans = self.frame.nunique(axis, dropna)
        return ans

    def idxmin(
        self,
        axis: "Axis" = 0,
        skipna: "bool" = True,
    ) -> pd.Series:
        ans = self.frame.idxmin(axis, skipna)
        return ans

    def idxmax(
        self,
        axis: "Axis" = 0,
        skipna: "bool" = True,
    ) -> pd.Series:
        ans = self.frame.idxmax(axis, skipna)
        return ans

    # ? safe?
    def mode(
        self,
        axis: "Axis" = 0,
        numeric_only: "bool" = False,
        dropna: "bool" = True,
    ) -> pd.DataFrame:
        ans = self.frame.mode(axis, numeric_only, dropna)
        return ans

    def quantile(
        self,
        q: float = 0.5,
        axis: "Axis" = 0,
        numeric_only: "bool" = True,
        interpolation: "str" = "linear",
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.quantile(q, axis, numeric_only, interpolation)
        return ans

    def asfreq(
        self,
        freq: "Frequency",
        method: Optional[str] = None,
        how: Optional[str] = None,
        normalize: "bool" = False,
        fill_value: Scalar = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.asfreq(freq, method, how, normalize, fill_value)
        return ProxyObject(ans)

    # ?to do
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
        ans = self.frame.resample(rule, axis, closed, label, convention, kind, loffset, base, on, level, origin, offset)

    def to_timestamp(
        self,
        freq: Optional[Frequency],
        how: "str" = "start",
        axis: "Axis" = 0,
        copy: "bool" = True,
    ) -> Type[ProxyObject]:
        ans = self.frame.to_timestamp(freq, how, axis, copy)
        return ProxyObject(ans)

    def to_period(
        self,
        freq: "Frequency | None" = None,
        axis: "Axis" = 0,
        copy: "bool" = True,
    ) -> Type[ProxyObject]:
        ans = self.frame.to_period(freq, axis, copy)
        return ProxyObject(ans)

    def isin(
        self,
        values: Union[dict, pd.DataFrame, pd.Series],
    ) -> Type[ProxyObject]:
        ans = self.frame.isin(values)
        return ProxyObject(ans)

    # def hist_frame(data: 'DataFrame', column: 'IndexLabel' = None, by=None, grid: 'bool' = True, xlabelsize: 'int | None' = None, xrot: 'float | None' = None, ylabelsize: 'int | None' = None, yrot: 'float | None' = None, ax=None, sharex: 'bool' = False, sharey: 'bool' = False, figsize: 'tuple[int, int] | None' = None, layout: 'tuple[int, int] | None' = None, bins: 'int | Sequence[int]' = 10, backend: 'str | None' = None, legend: 'bool' = False, **kwargs):
    #     ans = self.frame.hist_frame(column, by, grid, xlabelsize, xrot, ylabelsize, yrot, ax, sharex, sharey, figsize, layout, bins, backend, legend, kwargs)

    # def boxplot_frame(self, column=None, by=None, ax=None, fontsize=None, rot=0, grid=True, figsize=None, layout=None, return_type=None, backend=None, **kwargs):
    #     ans = self.frame.boxplot_frame(column, by, ax, fontsize, rot, grid, figsize, layout, return_type, backend, kwargs)

    def ffill(
        self: pd.DataFrame,
        axis: Optional[Axis] = None,
        inplace: "bool" = False,
        limit: Optional[int] = None,
        downcast: Optional[str] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.ffill(axis, inplace, limit, downcast)
        return ProxyObject(ans)

    def bfill(
        self: pd.DataFrame,
        axis: "None | Axis" = None,
        inplace: "bool" = False,
        limit: "None | int" = None,
        downcast: Optional[str] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.bfill(axis, inplace, limit, downcast)
        return ProxyObject(ans)

    def clip(
        self: pd.DataFrame,
        lower: Union[float, ArrayLike] = None,
        upper: Union[float, ArrayLike] = None,
        axis: "Axis | None" = None,
        inplace: "bool" = False,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.frame.clip(lower, upper, axis, inplace, *args, **kwargs)
        return ProxyObject(ans)

    def interpolate(
        self: pd.DataFrame,
        method: "str" = "linear",
        axis: "Axis" = 0,
        limit: "int | None" = None,
        inplace: "bool" = False,
        limit_direction: "str | None" = None,
        limit_area: "str | None" = None,
        downcast: "str | None" = None,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.frame.interpolate(method, axis, limit, inplace, limit_direction, limit_area, downcast, kwargs)
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
        ans = self.frame.where(cond, other, inplace, axis, level, errors, try_cast)
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
        ans = self.frame.mask(cond, other, inplace, axis, level, errors, try_cast)
        return ProxyObject(ans)

    def any(
        self,
        axis: Axis = 0,
        bool_only: Optional[bool] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.any(axis, bool_only, skipna, level, **kwargs)
        return ans

    def all(
        self,
        axis: Axis = 0,
        bool_only: Optional[bool] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.all(axis, bool_only, skipna, level, **kwargs)
        return ans

    def mad(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.mad(axis, skipna, level)
        return ans

    def sem(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        ddof: int = 1,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.sem(axis, skipna, level, ddof, numeric_only, **kwargs)
        return ans

    def var(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        ddof: int = 1,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.var(axis, skipna, level, ddof, numeric_only, **kwargs)
        return ans

    def std(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        ddof: int = 1,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.std(axis, skipna, level, ddof, numeric_only, **kwargs)
        return ans

    def cummin(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.cummin(axis, skipna, *args, **kwargs)
        return ans

    def cummax(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.cummax(axis, skipna, *args, **kwargs)
        return ans

    def cumsum(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.cumsum(axis, skipna, *args, **kwargs)
        return ans

    def cumprod(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.cumprod(axis, skipna, *args, **kwargs)
        return ans

    def sum(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        min_count: int = 0,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.sum(axis, skipna, level, numeric_only, min_count, **kwargs)
        return ans

    def prod(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        min_count: int = 0,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.prod(axis, skipna, level, numeric_only, min_count, **kwargs)
        return ans

    def mean(
        self,
        axis: Axis = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.mean(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def skew(
        self,
        axis: Axis = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.skew(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def kurt(
        self,
        axis: Axis = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.kurt(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def median(
        self,
        axis: Axis = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.median(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def max(
        self,
        axis: Axis = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.max(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def min(
        self,
        axis: Axis = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[pd.Series, pd.DataFrame]:
        ans = self.frame.min(axis, skipna, level, numeric_only, **kwargs)
        return ans

    def add(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.add(other, axis, level, fill_value)
        return ProxyObject(ans)

    def radd(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.radd(other, axis, level, fill_value)
        return ProxyObject(ans)

    def sub(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.sub(other, axis, level, fill_value)
        return ProxyObject(ans)

    def mul(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.mul(other, axis, level, fill_value)
        return ProxyObject(ans)

    def truediv(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.truediv(other, axis, level, fill_value)
        return ProxyObject(ans)

    def floordiv(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.floordiv(other, axis, level, fill_value)
        return ProxyObject(ans)

    def mod(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.mod(other, axis, level, fill_value)
        return ProxyObject(ans)

    def pow(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.pow(other, axis, level, fill_value)
        return ProxyObject(ans)

    def rmul(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.rmul(other, axis, level, fill_value)
        return ProxyObject(ans)

    def rsub(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.rsub(other, axis, level, fill_value)
        return ProxyObject(ans)

    def rtruediv(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.rtruediv(other, axis, level, fill_value)
        return ProxyObject(ans)

    def rfloordiv(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.rfloordiv(other, axis, level, fill_value)
        return ProxyObject(ans)

    def rpow(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.rpow(other, axis, level, fill_value)
        return ProxyObject(ans)

    def rmod(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[Level] = None,
        fill_value: Optional[float] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.rmod(other, axis, level, fill_value)
        return ProxyObject(ans)

    def eq(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[IndexLabel] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.eq(other, axis, level)
        return ProxyObject(ans)

    def ne(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[IndexLabel] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.ne(other, axis, level)
        return ProxyObject(ans)

    def lt(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[IndexLabel] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.lt(other, axis, level)
        return ProxyObject(ans)

    def gt(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[IndexLabel] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.gt(other, axis, level)
        return ProxyObject(ans)

    def le(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[IndexLabel] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.le(other, axis, level)
        return ProxyObject(ans)

    def ge(
        self,
        other: Union[Scalar, ArrayLike],
        axis: Axis = "columns",
        level: Optional[IndexLabel] = None,
    ) -> Type[ProxyObject]:
        ans = self.frame.ge(other, axis, level)
        return ProxyObject(ans)
