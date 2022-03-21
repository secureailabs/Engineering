/*********************************************************************************************
 *
 * @file SailWebApiFunctions.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Implementation of the Guid class that handles 128 bit (16 bytes) GUID/UUID values.
 *
 ********************************************************************************************/

#include <Windows.h>    // Always include Windows.h first

#include "64BitHashes.h"
#include "CompressionHelperFunctions.h"
#include "CoreTypes.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "Guid.h"
#include "SmartMemoryAllocator.h"
#include "StructuredBuffer.h"

 /// <summary>
 /// We need this special function coupled with the SmartMemoryAllocator to make sure that we
 /// are properly freeing the memory relating to the internal wszUnicodeString variable
 /// </summary>
 /// <param name="c_strAnsiString"></param>
 /// <returns></returns>
static BSTR __cdecl ConvertToBSTR(
    _in const std::string & c_strAnsiString
    ) throw()
{
    __DebugFunction();

    BSTR pszString = nullptr;

    try
    {
        // User the SmartMemoryAllocator in order to make sure that we deallocate memory properly
        // even if an exception is thrown
        SmartMemoryAllocator oSmartMemoryAllocator;
        // Convert the char * string to wchar * string 
        size_t unCharacterCountIncludingNullTerminatingCharacter = (size_t)(c_strAnsiString.size() + 1);
        size_t unConvertedChars = 0;
        wchar_t* wszUnicodeString = (wchar_t*)oSmartMemoryAllocator.Allocate((unsigned int)unCharacterCountIncludingNullTerminatingCharacter * sizeof(wchar_t));
        ::mbstowcs_s(&unConvertedChars, wszUnicodeString, unCharacterCountIncludingNullTerminatingCharacter, c_strAnsiString.c_str(), c_strAnsiString.size());
        pszString = ::SysAllocString(wszUnicodeString);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return pszString;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szString"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) uint64_t __cdecl Get64BitHashOfString(
    _in const char * c_szValue,
    _in bool fCaseSensitive
    )
{
    __DebugFunction();

    // [DllImport("64BitHashFunctions.dll", CallingConvention = CallingConvention.Cdecl )]
    // static extern public ulong Get64BitHashOfString(string value, bool caseSensitive);

    uint64_t un64HashValue = 0;

    try
    {
        un64HashValue = ::Get64BitHashOfNullTerminatedString(c_szValue, fCaseSensitive);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return un64HashValue;
}

/// <summary>
/// 
/// </summary>
/// <param name="unType"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl GenerateIdentifier(
    _in unsigned int unType
    )
{
    BSTR pszString = nullptr;

    try
    {
        GuidObjectType eGuidObjectType = (1 == unType) ? eDataset : (2 == unType) ? eTable : eColumn;
        Guid oIdentifier(eGuidObjectType);
        pszString = ::ConvertToBSTR(oIdentifier.ToString(eHyphensOnly));
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return pszString;
}

static std::string gs_strTargetTablePackageFilename;
static std::vector<Byte> gs_stlTablePackageRecordsBuffer;
static Byte * gs_pbWriteTarget = nullptr;
static uint64_t gs_un64CurrentOffset;

/// <summary>
/// 
/// </summary>
/// <param name="c_szTargetFilename"></param>
/// <param name="un64TargetFileSizeInBytes"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) void __cdecl OpenTablePackageFile(
    _in const char * c_szTargetFilename,
    _in uint64_t un64TargetFileSizeInBytes
    )
{
    __DebugFunction();

    try
    {
        gs_strTargetTablePackageFilename = c_szTargetFilename;
        gs_stlTablePackageRecordsBuffer.resize((size_t) (un64TargetFileSizeInBytes * 1.3));
        gs_pbWriteTarget = (Byte *) gs_stlTablePackageRecordsBuffer.data();
        gs_un64CurrentOffset = 0;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }
}

/// <summary>
/// 
/// </summary>
/// <param name="c_aszCellValues"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) void __cdecl AddRecordToTablePackageFile(
    _in const char * c_szRawRecord
    )
{
    __DebugFunction();

    try
    {
        // Create the raw record using OUR settings
        std::string strOutputRecord = c_szRawRecord;
        strOutputRecord += '\n';
        // Now write the record to destination buffer
        ::memcpy((void *) gs_pbWriteTarget, (const void *) strOutputRecord.c_str(), strOutputRecord.length());
        gs_pbWriteTarget += strOutputRecord.length();
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szTableIdentifier"></param>
/// <param name="c_szTableTitle"></param>
/// <param name="c_szTableDescription"></param>
/// <param name="c_szTableTags"></param>
/// <param name="nNumberOfColumns"></param>
/// <param name="nNumberOfRows"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) void __cdecl CompleteTablePackageFile(
    _in const char * c_szTableIdentifier,
    _in const char * c_szTableTitle,
    _in const char * c_szTableDescription,
    _in const char * c_szTableTags,
    _in int nNumberOfColumns,
    _in int nNumberOfRows
    )
{
    __DebugFunction();

    try
    {
        StructuredBuffer oTablePackage;
        StructuredBuffer oCompressedData = ::CompressToStructuredBuffer((const void *) gs_stlTablePackageRecordsBuffer.data(), (uint64_t) gs_stlTablePackageRecordsBuffer.size());

        oTablePackage.PutGuid("Identifier", Guid(c_szTableIdentifier));
        oTablePackage.PutString("Title", c_szTableTitle);
        oTablePackage.PutString("Description", c_szTableDescription);
        oTablePackage.PutString("Tags", c_szTableTags);
        oTablePackage.PutUnsignedInt64("NumberOfColumns", nNumberOfColumns);
        oTablePackage.PutUnsignedInt64("NumberOfRows", nNumberOfRows);
        oTablePackage.PutStructuredBuffer("CompressedData", oCompressedData);

        const Byte * c_pbSerializedOutput = oTablePackage.GetSerializedBufferRawDataPtr();
        uint64_t un64SerializedOutputSizeInBytes = oTablePackage.GetSerializedBufferRawDataSizeInBytes();
        HANDLE hFileHandle = ::CreateFileA(gs_strTargetTablePackageFilename.c_str(), GENERIC_WRITE, 0, nullptr, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
        _ThrowBaseExceptionIf((INVALID_HANDLE_VALUE == hFileHandle), "Failed to open file %s with GetLastError() = %d", gs_strTargetTablePackageFilename.c_str(), ::GetLastError());
        // TODO: Handle files that are more than 4Gb
        unsigned int unNumberOfBytesWritten = 0;
        ::WriteFile(hFileHandle, (const void *) c_pbSerializedOutput, (DWORD) un64SerializedOutputSizeInBytes, (DWORD *) &unNumberOfBytesWritten, nullptr);
        ::CloseHandle(hFileHandle);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }
}