# -------------------------------------------------------------------------------
# Engineering
# customtypes.py
# -------------------------------------------------------------------------------
"""RPC data types for secret control"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import uuid


class SecretObject:
    def __init__(self, obj):
        """
        Secret object type

        :param obj: python object to be converted
        :type obj: Any
        """
        self.content = obj
        self.guid = uuid.uuid4().hex
        self.type = str(type(obj))

    def to_dict(self):
        """
        serialize secret object to dict

        :return: dict
        :rtype: dict
        """
        return {
            "id": self.guid,
            "type": self.type,
            "object": 2,
        }


class ProxyObject:
    def __init__(self, obj):
        """
        Proxy object type

        :param obj: python object to be converted
        :type obj: Any
        """
        self.content = obj
        self.guid = uuid.uuid4().hex
        self.type = str(type(obj))

    def to_dict(self):
        """
        serilize proxy object to dict

        :return: dict
        :rtype: dict
        """
        return {
            "id": self.guid,
            "type": self.type,
            "object": 1,
        }
