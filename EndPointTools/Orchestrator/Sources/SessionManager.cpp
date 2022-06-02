/*********************************************************************************************
 *
 * @file SessionManager.cpp
 * @author Luis Miguel Huapaya
 * @date 7 April 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "Chronometer.h"
#include "CurlRest.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "JsonParser.h"
#include "SessionManager.h"
#include "StructuredBuffer.h"

#include <chrono>
#include <iostream>
#include <thread>
#include <vector>

/*********************************************************************************************/

SessionManager::SessionManager(void)
{
    __DebugFunction();
}

/*********************************************************************************************/

SessionManager::~SessionManager(void)
{
    __DebugFunction();
    
    //this->Logout();
}

/********************************************************************************************
 *
 * @class SessionManager
 * @function Login
 * @brief login to the Sail Platform
 * @param[in] c_strEmail (string) Email (i.e. username) used to login
 * @param[in] c_strUserPassword (string) Password used to login
 * @param[in] c_strServerIpAddress (string) Ip address of the Sail Platform Services API portal
 * @param[in] wServerPort (Word) Port number of the Sail Platform Services API portal
 * @return (bool) true if login was successful, false otherwise
 * @return (bool) false if credentials are invalid or any other errors
 * @note
 *     If already logged in, calling Login will override the previous session with this new
 *     session
 *
 ********************************************************************************************/

