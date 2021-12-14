#include "Windows.h"

#include "64BitHashes.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "Guid.h"
#include "JsonParser.h"
#include "SharedUtilityFunctions.h"

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

    catch (BaseException oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __LINE__);
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

    catch (BaseException oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return pszString;
}

static std::string gs_strReconvertedJson;
static std::string gs_strReconvertedStronglyTypedJson;

/// <summary>
/// 
/// </summary>
/// <param name="c_szJsonString"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl TestConvertJsonStringToStructuredBuffer(
    _in const char * c_szJsonString
    )
{
    __DebugFunction();

    std::string strStructureBufferStringRepresentation;

    try
    {
        StructuredBuffer oStructuredBuffer(::ConvertJsonStringToStructuredBuffer(c_szJsonString));
        strStructureBufferStringRepresentation = oStructuredBuffer.ToString();
        gs_strReconvertedJson = ::ConvertStructuredBufferToJson(oStructuredBuffer);
        gs_strReconvertedStronglyTypedJson = ::ConvertStructuredBufferToJson(oStructuredBuffer);
    }

    catch (BaseException oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __LINE__);
        strStructureBufferStringRepresentation = oBaseException.GetExceptionMessage();
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return  ::ConvertToBSTR(strStructureBufferStringRepresentation.c_str());
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szJsonString"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl TestConvertStructuredBufferToStandardJson(void)
{
    __DebugFunction();

    return  ::ConvertToBSTR(gs_strReconvertedJson.c_str());
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl TestConvertStructuredBufferToStronglyTypedJson(void)
{
    __DebugFunction();

    return  ::ConvertToBSTR(gs_strReconvertedStronglyTypedJson.c_str());
}