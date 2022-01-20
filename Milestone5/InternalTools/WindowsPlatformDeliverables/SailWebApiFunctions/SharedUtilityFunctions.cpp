#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <ip2string.h>
#include <OleAuto.h>
#include <stdio.h>
#include <time.h>

#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "SharedUtilityFunctions.h"
#include "SmartMemoryAllocator.h"

static int gs_nWsaStartupStatus = 0xFFFFFFFF;

/// <summary>
/// 
/// </summary>
/// <param name="c_szFilename"></param>
/// <returns></returns>
std::vector<Byte> __stdcall GetBinaryFileBuffer(
    const char * c_szFilename
    ) throw()
{
    __DebugFunction();

    std::vector<Byte> stlBinaryBuffer;
    HANDLE hFileHandle = ::CreateFileA(c_szFilename, GENERIC_READ, FILE_SHARE_READ, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);

    try
    {
        _ThrowBaseExceptionIf((INVALID_HANDLE_VALUE == hFileHandle), "Failed to open file %s", c_szFilename);
        BY_HANDLE_FILE_INFORMATION sFileInformation;
        bool fSuccess = ::GetFileInformationByHandle(hFileHandle, &sFileInformation);
        _ThrowBaseExceptionIf((true != fSuccess), "Failed to get file information for %s", c_szFilename);
        uint64_t un64FileSizeInBytes = (uint64_t) MAKE_QWORD(sFileInformation.nFileSizeHigh, sFileInformation.nFileSizeLow);
        // Make sure the buffer is large enough to receive the binary file
        stlBinaryBuffer.resize(un64FileSizeInBytes);
        // Read in the data
        Byte * pbBuffer = (Byte *) stlBinaryBuffer.data();
        uint64_t un64RemainingBytes = un64FileSizeInBytes;
        do
        {
            unsigned int unNumberOfBytesToRead = (unsigned int) min(un64RemainingBytes, 0xFFFFFFFF);
            unsigned int unNumberOfBytesRead = 0;
            fSuccess = ::ReadFile(hFileHandle, (void *) stlBinaryBuffer.data(), (DWORD)unNumberOfBytesToRead, (DWORD*)&unNumberOfBytesRead, nullptr);
            _ThrowBaseExceptionIf((true != fSuccess), "Failed to read file with GetLastError() = %d", ::GetLastError());
            un64RemainingBytes -= unNumberOfBytesRead;
            if (0 < un64RemainingBytes)
            {
                pbBuffer += unNumberOfBytesRead;
                unNumberOfBytesToRead -= unNumberOfBytesRead;
            }
        }
        while (0 < un64RemainingBytes);
    }
    
    catch (BaseException oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    // Make sure to close the file if required
    if (INVALID_HANDLE_VALUE != hFileHandle)
    {
        ::CloseHandle(hFileHandle);
    }

    return stlBinaryBuffer;
}

/// <summary>
/// We need this special function coupled with the SmartMemoryAllocator to make sure that we
/// are properly freeing the memory relating to the internal wszUnicodeString variable
/// </summary>
/// <param name="c_strAnsiString"></param>
/// <returns></returns>
BSTR __stdcall ConvertToBSTR(
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
        size_t unCharacterCountIncludingNullTerminatingCharacter = (size_t) (c_strAnsiString.size() + 1);
        size_t unConvertedChars = 0;
        wchar_t * wszUnicodeString = (wchar_t*) oSmartMemoryAllocator.Allocate((unsigned int) unCharacterCountIncludingNullTerminatingCharacter * sizeof(wchar_t));
        ::mbstowcs_s(&unConvertedChars, wszUnicodeString, unCharacterCountIncludingNullTerminatingCharacter, c_strAnsiString.c_str(), c_strAnsiString.size());
        pszString = ::SysAllocString(wszUnicodeString);
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

/// <summary>
/// 
/// </summary>
/// <param name="un64MillisecondEpochGmtTimestamp"></param>
/// <returns></returns>
std::string __stdcall GetDateStringFromEpochMillisecondTimestamp(
    _in uint64_t un64MillisecondEpochGmtTimestamp
    )
{
    __DebugFunction();

    // Convert the time in seconds to be usable by _localtime32_s
    time_t sEpochGmtTimeInSeconds = un64MillisecondEpochGmtTimestamp / 1000;
    struct tm sTime;
    ::_localtime32_s(&sTime, (const long*) &sEpochGmtTimeInSeconds);

    // Format the time string
    const char * c_szMonths [] = { "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" };
    const char * c_szDayIth [] = { "oops", "st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", "st" };
    char szTemporaryBuffer[80];
    ::sprintf_s(szTemporaryBuffer, sizeof(szTemporaryBuffer), "%s %02d%s, %04d @ %02d:%02d:%02d", c_szMonths[sTime.tm_mon], sTime.tm_mday, c_szDayIth[sTime.tm_mday], (sTime.tm_year + 1900), sTime.tm_hour, sTime.tm_min, sTime.tm_sec);

    return std::string(szTemporaryBuffer);
}

/// <summary>
/// 
/// </summary>
/// <param name="c_strIncomingAddress"></param>
/// <returns></returns>
std::string __stdcall GetNumericalIpAddress(
    _in const std::string & c_strIncomingAddress
    )
{
    __DebugFunction();

    std::string strIpAddress = "0.0.0.0";

    if (0 != gs_nWsaStartupStatus)
    {
        WSADATA sWsaData;
        Word wVersionRequested = MAKEWORD(2, 2);

        gs_nWsaStartupStatus = ::WSAStartup(wVersionRequested, &sWsaData);
        _ThrowBaseExceptionIf((0 != gs_nWsaStartupStatus), "WSA Socket Functions not initialized properly.", nullptr);
    }
    
    if (0 == gs_nWsaStartupStatus)
    {
        ADDRINFOEXA * psAddressInformation = nullptr;

        if (0 == ::GetAddrInfoExA(c_strIncomingAddress.c_str(), nullptr, NS_DNS, nullptr, nullptr, &psAddressInformation, nullptr, nullptr, nullptr, nullptr))
        {
            for (ADDRINFOEXA * psAddressInformationElement = psAddressInformation; nullptr != psAddressInformationElement; psAddressInformationElement = psAddressInformationElement->ai_next)
            {
                if (AF_INET == psAddressInformationElement->ai_family)
                {
                    struct sockaddr_in * psIpv4Address = (struct sockaddr_in *) psAddressInformationElement->ai_addr;
                    char szString[20];
                    
                    strIpAddress = ::InetNtopA(AF_INET, &(psIpv4Address->sin_addr), szString, sizeof(szString));
                }
            }
        }
    }

    return strIpAddress;
}