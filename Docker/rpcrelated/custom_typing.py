from datetime import datetime, timedelta, tzinfo
from typing import Any, Callable, Hashable, List, Mapping, Optional, Tuple, Union

import numpy as np
import pandas as pd
from pandas import Interval
from pandas._libs import Period, Timedelta, Timestamp

ArrayLike = Union[pd.Series, pd.DataFrame, np.ndarray, tuple, list]

# scalars

PythonScalar = Union[str, int, float, bool]
DatetimeLikeScalar = Union[Period, Timestamp, Timedelta]
PandasScalar = Union[Period, Timestamp, Timedelta, Interval]
Scalar = Union[PythonScalar, PandasScalar]


# timestamp and timedelta convertible types

TimestampConvertibleTypes = Union["Timestamp", datetime, np.datetime64, int, np.int64, float, str]
TimedeltaConvertibleTypes = Union["Timedelta", timedelta, np.timedelta64, int, np.int64, float, str]
Timezone = Union[str, tzinfo]


Axis = Union[str, int]
IndexLabel = Union[Hashable, List[Hashable]]
Level = Union[Hashable, int]

Shape = Tuple[int, ...]
Suffixes = Tuple[Optional[str], Optional[str]]
Ordered = Optional[bool]
# JSONSerializable = Optional[Union[PythonScalar, List, Dict]]
Frequency = Union[str, "DateOffset"]
# Axes = Collection[Any]

# RandomState = Union[
#     int,
#     ArrayLike,
#     np.random.Generator,
#     np.random.BitGenerator,
#     np.random.RandomState,
# ]

# # dtypes
# NpDtype = Union[str, np.dtype, type_t[Union[str, float, int, complex, bool, object]]]
# Dtype = Union["ExtensionDtype", NpDtype]
# AstypeArg = Union["ExtensionDtype", "npt.DTypeLike"]
# # DtypeArg specifies all allowable dtypes in a functions its dtype argument
# DtypeArg = Union[Dtype, Dict[Hashable, Dtype]]
# DtypeObj = Union[np.dtype, "ExtensionDtype"]

# For functions like rename that convert one label to another
Renamer = Union[Mapping[Hashable, Any], Callable[[Hashable], Hashable]]

# # to maintain type information across generic functions and parametrization
# T = TypeVar("T")

# # used in decorators to preserve the signature of the function it decorates
# # see https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
# FuncType = Callable[..., Any]
# F = TypeVar("F", bound=FuncType)

# # types of vectorized key functions for DataFrame::sort_values and
# # DataFrame::sort_index, among others
# ValueKeyFunc = Optional[Callable[["Series"], Union["Series", AnyArrayLike]]]
# IndexKeyFunc = Optional[Callable[["Index"], Union["Index", AnyArrayLike]]]

# # types of `func` kwarg for DataFrame.aggregate and Series.aggregate
# AggFuncTypeBase = Union[Callable, str]
# AggFuncTypeDict = Dict[Hashable, Union[AggFuncTypeBase, List[AggFuncTypeBase]]]
# AggFuncType = Union[
#     AggFuncTypeBase,
#     List[AggFuncTypeBase],
#     AggFuncTypeDict,
# ]
# AggObjType = Union[
#     "Series",
#     "DataFrame",
#     "GroupBy",
#     "SeriesGroupBy",
#     "DataFrameGroupBy",
#     "BaseWindow",
#     "Resampler",
# ]

# PythonFuncType = Callable[[Any], Any]

# # filenames and file-like-objects
# AnyStr_cov = TypeVar("AnyStr_cov", str, bytes, covariant=True)
# AnyStr_con = TypeVar("AnyStr_con", str, bytes, contravariant=True)


# FilePath = Union[str, "PathLike[str]"]

# # for arbitrary kwargs passed during reading/writing files
# StorageOptions = Optional[Dict[str, Any]]


# # compression keywords and compression
# CompressionDict = Dict[str, Any]
# CompressionOptions = Optional[Union[Literal["infer", "gzip", "bz2", "zip", "xz", "zstd"], CompressionDict]]
# XMLParsers = Literal["lxml", "etree"]


# # types in DataFrameFormatter
# FormattersType = Union[List[Callable], Tuple[Callable, ...], Mapping[Union[str, int], Callable]]
# ColspaceType = Mapping[Hashable, Union[str, int]]
# FloatFormatType = Union[str, Callable, "EngFormatter"]
# ColspaceArgType = Union[str, int, Sequence[Union[str, int]], Mapping[Hashable, Union[str, int]]]

# # Arguments for fillna()
# FillnaOptions = Literal["backfill", "bfill", "ffill", "pad"]

# # internals
# Manager = Union["ArrayManager", "SingleArrayManager", "BlockManager", "SingleBlockManager"]
# SingleManager = Union["SingleArrayManager", "SingleBlockManager"]
# Manager2D = Union["ArrayManager", "BlockManager"]

# indexing
# PositionalIndexer -> valid 1D positional indexer, e.g. can pass
# to ndarray.__getitem__
# ScalarIndexer is for a single value as the index
# SequenceIndexer is for list like or slices (but not tuples)
# PositionalIndexerTuple is extends the PositionalIndexer for 2D arrays
# These are used in various __getitem__ overloads
# TODO(typing#684): add Ellipsis, see
# https://github.com/python/typing/issues/684#issuecomment-548203158
# https://bugs.python.org/issue41810
# Using List[int] here rather than Sequence[int] to disallow tuples.
# ScalarIndexer = Union[int, np.integer]
# SequenceIndexer = Union[slice, List[int], np.ndarray]
# PositionalIndexer = Union[ScalarIndexer, SequenceIndexer]
# PositionalIndexerTuple = Tuple[PositionalIndexer, PositionalIndexer]
# PositionalIndexer2D = Union[PositionalIndexer, PositionalIndexerTuple]
# if TYPE_CHECKING:
#     TakeIndexer = Union[Sequence[int], Sequence[np.integer], npt.NDArray[np.integer]]
# else:
#     TakeIndexer = Any

# # Windowing rank methods
# WindowingRankType = Literal["average", "min", "max"]

# # read_csv engines
# CSVEngine = Literal["c", "python", "pyarrow", "python-fwf"]
