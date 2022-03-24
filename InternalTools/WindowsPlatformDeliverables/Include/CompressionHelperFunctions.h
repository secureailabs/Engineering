//////////////////////////////////////////////////////////////////////////////////////////////
//
// @file CompressionHelperFunctions.h
// @author David Gascon
// @date 25 October 2021
// @License Private and Confidential. Internal Use Only.
// @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
//
//////////////////////////////////////////////////////////////////////////////////////////////


#pragma once

#include "CoreTypes.h"
#include "StructuredBuffer.h"

/********************************************************************************************/
extern StructuredBuffer __stdcall CompressToStructuredBuffer(
    _in const void * c_pbRawBytes,
    _in uint64_t unRawBufferSizeInBytes
    ) throw();

/********************************************************************************************/
extern std::vector<Byte> __stdcall DecompressStructuredBuffer(
    _in const StructuredBuffer & c_oCompressedBuffer
    ) throw();