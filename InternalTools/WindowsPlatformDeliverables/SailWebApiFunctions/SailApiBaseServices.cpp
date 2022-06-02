#include <Windows.h>

#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "JsonParser.h"
#include "RestApiHelperFunctions.h"
#include "SharedUtilityFunctions.h"
#include "StructuredBuffer.h"
#include "SmartMemoryAllocator.h"

#include <mutex>
#include <iostream>

static std::mutex gs_stlMutex;
static bool gs_fIsLoggedOn = false;
static HANDLE gs_EosbMaintenanceThread = INVALID_HANDLE_VALUE;
static Dword gs_dwEosbMaintenanceThreadIdentifier = 0;
static std::string gs_strSailPlatformServicesIpAddress;
static std::string gs_strSailPlatformServicesAccessToken;
static std::string gs_strSailPlatformServicesRefreshToken;
static std::string gs_strCurrentUserIdentifier;
static std::string gs_strCurrentUserOrganizationalIdentifier;
static Qword gs_qwCurrentUserAccessRightsMask;

/// <summary>
/// 
/// </summary>
/// <param name="pParameter"></param>
/// <returns></returns>
static Dword __stdcall AccessTokenMaintenanceThread(
    _in void * pParameter
)
{
    __DebugFunction();

    UNREFERENCED_PARAMETER(pParameter);

    try
    {
        bool fIsLoggedOn = false;
        do
        {
            // Only do this every minute. The rest of the time, just put the thread sleep
            ::Sleep(60000);
            // Check to see if we are still logged on. If not, then this thread ends
            gs_stlMutex.lock();
            fIsLoggedOn = gs_fIsLoggedOn;
            std::string strSailPlatformServicesAccessToken = gs_strSailPlatformServicesAccessToken;
            std::string strSailPlatformServicesRefreshToken = gs_strSailPlatformServicesRefreshToken;
            std::string strSailPlatformServicesIpAddress = gs_strSailPlatformServicesIpAddress;
            Word wSailPlatformServicesPortAddress = 8000;
            gs_stlMutex.unlock();
            if (true == fIsLoggedOn)
            {
                // Sanity check against all of our global variables, and make thread
                // safe copies of each value
                __DebugAssert(0 < strSailPlatformServicesAccessToken.size());
                __DebugAssert(0 < strSailPlatformServicesRefreshToken.size());
                __DebugAssert(0 < strSailPlatformServicesIpAddress.size());
                __DebugAssert(0 < wSailPlatformServicesPortAddress);
                // Now we call into the SAIL Platform Services API portal to refresh our
                // EOSB if needed.
                // Build out the REST API call query
                std::string strVerb = "POST";
                std::string strApiUri = "/refresh-token";
                std::string strJsonBody = "{\"refresh_token\": \""+ strSailPlatformServicesRefreshToken +"\"}";

                // Send the REST API call to the SAIL Web Api Portal
                std::vector<Byte> stlRestResponse = ::RestApiCall(strSailPlatformServicesIpAddress, (Word) wSailPlatformServicesPortAddress, strVerb, strApiUri, strJsonBody, true);

                // Parse the returning value.
                StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());

                // Did the transaction succeed?
                if ((true == oResponse.IsElementPresent("access_token", ANSI_CHARACTER_STRING_VALUE_TYPE)))
                {
                    // Check to see if we need to update the internal gs_strSailPlatformServicesEosb
                    if (true == oResponse.IsElementPresent("refresh_token", ANSI_CHARACTER_STRING_VALUE_TYPE))
                    {
                        const std::lock_guard<std::mutex> lock(gs_stlMutex);
                        // There is a race condition which exists where someone can call Logout()
                        // while the CheckEosb transaction is running. By the time you get the
                        // result, we might suddenly be no longer logged in. We need to check
                        // before updating the internal EOSB
                        if (true == gs_fIsLoggedOn)
                        {    
                            gs_strSailPlatformServicesAccessToken = oResponse.GetString("access_token");
                            gs_strSailPlatformServicesRefreshToken = oResponse.GetString("refresh_token");
                        }
                        else
                        {
                            // Quick sanity check on global variables
                            __DebugAssert(0 == gs_strSailPlatformServicesRefreshToken.size());
                            __DebugAssert(0 == gs_strSailPlatformServicesAccessToken.size());
                            __DebugAssert(INVALID_HANDLE_VALUE == gs_EosbMaintenanceThread);
                            __DebugAssert(0 == gs_dwEosbMaintenanceThreadIdentifier);
                            // Stop looping
                            fIsLoggedOn = false;
                        }
                    }
                }
                else if ((true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
                {
                    // We are no longer logged on. We need to update the internal global variables
                    // to reflect this.
                    const std::lock_guard<std::mutex> lock(gs_stlMutex);
                    gs_strSailPlatformServicesAccessToken = "";
                    gs_strSailPlatformServicesRefreshToken = "";
                    gs_EosbMaintenanceThread = INVALID_HANDLE_VALUE;
                    gs_dwEosbMaintenanceThreadIdentifier = 0;
                    gs_fIsLoggedOn = false;
                    // Stop looping
                    fIsLoggedOn = false;
                }
                else
                {
                    ::RegisterBaseException(BaseException(__FILE__, __func__, __LINE__, "Unexpected return values from CheckEosb"), __func__, __FILE__, __LINE__);
                }
            }
        }
        while (true == fIsLoggedOn);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return 0;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
extern "C" __declspec(dllexport) bool __stdcall IsLoggedOn(void)
{
    __DebugFunction();

    bool fIsLoggedOn = false;
    const std::lock_guard<std::mutex> lock(gs_stlMutex);
    fIsLoggedOn = gs_fIsLoggedOn;

    return fIsLoggedOn;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
std::string __stdcall GetSailPlatformServicesIpAddress(void)
{
    __DebugFunction();

    const std::lock_guard<std::mutex> lock(gs_stlMutex);
    std::string strSailPlatformServicesIpAddress = gs_strSailPlatformServicesIpAddress;

    return strSailPlatformServicesIpAddress;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
std::string __stdcall GetSailPlatformServicesAccessToken(void)
{
    __DebugFunction();

    const std::lock_guard<std::mutex> lock(gs_stlMutex);
    std::string strSailPlatformServicesAccessToken = gs_strSailPlatformServicesAccessToken;

    return strSailPlatformServicesAccessToken;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
std::string __stdcall GetSailPlatformServicesUserIdentifier(void)
{
    __DebugFunction();

    const std::lock_guard<std::mutex> lock(gs_stlMutex);
    std::string strCurrentUserIdentifier = gs_strCurrentUserIdentifier;

    return strCurrentUserIdentifier;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
std::string __stdcall GetSailPlatformServicesUserOrganizationIdentifier(void)
{
    __DebugFunction();

    const std::lock_guard<std::mutex> lock(gs_stlMutex);
    std::string strCurrentUserOrganizationalIdentifier = gs_strCurrentUserOrganizationalIdentifier;

    return strCurrentUserOrganizationalIdentifier;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
static void __stdcall SetSailPlatformServicesIpAddress(
    _in const std::string & c_strSailPlatformServicesIpAddress
    )
{
    __DebugFunction();

    const std::lock_guard<std::mutex> lock(gs_stlMutex);
    gs_strSailPlatformServicesIpAddress = c_strSailPlatformServicesIpAddress;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_strSailPlatformServicesEosb"></param>
/// <returns></returns>
static void __stdcall SetSailPlatformServicesTokens(
    _in const std::string& c_strSailPlatformServicesAccessToken,
    _in const std::string& c_strSailPlatformServicesRefreshToken
    )
{
    __DebugFunction();

    const std::lock_guard<std::mutex> lock(gs_stlMutex);
    gs_strSailPlatformServicesAccessToken = c_strSailPlatformServicesAccessToken;
    gs_strSailPlatformServicesRefreshToken = c_strSailPlatformServicesRefreshToken;
    // Set global variables
    if ((false == gs_fIsLoggedOn)&&(0 < c_strSailPlatformServicesAccessToken.size()))
    {
        __DebugAssert(INVALID_HANDLE_VALUE == gs_EosbMaintenanceThread);
        __DebugAssert(0 == gs_dwEosbMaintenanceThreadIdentifier);

        // If we were not logged on before, we need to begin a thread
        // which effectively keeps the Access Token fresh
        gs_EosbMaintenanceThread = ::CreateThread(nullptr, 0, (LPTHREAD_START_ROUTINE) AccessTokenMaintenanceThread, nullptr, 0, (DWORD *)  &gs_dwEosbMaintenanceThreadIdentifier);
        _ThrowBaseExceptionIf((INVALID_HANDLE_VALUE == gs_EosbMaintenanceThread), "CreateThread() failed with GetLastError() = %d", ::GetLastError());
        gs_fIsLoggedOn = true;
    }
}

/// <summary>
/// Set the SAIL Web API portal IP address
/// </summary>
/// <param name="c_szIpAddressOfSailWebApiPortal"></param>
/// <returns></returns>
static bool __cdecl SetIpAndPortAddress(
    _in const char * c_szSailPlatformsServicesIpAddress
    )
{
    __DebugFunction();

    bool fSuccess = false;

    try
    {
        if (nullptr != c_szSailPlatformsServicesIpAddress)
        {
            // SetIpAddress() should not succeed if we are already logged on
            _ThrowBaseExceptionIf((true == ::IsLoggedOn()), "Cannot SetIpAddress() while the library is running a live session.", nullptr);
            // Reset the IP settings to the new values
            ::SetSailPlatformServicesIpAddress(::GetNumericalIpAddress(c_szSailPlatformsServicesIpAddress));
            // If we get here, no exception was thrown so the operation was a success
            fSuccess = true;
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return fSuccess;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_strCurrentUserOrganizationIdentifier"></param>
/// <returns></returns>
static void __stdcall SetCurrentUserOrganizationIdentifier(
    _in const std::string & c_strCurrentUserOrganizationIdentifier
    )
{
    __DebugFunction();

    if (true == ::IsLoggedOn())
    {
        const std::lock_guard<std::mutex> lock(gs_stlMutex);
        gs_strCurrentUserOrganizationalIdentifier = c_strCurrentUserOrganizationIdentifier;
    }
}

/// <summary>
/// 
/// </summary>
/// <param name="c_strCurrentUserIdentifier"></param>
/// <returns></returns>
static void __stdcall SetCurrentUserIdentifier(
    _in const std::string & c_strCurrentUserIdentifier
    )
{
    __DebugFunction();

    if (true == ::IsLoggedOn())
    {
        const std::lock_guard<std::mutex> lock(gs_stlMutex);
        gs_strCurrentUserIdentifier = c_strCurrentUserIdentifier;
    }
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl GetIpAddress(void)
{
    __DebugFunction();

    // [DllImport("SailWebApiPortalFunctions.dll", CallingConvention = CallingConvention.Cdecl )]
    // [return: MarshalAs(UnmanagedType.BStr)]
    // static extern public string GetIpAddress();

    std::string strIpAddress = "";

    try
    {
        strIpAddress = ::GetSailPlatformServicesIpAddress();
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return ::ConvertToBSTR(strIpAddress);
}

/// <summary>
/// Logs into SAIL web services and gets an EOSB string. This is cached internally for future use
/// </summary>
/// <param name="c_szUsername"></param>
/// <param name="c_szPAssword"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) bool __cdecl Login(
    _in const char * c_szSailPlatformsServicesIpAddress,
    _in const char * c_szUsername,
    _in const char * c_szPassword
    )
{
    __DebugFunction();

    // [DllImport("SailWebApiPortalFunctions.dll", CallingConvention = CallingConvention.Cdecl )]
    // static extern public bool Login(string username, string password);

    try
    {
        _ThrowBaseExceptionIf((true == ::IsLoggedOn()), "Cannot call Login() when already logged on", nullptr);

        // Establish the target IP address and port address. This function throws if we are currently
        // running an existing session
        ::SetIpAndPortAddress(c_szSailPlatformsServicesIpAddress);

        // Build out the REST API call query
        std::string strVerb = "POST";
        std::string strApiUri = "/login";
        std::string strBody = "grant_type=&username="+ ::UrlEncodeString(std::string(c_szUsername)) +"&password=" + ::UrlEncodeString(std::string(c_szPassword)) + "&scope=&client_id=&client_secret=";
        std::vector<std::string> stlListOfHeaders;
        stlListOfHeaders.push_back("Content-Type: application/x-www-form-urlencoded");

        // Send the REST API call to the SAIL Web Api Portal
        std::vector<Byte> stlRestResponse = ::RestApiCall(gs_strSailPlatformServicesIpAddress, (Word)8000, strVerb, strApiUri, strBody, true, stlListOfHeaders);

        // Parse the returning value.
        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());

        // Did the transaction succeed?
        _ThrowBaseExceptionIf((true != oResponse.IsElementPresent("access_token", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Failed to log in. Invalid Credentials.", nullptr);

        // Make sure to record the EOSB
        ::SetSailPlatformServicesTokens(oResponse.GetString("access_token"), oResponse.GetString("refresh_token"));

        // By default, we automatically get the basic user information since some of those
        // values are useful in other SAIL Web API Portal transactions
        strVerb = "GET";
        strApiUri = "/me";
        stlListOfHeaders.clear();
        stlListOfHeaders.push_back("Authorization: Bearer " + ::GetSailPlatformServicesAccessToken());

        // Send the REST API call to the SAIL Web Api Portal
        stlRestResponse = ::RestApiCall(gs_strSailPlatformServicesIpAddress, (Word)8000, strVerb, strApiUri, strBody, true, stlListOfHeaders);
        
        // Parse the returning value.
        oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());

        // Did the transaction succeed?
        _ThrowBaseExceptionIf((true != oResponse.IsElementPresent("id", ANSI_CHARACTER_STRING_VALUE_TYPE)), "GetBasicUsedInformation() has failed", nullptr);
        _ThrowBaseExceptionIf((true != oResponse.IsElementPresent("organization", INDEXED_BUFFER_VALUE_TYPE)), "GetBasicUsedInformation() has failed", nullptr);

        // Extract all values and cache them in global variables
        ::SetCurrentUserOrganizationIdentifier(oResponse.GetStructuredBuffer("organization").GetString("id"));
        ::SetCurrentUserIdentifier(oResponse.GetString("id"));
        // If we get here, no exceptions were thrown, so the transaction was successfull!!!
        gs_fIsLoggedOn = true;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return gs_fIsLoggedOn;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
extern "C" __declspec(dllexport) bool __cdecl Logout(void)
{
    __DebugFunction();

    // [DllImport("SailWebApiPortalFunctions.dll", CallingConvention = CallingConvention.Cdecl )]
    // static extern public bool Logout();

    bool fSuccess = false;

    try
    {
        // We can only logout if we are logged in

        if (true == ::IsLoggedOn())
        {
            const std::lock_guard<std::mutex> lock(gs_stlMutex);
            gs_strSailPlatformServicesAccessToken = "";
            gs_strSailPlatformServicesRefreshToken = "";
            gs_EosbMaintenanceThread = INVALID_HANDLE_VALUE;
            gs_dwEosbMaintenanceThreadIdentifier = 0;
            gs_fIsLoggedOn = false;
            fSuccess = true;
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return fSuccess;
}
