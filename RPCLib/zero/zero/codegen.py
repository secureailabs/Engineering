# -------------------------------------------------------------------------------
# Engineering
# codegen.py
# -------------------------------------------------------------------------------
"""RPC client side code generation tool"""
# -------------------------------------------------------------------------------
# modified from https://github.com/Ananto30/zero under MIT license
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import inspect

# from pydantic import BaseModel
from zero.type_util import is_pydantic


class CodeGen:
    def __init__(self, rpc_router, rpc_input_type_map, rpc_return_type_map):
        """
        init code generator

        :param rpc_router: rpc dict
        :type rpc_router: dict
        :param rpc_input_type_map: rpc input type dict
        :type rpc_input_type_map: dict
        :param rpc_return_type_map: rpc return type dict
        :type rpc_return_type_map: dict
        """
        self._rpc_router = rpc_router
        self._rpc_input_type_map = rpc_input_type_map
        self._rpc_return_type_map = rpc_return_type_map
        self._typing_imports = set()

    def generate_code(self, host="localhost", port=5559):
        """
        generate code
        """
        code = f"""
import typing  # remove this if not needed
from typing import List, Dict, Union, Optional, Tuple  # remove this if not needed
from zero import ZeroClient


zero_client = ZeroClient("{host}", {port})


class RpcClient:
    def __init__(self, zero_client: ZeroClient):
        self._zero_client = zero_client
        """

        for f in self._rpc_router:
            code += f"""
    def {f}(self, {self.get_function_str(f)}
        return self._zero_client.call("{f}", {None if self._rpc_input_type_map[f] is None else "msg"})
        """
        # self.generate_data_classes()  TODO: next feature
        return code

    def get_imports(self):
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """
        return f"from typing import {', '.join([i for i in self._typing_imports])}"

    def get_input_type_str(self, func_name: str):  # pragma: no cover
        """
        get input type

        :param func_name: function name
        :type func_name: str
        :return: type dict
        :rtype: dict
        """
        if self._rpc_input_type_map[func_name] is None:
            return ""
        if self._rpc_input_type_map[func_name].__module__ == "typing":
            n = self._rpc_input_type_map[func_name]._name
            self._typing_imports.add(n)
            return ": " + n
        return ": " + self._rpc_input_type_map[func_name].__name__

    def get_return_type_str(self, func_name: str):  # pragma: no cover
        """
        get return type

        :param func_name: function name
        :type func_name: str
        :return: return type dict
        :rtype: dict
        """
        if self._rpc_return_type_map[func_name].__module__ == "typing":
            n = self._rpc_return_type_map[func_name]._name
            self._typing_imports.add(n)
            return n
        return self._rpc_return_type_map[func_name].__name__

    def get_function_str(self, func_name: str):
        """
        get function router info

        :param func_name: function name
        :type func_name: str
        :return: function router info
        :rtype: dict
        """
        return inspect.getsourcelines(self._rpc_router[func_name])[0][0].split("(", 1)[1].replace("\n", "")

    def generate_data_classes(self):  # pragma: no cover
        # TODO: next target, add pydantic support
        """
        get data classes
        """
        code = ""
        for f in self._rpc_input_type_map:
            input_class = self._rpc_input_type_map[f]
            if input_class and is_pydantic(input_class):
                code += inspect.getsource(input_class)
        # print(code)