bool __thiscall SessionManager::Login(
    _in const std::string & c_strEmail,
    _in const std::string & c_strUserPassword,
    _in const std::string & c_strServerIpAddress,
    _in Word wServerPort
    ) throw()
{
    __DebugFunction();
    __DebugAssert(0 < c_strEmail.size());
    __DebugAssert(0 < c_strUserPassword.size());
    __DebugAssert(0 < wServerPort);
    __DebugAssert(0 < c_strServerIpAddress.size());

    bool fSuccess = false;
    
    try
    {
        // Build out the REST API call query
        std::string strVerb = "POST";
        std::string strApiUri = "/login";
        std::string strBody = "grant_type=&username="+ ::UrlEncodeString(c_strEmail) +"&password=" + ::UrlEncodeString(std::string(c_strUserPassword)) + "&scope=&client_id=&client_secret=";
        std::vector<std::string> stlListOfHeaders;
        stlListOfHeaders.push_back("Content-Type: application/x-www-form-urlencoded");

        // Send the REST API call to the SAIL Web Api Portal
        std::vector<Byte> stlRestResponse = ::RestApiCall(c_strServerIpAddress, wServerPort, strVerb, strApiUri, strBody, true, stlListOfHeaders);

        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));
        // Did the transaction succeed?
        _ThrowBaseExceptionIf((true != oResponse.IsElementPresent("access_token", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Failed to log in. Invalid Credentials.", nullptr);

        // Calling SetEosb() will start the update thread automatically
        this->SetSessionParameters(c_strServerIpAddress, wServerPort, oResponse.GetString("access_token"), oResponse.GetString("refresh_token"));
        // If we get here, we were successful
        fSuccess = true;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    return fSuccess;
}

/********************************************************************************************
 *
 * @class SessionManager
 * @function Logout
 * @brief Logout and invalidate the current session
 * @return (void) Nothing
 *
 ********************************************************************************************/

void __thiscall SessionManager::Logout(void) throw()
{
    __DebugFunction();
    
    try
    {
        bool fWasRunning = false;
        // Signal the termination of the SessionManager. We need to be within a lock to
        // do this
        m_oLock.lock();
        fWasRunning = m_fIsRunning;
        m_fIsRunning = false;
        m_oLock.unlock();
        // Only attempt to logout if we were actually running.
        if (true == fWasRunning)
        {
            // Now join the thread (i.e. wait for it to exit properly)
            m_oAccessTokenMaintenanceThread.get()->join();
            // Update member variables to their starting state.
            m_oAccessTokenMaintenanceThread = nullptr;
            m_strAccessToken = "";
            m_strRefreshToken = "";
            m_strServerIpAddress = "";
            m_wServerPortNumber = 0;
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
}

/********************************************************************************************
 *
 * @class SessionManager
 * @function GetServerIpAddress
 * @brief Returns the Sail Platform Services Ip address for the current session
 * @return (string) Ip address of Sail Platform Services Ip address for the current session
 * @return (string) Empty string if there is no current session
 *
 ********************************************************************************************/

std::string __thiscall SessionManager::GetServerIpAddress(void) const throw()
{
    __DebugFunction();

    const std::lock_guard<std::mutex> stlLock(m_oLock);
    std::string strServerIpAddress{m_strServerIpAddress};

    return strServerIpAddress;
}

/********************************************************************************************
 *
 * @class SessionManager
 * @function GetServerPortNumber
 * @brief Returns the Sail Platform Services port number for the current session
 * @return (Word) Port number of the Sail Platform Services for the current session
 * @return (Word) 0 if there is no current session
 *
 ********************************************************************************************/


Word __thiscall SessionManager::GetServerPortNumber(void) const throw()
{
    __DebugFunction();

    const std::lock_guard<std::mutex> stlLock(m_oLock);
    Word wServerPortNumber = m_wServerPortNumber;

    return wServerPortNumber;
}

/********************************************************************************************
 *
 * @class SessionManager
 * @function GetEosb
 * @brief Returns the Sail Platform Services port number for the current session
 * @return (string) Base64 string of the EOSB for a valid session
 * @return (string) Empty string if there is no current session
 *
 ********************************************************************************************/

std::string __thiscall SessionManager::GetAccessToken(void) const throw()
{
    __DebugFunction();

    const std::lock_guard<std::mutex> stlLock(m_oLock);
    std::string strAccessToken{m_strAccessToken};

    return strAccessToken;
}

/********************************************************************************************
 *
 * @class SessionManager
 * @function SetEosb
 * @brief This function allows external code to update the EOSB. This is required since a lot
 *
 * @return (string) Base64 string of the EOSB for a valid session
 * @return (string) Empty string if there is no current session
 *
 ********************************************************************************************/

void __thiscall SessionManager::SetAccessTokens(
    _in const std::string & c_strAccessToken,
    _in const std::string & c_strRefreshToken
    ) throw()
{
    __DebugFunction();

    const std::lock_guard<std::mutex> stlLock(m_oLock);
    // If someone is setting an EOSB, we'd better have a running session, so let's make sure
    if ((true == m_fIsRunning)&&(0 < m_strServerIpAddress.size())&&(0 < m_wServerPortNumber)&&(0 < m_strAccessToken.size())&&(0 < m_strRefreshToken.size()))
    {
        m_strAccessToken = c_strAccessToken;
    }
}

/********************************************************************************************
 *
 * @class SessionManager
 * @function SetSessionParameters
 * @brief Private method used to set all of the session parameters in an atomic fashion
 * @param[in] c_strServerIpAddress (string) Ip address of the Sail Platform Services API portal for the current session
 * @param[in] wServerPort (Word) Port number of the Sail Platform Services API portal for the current session
 * @param[in] c_strEosb (string) EOSB for the current session
 *
 ********************************************************************************************/

void __thiscall SessionManager::SetSessionParameters(
    _in const std::string & c_strServerIpAddress,
    _in Word wServerPortNumber,
    _in const std::string & c_strAccessToken,
    _in const std::string & c_strRefreshToken
    )
{
    __DebugFunction();

    const std::lock_guard<std::mutex> stlLock(m_oLock);
    // Update the EOSB
    m_strServerIpAddress = c_strServerIpAddress;
    m_wServerPortNumber = wServerPortNumber;
    m_strAccessToken = c_strAccessToken;
    m_strRefreshToken = c_strRefreshToken;
    // If the update thread isn't running, start it now after setting the m_strEosb
    if (false == m_fIsRunning)
    {
        // Make sure the state variable is set to true before starting the thread, or else the
        // thread runs a chance of exiting immediately
        m_fIsRunning = true;
        // Start the maintenance thread
        m_oAccessTokenMaintenanceThread = std::unique_ptr<std::thread>(new std::thread(&SessionManager::AccessTokenMaintenanceFunction, this));
    }
}

/********************************************************************************************/

bool __thiscall SessionManager::IsRunning(void) const throw()
{
    __DebugFunction();

    bool fIsRunning = false;

    try
    {
        const std::lock_guard<std::mutex> stlLock(m_oLock);
        fIsRunning = m_fIsRunning;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return fIsRunning;
}

/********************************************************************************************
 *
 * @class SessionManager
 * @function EosbMaintenanceFunction
 * @brief This function runs on it's own thread and continuously spins to maintain the freshness
 *        of the EOSB. This ensures that the EOSB is always fresh, even when an application
 *        goes idle for a while.
 * @note
 *     The function runs on it's own thread until the m_fIsRunning is set to false
 *
 ********************************************************************************************/

void __thiscall SessionManager::AccessTokenMaintenanceFunction(void) throw()
{
    __DebugFunction();

    try
    {
        Chronometer oChronometer;
        // Start the chronometer
        oChronometer.Start();

        do
        {
            bool fIsRunning = false;
            std::string strCurrentAccessToken{};
            std::string strCurrentRefreshToken{};
            std::string strServerIpAddress{};
            Word wServerPortNumber{0};

            // Sleep for 100 milliseconds
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            // Now let's check if we are still running. We do this in an artificially
            // nested scope to protect the mutex in case an exception is thrown
            if (true == this->IsRunning())
            {
                const std::lock_guard<std::mutex> stlLock(m_oLock);
                // Quick reality check that ensures that the session manager didn't fall into
                // a weird state
                __DebugAssert(0 < m_strAccessToken.size());
                __DebugAssert(0 < m_strRefreshToken.size());
                __DebugAssert(0 < m_strServerIpAddress.size());
                __DebugAssert(0 < m_wServerPortNumber);
                // Take an atomic snapshot of the session manager settings
                fIsRunning = true;
                strCurrentAccessToken = m_strAccessToken;
                strCurrentRefreshToken = m_strRefreshToken;
                strServerIpAddress = m_strServerIpAddress;
                wServerPortNumber = m_wServerPortNumber;
            }
            else
            {
                fIsRunning = false;
            }

            // Check to see if 60 seconds has expired on the chronometer. We only care to
            // try and refresh the EOSB once every minute
            if ((true == fIsRunning)&&(60 < oChronometer.GetElapsedTimeWithPrecision(Second)))
            {
                __DebugAssert(0 < strCurrentRefreshToken.size());
                __DebugAssert(0 < strCurrentAccessToken.size());
                __DebugAssert(0 < strServerIpAddress.size());
                __DebugAssert(0 < wServerPortNumber);

                // Reset the chronometer so we can count down another 10 seconds
                oChronometer.Reset();
                oChronometer.Start();
                // We aren't stopping, update the EOSB
                std::string strVerb = "POST";
                std::string strApiUrl = "/refresh-token";
                std::string strJsonBody = "{\"refresh_token\": \""+ strCurrentRefreshToken +"\"}";
                // Make the API call and get REST response
                std::vector<Byte> stlRestResponse = ::RestApiCall(strServerIpAddress, wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
                // Check to make sure the response size isn't 0 before trying to convert it into a StructuredBuffer
                _ThrowBaseExceptionIf((0 == stlRestResponse.size()), "ERROR: Invalid 0 sized response", nullptr);
                // Extract the return parameters
                StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));
                // Make sure the transaction was an actual success and that a new EOSB was provided
                if ((true == oResponse.IsElementPresent("access_token", ANSI_CHARACTER_STRING_VALUE_TYPE)))
                {
                    // Check to see if we need to update the internal gs_strSailPlatformServicesEosb
                    if (true == oResponse.IsElementPresent("refresh_token", ANSI_CHARACTER_STRING_VALUE_TYPE))
                    {
                        this->SetAccessTokens(oResponse.GetString("access_token"), oResponse.GetString("refresh_token"));
                    }
                }
            }
        }
        while (true == this->IsRunning());
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
}
