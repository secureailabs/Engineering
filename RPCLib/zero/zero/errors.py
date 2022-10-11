# -------------------------------------------------------------------------------
# Engineering
# errors.py
# -------------------------------------------------------------------------------
"""RPC exception and error module"""
# -------------------------------------------------------------------------------
# modified from https://github.com/Ananto30/zero under MIT license
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------


class ZeroException(Exception):
    pass


class MethodNotFoundException(ZeroException):
    pass
