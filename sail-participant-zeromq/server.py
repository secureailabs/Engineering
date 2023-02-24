import importlib
import inspect
import os
import pkgutil
import sys
from queue import Queue

import sail_safe_functions
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.data_model.data_model_longitudinal import DataModelLongitudinal
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions.aggregator.reference_dataset_tabular import ReferenceDatasetTabular
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.safe_function_base import SafeFunctionBase
from zero import ZeroServer


def register_safe_functions(server: ZeroServer):
    # this function walks the safe function library starting from the root,
    # it looks for classes that extend the safe function base class
    # in then registers the run function from each of those classes as an rpc
    # this we we can add whatever helper classes and objects we want to the safe function library
    # without worrying about them being picked up as RPCs

    # TODO do something similar with serializable objects and add those to the serialization tables

    root_path = os.path.dirname(sail_safe_functions.__file__)
    queue_module = Queue()
    queue_module.put((["sail_safe_functions"], root_path))
    dict_import = {}
    while not queue_module.empty():
        list_name_module, module_path = queue_module.get()
        for module_finder, name, ispkg in pkgutil.iter_modules([module_path]):
            list_name_module_new = list_name_module.copy()
            list_name_module_new.append(name)
            path_dir_module = os.path.join(module_finder.path, name)
            queue_module.put((list_name_module_new, path_dir_module))
            name_module = ".".join(list_name_module_new)
            moduleipl = importlib.import_module(name_module)
            for name_member, object_member in inspect.getmembers(moduleipl):
                if inspect.isclass(object_member):
                    if issubclass(object_member, SafeFunctionBase):
                        if object_member != SafeFunctionBase:
                            # TODO check if run function actually exists!!!
                            dict_import[name_member] = object_member.run

    for name_safe_function, safe_function in dict_import.items():
        print(f"adding: {name_safe_function}")
        server.register_rpc(safe_function, name_safe_function)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise RuntimeError("must have port number argument")
    port = int(sys.argv[1])
    server = ZeroServer(port=port)
    register_safe_functions(server)

    server._serializer_table["ReferenceDatasetLongitudinal"] = ReferenceDatasetLongitudinal
    server._serializer_table["ReferenceDatasetTabular"] = ReferenceDatasetTabular
    server._serializer_table["ReferenceDataFrame"] = ReferenceDataFrame
    server._serializer_table["ReferenceSeries"] = ReferenceSeries
    server._serializer_table["DataModelTabular"] = DataModelTabular
    server._serializer_table["DataModelLongitudinal"] = DataModelLongitudinal
    server._serializer_table["DataModelDataFrame"] = DataModelDataFrame
    server._serializer_table["DataModelSeries"] = DataModelSeries

    server._deserializer_table["ReferenceDatasetLongitudinal"] = ReferenceDatasetLongitudinal
    server._deserializer_table["ReferenceDatasetTabular"] = ReferenceDatasetTabular
    server._deserializer_table["ReferenceDataFrame"] = ReferenceDataFrame
    server._deserializer_table["ReferenceSeries"] = ReferenceSeries
    server._deserializer_table["DataModelTabular"] = DataModelTabular
    server._deserializer_table["DataModelLongitudinal"] = DataModelLongitudinal
    server._deserializer_table["DataModelDataFrame"] = DataModelDataFrame
    server._deserializer_table["DataModelSeries"] = DataModelSeries
    server.run()
