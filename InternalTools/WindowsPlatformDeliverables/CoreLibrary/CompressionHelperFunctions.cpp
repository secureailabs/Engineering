/*********************************************************************************************
 *
 * @file CompressionHelperFunctions.cpp
 * @author David Gascon
 * @date 25 October 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "StructuredBuffer.h"

#include <iostream>

/********************************************************************************************
 *
 * @function CompressToStructuredBuffer
 * @brief Uses LZMA2 compression to compress the data and build a structured buffer from it
 * @param[in] c_pbRawBytes pointer to the data buffer
 * @param[in] unRawBufferSizeInBytes size of the data buffer
 * @return A StructuredBuffer containing the compressed data, its size, and encoding properties
 *
 ********************************************************************************************/
StructuredBuffer __stdcall CompressToStructuredBuffer(
    _in const void * c_pbRawBytes,
    _in uint64_t un64RawBufferSizeInBytes
    ) throw()
{
    __DebugFunction();

    StructuredBuffer oCompressedBuffer;

    try
    {
        oCompressedBuffer.PutBuffer("CompressedBuffer", (const Byte *) c_pbRawBytes, (unsigned int) un64RawBufferSizeInBytes);
        oCompressedBuffer.PutUnsignedInt64("OriginalSize", un64RawBufferSizeInBytes);
        oCompressedBuffer.PutUnsignedInt64("CompressedSize", un64RawBufferSizeInBytes);
        oCompressedBuffer.PutByte("EncodingProperty", 0x00);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return oCompressedBuffer;
}

/********************************************************************************************
 *
 * @function DecompressStructuredBuffer
 * @brief Uses LZMA2 compression to compress the data and build a structured buffer from it
 * @param[in] compressedBuffer - The StructuredBuffer to pull data from
 * @return std::vector<Byte> - The decompressed data
 *
 ********************************************************************************************/
std::vector<Byte> __stdcall DecompressStructuredBuffer(
    _in const StructuredBuffer & c_oCompressedBuffer
    ) throw()
{
    __DebugFunction();

    try
    {
        _ThrowBaseExceptionIf((false == c_oCompressedBuffer.IsElementPresent("CompressedBuffer", BUFFER_VALUE_TYPE)), "ERROR: Invalid input, missing CompressedBuffer element.", nullptr);
        _ThrowBaseExceptionIf((false == c_oCompressedBuffer.IsElementPresent("OriginalSize", UINT64_VALUE_TYPE)), "ERROR: Invalid input, missing OriginalSize element.", nullptr);
        _ThrowBaseExceptionIf((false == c_oCompressedBuffer.IsElementPresent("CompressedSize", UINT64_VALUE_TYPE)), "ERROR: Invalid input, missing CompressedSize element.", nullptr);
        _ThrowBaseExceptionIf((c_oCompressedBuffer.GetUnsignedInt64("OriginalSize") != c_oCompressedBuffer.GetUnsignedInt64("CompressedSize")), "ERROR: Invalid input, (OriginalSize != CompressedSize)", nullptr);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return c_oCompressedBuffer.GetBuffer("CompressedBuffer");
}