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
        // Prepare the API call
        std::string strVerb = "POST";
        std::string strApiUrl = "/SAIL/AuthenticationManager/User/Login?Email="+ c_strEmail +"&Password="+ c_strUserPassword;
        std::string strJsonBody = "";
        // Make the API call and get REST response
        std::vector<Byte> stlRestResponse = ::RestApiCall(c_strServerIpAddress, wServerPort, strVerb, strApiUrl, strJsonBody, true);
        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));
        // Did the call succeed?
        _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Error logging in.", nullptr);
        // If the call succeeded, let's make sure that the format of the return value is correct
        _ThrowBaseExceptionIf((false == oResponse.IsElementPresent("Eosb", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID FORMAT. Invalid return value, missing 'Eosb'", nullptr);
        // Calling SetEosb() will start the update thread automatically
        this->SetSessionParameters(c_strServerIpAddress, wServerPort, oResponse.GetString("Eosb"));
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
            m_oEosbMaintenanceThread.get()->join();
            // Update member variables to their starting state.
            m_oEosbMaintenanceThread = nullptr;
            m_strEosb = "";
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
    
    const std::lock_guard<std::mutex> lock(m_oLock);
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
    
    const std::lock_guard<std::mutex> lock(m_oLock);
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

std::string __thiscall SessionManager::GetEosb(void) const throw()
{
    __DebugFunction();
    
    const std::lock_guard<std::mutex> lock(m_oLock);
    std::string strEosb{m_strEosb};
    
    return strEosb;
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

void __thiscall SessionManager::SetEosb(
    _in const std::string & c_strEosb
    ) throw()
{
    __DebugFunction();
    
    const std::lock_guard<std::mutex> lock(m_oLock);
    // If someone is setting an EOSB, we'd better have a running session, so let's make sure
    if ((true == m_fIsRunning)&&(0 < m_strServerIpAddress.size())&&(0 < m_wServerPortNumber)&&(0 < m_strEosb.size()))
    {
        m_strEosb = c_strEosb;
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
    _in const std::string & c_strEosb
    )
{
    __DebugFunction();
    
    const std::lock_guard<std::mutex> lock(m_oLock);
    // Update the EOSB
    m_strServerIpAddress = c_strServerIpAddress;
    m_wServerPortNumber = wServerPortNumber;
    m_strEosb = c_strEosb;
    // If the update thread isn't running, start it now after setting the m_strEosb
    if (false == m_fIsRunning)
    {
        // Make sure the state variable is set to true before starting the thread, or else the
        // thread runs a chance of exiting immediately
        m_fIsRunning = true;
        // Start the maintenance thread
        m_oEosbMaintenanceThread = std::unique_ptr<std::thread>(new std::thread(&SessionManager::EosbMaintenanceFunction, this));
    }
}

/********************************************************************************************/

bool __thiscall SessionManager::IsRunning(void) const throw()
{
    __DebugFunction();
    
    bool fIsRunning = false;
    
    try
    {
        const std::lock_guard<std::mutex> lock(m_oLock);
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

void __thiscall SessionManager::EosbMaintenanceFunction(void) throw()
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
            std::string strCurrentEosb{};
            std::string strServerIpAddress{};
            Word wServerPortNumber{0};
            
            // Sleep for 100 milliseconds
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            // Now let's check if we are still running. We do this in an artificially
            // nested scope to protect the mutex in case an exception is thrown
            if (true == this->IsRunning())
            {
                const std::lock_guard<std::mutex> lock(m_oLock);
                // Quick reality check that ensures that the session manager didn't fall into
                // a weird state
                __DebugAssert(0 < m_strEosb.size());
                __DebugAssert(0 < m_strServerIpAddress.size());
                __DebugAssert(0 < m_wServerPortNumber);
                // Take an atomic snapshot of the session manager settings
                fIsRunning = true;
                strCurrentEosb = m_strEosb;
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
                __DebugAssert(0 < strCurrentEosb.size());
                __DebugAssert(0 < strServerIpAddress.size());
                __DebugAssert(0 < wServerPortNumber);
                    
                // Reset the chronometer so we can count down another 10 seconds
                oChronometer.Reset();
                oChronometer.Start();
                // We aren't stopping, update the EOSB
                std::string strVerb = "GET";
                std::string strApiUrl = "/SAIL/AuthenticationManager/CheckEosb?Eosb=" + strCurrentEosb;
                std::string strJsonBody = "";
                // Make the API call and get REST response
                std::vector<Byte> stlRestResponse = ::RestApiCall(strServerIpAddress, wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
                // Check to make sure the response size isn't 0 before trying to convert it into a StructuredBuffer
                _ThrowBaseExceptionIf((0 == stlRestResponse.size()), "ERROR: Invalid 0 sized response", nullptr);
                // Extract the return parameters
                StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));
                // Make sure the transaction was an actual success and that a new EOSB was provided
                if ((200 == oResponse.GetFloat64("Status"))&&(true == oResponse.IsElementPresent("Eosb", ANSI_CHARACTER_STRING_VALUE_TYPE)))
                {
                    this->SetEosb(oResponse.GetString("Eosb"));
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
