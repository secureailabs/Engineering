#pragma once

#include <windows.h>

#include "CoreTypes.h"

#include <string>
#include <vector>

/// <summary>
/// 
/// </summary>
/// <param name="c_szFilename">Target filename to load</param>
/// <returns>On Success. An STL vector containing the binary contents of the file.</returns>
/// <returns>On Failure. An empty STL vector.</returns>
extern std::vector<Byte> __stdcall GetBinaryFileBuffer(
    const char * c_szFilename
    ) throw();

/// <summary>
/// 
/// </summary>
/// <param name="c_strAnsiString"></param>
/// <returns></returns>
extern BSTR __stdcall ConvertToBSTR(
    _in const std::string & c_strAnsiString
    ) throw();

/// <summary>
/// 
/// </summary>
/// <param name="un64MillisecondEpochGmtTimestamp"></param>
/// <returns></returns>
extern std::string __stdcall GetDateStringFromEpochMillisecondTimestamp(
    _in uint64_t un64MillisecondEpochGmtTimestamp
    );

/// <summary>
/// This function takes in an address, which may be a numerical ip address, or it may be
/// a URL. In either case, the function will produce a valid numerical ip address or throw
/// an exception if the address is not found, or if the format of the address is invalid
/// </summary>
/// <param name="c_strIncomingAddress"></param>
/// <returns></returns>
extern std::string __stdcall GetNumericalIpAddress(
    _in const std::string & c_strIncomingAddress
    );