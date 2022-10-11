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

# from pydoc import locate


# class LogisticRegression(torch.nn.Module):
#     def __init__(self, input_dim, output_dim):
#         super(LogisticRegression, self).__init__()
#         self.in_features = input_dim
#         self.out_features = output_dim
#         self.linear = torch.nn.Linear(input_dim, output_dim)

#     def forward(self, x):
#         outputs = torch.sigmoid(self.linear(x))
#         return outputs


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


# class TorchLinearModel:
#     def __init__(self, obj):
#         self.content = obj
#         self.type = str(type(obj))
#         self.in_features = obj.in_features
#         self.out_features = obj.out_features

#     def _convert_tensor(self):
#         state = self.content.state_dict()
#         state = dict(state)
#         for key in state:
#             if isinstance(state[key], torch.Tensor):
#                 state[key] = state[key].tolist()
#         return state

#     def to_dict(self):
#         return {
#             "content": self._convert_tensor(),
#             "in_features": self.in_features,
#             "out_features": self.out_features,
#             "type": self.type,
#             "TorchLinearModel": True,
#         }

#     @staticmethod
#     def makeModel(msg):
#         for key in msg["content"]:
#             if isinstance(msg["content"][key], list):
#                 msg["content"][key] = torch.Tensor(msg["content"][key])
#         model = LogisticRegression(msg["in_features"], msg["out_features"])
#         model.load_state_dict(msg["content"])
#         return model
