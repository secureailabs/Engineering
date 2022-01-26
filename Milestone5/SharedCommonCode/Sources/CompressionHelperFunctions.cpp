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
#include "ExceptionRegister.h"
#include "StructuredBuffer.h"

#include <Alloc.h>
#include <Lzma2Dec.h>
#include <Lzma2Enc.h>

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
    const void * c_pbRawBytes,
    uint64_t unRawBufferSizeInBytes
    ) throw()
{
    __DebugFunction();
    __DebugAssert(nullptr != c_pbRawBytes);
    __DebugAssert(unRawBufferSizeInBytes > 0);

    StructuredBuffer oCompressedBuffer;
    
    try
    {
        

        // In a very worst case scenario data which is completely random will bloat
        // our compressed size.  We don't expect this in reality, but we also shouldn't
        // fail if we encounter it - hence the multiply by 1.1
        std::vector<Byte> stlCompressedDestination(unRawBufferSizeInBytes * 1.1);
        size_t unOutBufSize = stlCompressedDestination.size();

        CLzma2EncHandle hEncodeHandle = ::Lzma2Enc_Create(&g_Alloc, &g_BigAlloc);
        __DebugAssert(NULL != hEncodeHandle);

        CLzma2EncProps encodeProperties;

        ::Lzma2EncProps_Init(&encodeProperties);

        // Level dictates the quality of compression (1 being fastest, 9 being most compressed)
        encodeProperties.lzmaProps.level = 1;

        // How many concurrent threads should LZMA2 use for encoding. Going beyond the machine's
        // actual cores will yield no further benefit
        encodeProperties.numTotalThreads = 4;

        // Algo = 0 sets to fast algorithm
        encodeProperties.lzmaProps.algo = 0;

        // This establishes known sane defaults from the LZMA library, and sanitizes our settings
        ::Lzma2EncProps_Normalize(&encodeProperties);

        SRes nLzmaStatus = ::Lzma2Enc_SetProps(hEncodeHandle, &encodeProperties);
        __DebugAssert(SZ_OK == nLzmaStatus);

        nLzmaStatus = ::Lzma2Enc_Encode2(
                            hEncodeHandle,
                            nullptr,
                            reinterpret_cast<Byte*>(&stlCompressedDestination[0]),
                            &unOutBufSize,
                            nullptr,
                            reinterpret_cast<const Byte*>(c_pbRawBytes),
                            unRawBufferSizeInBytes,
                            nullptr);

        // Clean-up the operation before any assertions
        ::Lzma2Enc_Destroy(hEncodeHandle);
        __DebugAssert(SZ_OK == nLzmaStatus);

        // Lzma2 Encoding will tell us exactly how many bytes we compressed into
        stlCompressedDestination.resize(unOutBufSize);

        oCompressedBuffer.PutBuffer("CompressedBuffer", stlCompressedDestination);
        oCompressedBuffer.PutUnsignedInt64("OriginalSize", unRawBufferSizeInBytes);
        oCompressedBuffer.PutByte("EncodingProperty", Lzma2Enc_WriteProperties(hEncodeHandle));

        //std::cout << "Compression ratio: " << (1 - (double(unOutBufSize) / double(unRawBufferSizeInBytes))) * 100.0f << "% (" << unRawBufferSizeInBytes << " -> " << unOutBufSize << ")" << std::endl;
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    return oCompressedBuffer;
}

/********************************************************************************************
 *
 * @function DecompressStructuredBuffer
 * @brief Uses LZMA2 compression to compress the data and build a structured buffer from it
 * @param[in] c_oCompressedBuffer - The StructuredBuffer to pull data from
 * @return std::vector<Byte> - The decompressed data
 *
 ********************************************************************************************/
std::vector<Byte> __stdcall DecompressStructuredBuffer(
    const StructuredBuffer & c_oCompressedBuffer
    ) throw()
{
    __DebugFunction();

    std::vector<Byte> stlDecompressedBuffer;
    
    try
    {
        std::vector<Byte> stlCompressedBuffer = c_oCompressedBuffer.GetBuffer("CompressedBuffer");
        uint64_t unOriginalSize = c_oCompressedBuffer.GetUnsignedInt64("OriginalSize");
        Byte bEncodingProperties = c_oCompressedBuffer.GetByte("EncodingProperty");

        stlDecompressedBuffer.resize(unOriginalSize);
        
        uint64_t unCompressedSize = stlCompressedBuffer.size();
        ELzmaStatus pLzmaStatus;

        SRes nLzmaStatus = ::Lzma2Decode(stlDecompressedBuffer.data(), &unOriginalSize,
            stlCompressedBuffer.data(), &unCompressedSize,
            bEncodingProperties, LZMA_FINISH_END, &pLzmaStatus, &g_Alloc);

        // LZMA_STATUS_FINISHED_WITH_MARK tells us we found our end marker
        __DebugAssert((SZ_OK == nLzmaStatus) && (pLzmaStatus == LZMA_STATUS_FINISHED_WITH_MARK));
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    return stlDecompressedBuffer;
}

