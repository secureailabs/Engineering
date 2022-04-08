/*********************************************************************************************
 *
 * @file SessionManager.cpp
 * @author Luis Miguel Huapaya
 * @date 7 April 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "CurlRest.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "JsonParser.h"
#include "SessionManager.h"
#include "StructuredBuffer.h"

#include <iostream>
#include <vector>

/*********************************************************************************************/

static bool __stdcall CheckEosb(
    _in const std::string & c_strEosb,
    _in const std::string & c_strServerIpAddress,
    _in Word wServerPort
    ) throw()
{
    __DebugFunction();

    bool fSuccess = false;
    
    try
    {
        std::string strVerb = "GET";
        std::string strApiUri = "/SAIL/AuthenticationManager/CheckEosb?Eosb=" + c_strEosb;
        std::string strJsonBody = "";
        // Send the REST API call to the SAIL Web Api Portal
        std::vector<Byte> stlRestResponse = ::RestApiCall(c_strServerIpAddress, (Word) wServerPort, strVerb, strApiUri, strJsonBody, true);
        // Parse the returning value.
        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
        // Did the transaction succeed?
        if ((true == oResponse.IsElementPresent("Status", FLOAT64_VALUE_TYPE))&&(200 == oResponse.GetFloat64("Status")))
        {
            // Check to see if we need to update the internal gs_strSailPlatformServicesEosb
            if (true == oResponse.IsElementPresent("Eosb", ANSI_CHARACTER_STRING_VALUE_TYPE))
            {
                std::cout << "bool __stdcall CheckEosb()" << std::endl;
                std::cout << oResponse.GetString("Eosb") << std::endl;
                fSuccess = true;
            }
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
    
    return fSuccess;
}

/*********************************************************************************************/

SessionManager::SessionManager(void)
{
    __DebugFunction();
}

/*********************************************************************************************/

SessionManager::~SessionManager(void)
{
    __DebugFunction();
    
    this->Logout();
}

/*********************************************************************************************/

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
        std::cout << "JSON = " << (char *) stlRestResponse.data() << std::endl;
        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));
        // Did the call succeed?
        _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Error logging in.", nullptr);
        // If the call succeeded, let's make sure that the format of the return value is correct
        _ThrowBaseExceptionIf((false == oResponse.IsElementPresent("Eosb", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID FORMAT. Invalid return value, missing 'Eosb'", nullptr);
        // Calling SetEosb() will start the update thread automatically
        std::cout << oResponse.ToString() << std::endl;
        this->SetSessionParameters(c_strServerIpAddress, wServerPort, oResponse.GetString("Eosb"));
        // If we get here, we were successful
        fSuccess = ::CheckEosb(oResponse.GetString("Eosb"), c_strServerIpAddress, wServerPort);
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

/*********************************************************************************************/

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
            // Update member variables to their starting state
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

/*********************************************************************************************/

std::string __thiscall SessionManager::GetServerIpAddress(void) const throw()
{
    __DebugFunction();
    
    std::unique_lock<std::mutex> oMutexLock(m_oLock);
    std::string strServerIpAddress{m_strServerIpAddress};
    
    return strServerIpAddress;
}

/*********************************************************************************************/

Word __thiscall SessionManager::GetServerPortNumber(void) const throw()
{
    __DebugFunction();
    
    std::unique_lock<std::mutex> oMutexLock(m_oLock);
    Word wServerPortNumber = m_wServerPortNumber;
    
    return wServerPortNumber;
}

/*********************************************************************************************/

std::string __thiscall SessionManager::GetEosb(void) const throw()
{
    __DebugFunction();
    
    std::unique_lock<std::mutex> oMutexLock(m_oLock);
    std::string strEosb{m_strEosb};
    
    return strEosb;
}

/*********************************************************************************************/

void __thiscall SessionManager::SetEosb(
    _in const std::string & c_strEosb
    ) throw()
{
    __DebugFunction();
    
    std::unique_lock<std::mutex> oMutexLock(m_oLock);
    m_strEosb = c_strEosb;
}

/*********************************************************************************************/

void __thiscall SessionManager::SetSessionParameters(
    _in const std::string & c_strServerIpAddress,
    _in Word wServerPortNumber,
    _in const std::string & c_strEosb
    )
{
    __DebugFunction();
    
    std::unique_lock<std::mutex> oMutexLock(m_oLock);
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
            
/*********************************************************************************************/

void __thiscall SessionManager::EosbMaintenanceFunction(void) throw()
{
    __DebugFunction();
    
    try
    {
        bool fIsRunning;
        
        do
        {
            using namespace std::literals;
            std::unique_lock<std::mutex> oMutexLock(m_oLock);
            // Wait no more than 1 minute to check the EOSB
            m_oTimedWait.wait_for(oMutexLock, 1min, [&] { return !m_fIsRunning; });
            if (true == m_fIsRunning)
            {
                // We aren't stopping, update the EOSB
                std::string strVerb = "GET";
                std::string strApiUrl = "/SAIL/AuthenticationManager/CheckEosb?Eosb=" + m_strEosb;
                std::string strJsonBody = "";
                // Make the API call and get REST response
                std::vector<Byte> stlRestResponse = ::RestApiCall(m_strServerIpAddress, m_wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
                // Check to make sure the response size isn't 0 before trying to convert it into a StructuredBuffer
                _ThrowBaseExceptionIf((0 == stlRestResponse.size()), "ERROR: Invalid 0 sized response", nullptr);
                // Extract the return parameters
                StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));
                // Make sure the transaction was an actual success
                _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "ERROR: Failed to get an Eosb update", nullptr);
                // Update the internal EOSB
                m_strEosb = oResponse.GetString("Eosb");
                // Make sure we continue looping
                fIsRunning = true;
            }
        }
        while (true == fIsRunning);
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
