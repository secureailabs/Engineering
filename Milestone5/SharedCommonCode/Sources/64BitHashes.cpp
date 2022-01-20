/*********************************************************************************************
 *
 * @file 64BitHashes.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Implementations of C functions used to generate quick 64 bit hashes.
 *
 * In some circumstances, it is really useful to use 64-bit hashes as opposed to larger
 * hashes like MD-5 or SHA-1 and SHA-2. The biggest use of such hashes are for indexing
 * element using STL objects, like std::map. Since 64 bit is a native size to the CPU, it
 * indexes a lot quicker within STL than if you used a larger buffer hosting a more
 * traditional hash.
 *
 ********************************************************************************************/

#include "DebugLibrary.h"
#include "64BitHashes.h"

/********************************************************************************************
 *
 * @function Get64BitHashOfNullTerminatedString
 * @param[in] c_szString Pointer to the null terminated string to be hashed.
 * @param[in] fCaseSensitive True if the hash is case sensitive and false if the hash is case insensitive
 * @brief Function returns a 64 bit hash for a null terminated string.
 * @return 0 if (nullptr == @p c_szString)
 * @return 0 if (0 == sizeof(@p c_szString))
 * @return A valid 64 bit hash
 * @warning The 64 bit hash generated by this function is not cryptographically strong.
 *
 ********************************************************************************************/

Qword __cdecl Get64BitHashOfNullTerminatedString(
    _in const char * c_szString,
    _in bool fCaseSensitive
    )
{
    Qword qwHash = 0;

    if (NULL != c_szString)
    {
        Dword dwHighOrderHash = 5281;
        Dword dwLowOrderHash = 1315423911;
        unsigned int unStringIndex = 0;

        while (0 != c_szString[unStringIndex])
        {
            Dword dwToken = (true == fCaseSensitive) ? c_szString[unStringIndex] : (c_szString[unStringIndex] - 'A' + 'a');
            dwHighOrderHash = ((dwHighOrderHash << 5) + dwHighOrderHash) + dwToken;
            dwLowOrderHash ^= ((dwLowOrderHash << 5) + (Dword) dwToken + (dwLowOrderHash >> 2));
            ++unStringIndex;
        }

        qwHash = MAKE_QWORD(dwHighOrderHash, dwLowOrderHash);
    }

    return qwHash;
}

/********************************************************************************************
 *
 * @function Get64BitHashOfByteArray
 * @param[in] c_pbBuffer Pointer to the byte buffer to be hashed.
 * @param[in] unBufferSizeInBytes Size in bytes of the byte buffer @p c_pbBuffer to be hashed.
 * @brief Function returns a 64 bit hash for a byte buffer @p c_pbBuffer of size @p unBufferSizeInBytes.
 * @return 0 if (nullptr == @p c_pbBuffer)
 * @return 0 if (0 == @p unBufferSizeInBytes)
 * @return A valid 64 bit hash
 * @warning The 64 bit hash generated by this function is not cryptographically strong.
 *
 ********************************************************************************************/
    
Qword __cdecl Get64BitHashOfByteArray(
    _in const Byte * c_pbBuffer,
    _in unsigned int unBufferSizeInBytes
    )
{
    Qword qwHash = 0;

    if (NULL != c_pbBuffer)
    {
        Dword dwHighOrderHash = 5281;
        Dword dwLowOrderHash = 1315423911;

        for (unsigned int unIndex = 0; unIndex < unBufferSizeInBytes; ++unIndex)
        {
            dwHighOrderHash = ((dwHighOrderHash << 5) + dwHighOrderHash) + (Dword) c_pbBuffer[unIndex];
            dwLowOrderHash ^= ((dwLowOrderHash << 5) + (Dword) c_pbBuffer[unIndex] + (dwLowOrderHash >> 2));
        }

        qwHash = MAKE_QWORD(dwHighOrderHash, dwLowOrderHash);
    }

    return qwHash;
}
