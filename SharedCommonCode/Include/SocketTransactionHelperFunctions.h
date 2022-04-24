/*********************************************************************************************
 *
 * @file TlsHelperFunctions.h
 * @author Prawal Gangwar
 * @date 18 Feb 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "CoreTypes.h"
#include "Socket.h"
#include "StructuredBuffer.h"

extern std::vector<Byte> __stdcall GetSocketTransaction(
    _in Socket * poSocket,
    _in unsigned int unMillisecondTimeout
    );

extern bool __stdcall PutSocketTransaction(
    _in Socket * poSocket,
    _in const std::vector<Byte> & c_stlSerializedTransaction
    ) throw();
