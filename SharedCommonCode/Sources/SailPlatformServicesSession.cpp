/*********************************************************************************************
 *
 * @file SailPlatformServicesSession.cpp
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
#include "SailPlatformServicesSession.h"
#include "StructuredBuffer.h"

#include <chrono>
#include <iostream>
#include <thread>
#include <vector>

/*********************************************************************************************/

SailPlatformServicesSession::SailPlatformServicesSession(
    _in const std::string & c_strServerIpAddress,
    _in Word wServerPortNumber
    )
{
    __DebugFunction();
    
    m_strServerIpAddress = c_strServerIpAddress;
    m_wServerPortNumber = wServerPortNumber;
}

/*********************************************************************************************/

SailPlatformServicesSession::~SailPlatformServicesSession(void)
{
    __DebugFunction();
    
    this->Logout();
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function GetServerIpAddress
 * @brief Returns the Sail Platform Services Ip address for the current session
 * @return (string) Ip address of Sail Platform Services Ip address for the current session
 * @return (string) Empty string if there is no current session
 *
 ********************************************************************************************/

std::string __thiscall SailPlatformServicesSession::GetServerIpAddress(void) const throw()
{
    __DebugFunction();
    
    const std::lock_guard<std::mutex> stlLock(m_oLock);
    std::string strServerIpAddress{m_strServerIpAddress};
    
    return strServerIpAddress;
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function GetServerPortNumber
 * @brief Returns the Sail Platform Services port number for the current session
 * @return (Word) Port number of the Sail Platform Services for the current session
 * @return (Word) 0 if there is no current session
 *
 ********************************************************************************************/


Word __thiscall SailPlatformServicesSession::GetServerPortNumber(void) const throw()
{
    __DebugFunction();
    
    const std::lock_guard<std::mutex> stlLock(m_oLock);
    Word wServerPortNumber = m_wServerPortNumber;
    
    return wServerPortNumber;
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function GetEosb
 * @brief Returns the Sail Platform Services port number for the current session
 * @return (string) Base64 string of the EOSB for a valid session
 * @return (string) Empty string if there is no current session
 *
 ********************************************************************************************/

std::string __thiscall SailPlatformServicesSession::GetEosb(void) const throw()
{
    __DebugFunction();
    
    const std::lock_guard<std::mutex> stlLock(m_oLock);
    std::string strEosb{m_strEosb};
    
    return strEosb;
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function SetEosb
 * @brief This function allows external code to update the EOSB. This is required since a lot
 *        
 * @return (string) Base64 string of the EOSB for a valid session
 * @return (string) Empty string if there is no current session
 *
 ********************************************************************************************/

void __thiscall SailPlatformServicesSession::SetEosb(
    _in const std::string & c_strEosb
    ) throw()
{
    __DebugFunction();
    
    const std::lock_guard<std::mutex> stlLock(m_oLock);
    // If someone is setting an EOSB, we'd better have a running session, so let's make sure
    if ((true == m_fIsRunning)&&(0 < m_strServerIpAddress.size())&&(0 < m_wServerPortNumber)&&(0 < m_strEosb.size()))
    {
        m_strEosb = c_strEosb;
    }
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function RegisterOrganization
 * @brief Method used to register a new organization and its default administrator
 * @return (void) Nothing
 * @param[in] c_oRegistrationInformation (StructuredBuffer) Registration parameters
 *
 ********************************************************************************************/
 
void __thiscall SailPlatformServicesSession::RegisterOrganization(
    _in const StructuredBuffer & c_oRegistrationParameters
    )
{
    __DebugFunction();
    
    // Get the ip address and port number
    std::string strServerIpAddress = this->GetServerIpAddress();
    Word wServerPortNumber = this->GetServerPortNumber();
    // Prepare the API call
    std::string strVerb = "POST";
    std::string strApiUrl = "/SAIL/AccountManager/RegisterUser";
    std::string strJsonBody = ::ConvertStructuredBufferToJson(c_oRegistrationParameters);
    // Make the API call and get REST response
    std::vector<Byte> stlRestResponse = ::RestApiCall(strServerIpAddress, wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
    StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));
    // Did the call succeed?
    _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Error registering new organization and super user.", nullptr);
    _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("RootEventStatus")), "Error registering root event for the organization.", nullptr);
}
       
/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function Login
 * @brief login to the Sail Platform
 * @param[in] c_strEmail (string) Email (i.e. username) used to login
 * @param[in] c_strUserPassword (string) Password used to login
 * @return (void) Nothing
 * @note
 *     If already logged in, calling Login will override the previous session with this new
 *     session
 *
 ********************************************************************************************/

void __thiscall SailPlatformServicesSession::Login(
    _in const std::string & c_strEmail,
    _in const std::string & c_strUserPassword
    )
{
    __DebugFunction();
    __DebugAssert(0 < c_strEmail.size());
    __DebugAssert(0 < c_strUserPassword.size());

    // Get the ip address and port number
    std::string strServerIpAddress = this->GetServerIpAddress();
    Word wServerPortNumber = this->GetServerPortNumber();
    // Prepare the API call
    std::string strVerb = "POST";
    std::string strApiUrl = "/SAIL/AuthenticationManager/User/Login?Email="+ c_strEmail +"&Password="+ c_strUserPassword;
    std::string strJsonBody = "";
    // Make the API call and get REST response
    std::vector<Byte> stlRestResponse = ::RestApiCall(strServerIpAddress, wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
    StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));
    // Did the call succeed?
    _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Error logging in.", nullptr);
    // If the call succeeded, let's make sure that the format of the return value is correct
    _ThrowBaseExceptionIf((false == oResponse.IsElementPresent("Eosb", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID FORMAT. Invalid return value, missing 'Eosb'", nullptr);
    // Calling SetEosb() will start the update thread automatically
    this->StartSession(oResponse.GetString("Eosb"));
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function Logout
 * @brief Logout and invalidate the current session
 * @return (void) Nothing
 *
 ********************************************************************************************/

void __thiscall SailPlatformServicesSession::Logout(void) throw()
{
    __DebugFunction();
    
    try
    {
        bool fWasRunning = false;
        // Signal the termination of the SailPlatformServicesSession. We need to be within a lock to
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
 * @class SailPlatformServicesSession
 * @function GetBasicUserInformation
 * @brief Method used to fetch user information
 * @param[in] c_oRegistrationParameters (StructuredBuffer) Registration parameters
 *
 ********************************************************************************************/
 
StructuredBuffer __thiscall SailPlatformServicesSession::GetBasicUserInformation(void)
{
    __DebugFunction();
    _ThrowBaseExceptionIf((false == this->IsRunning()), "ERROR: Cannot get basic user information before logging in.", nullptr);
    
    // Get the ip address and port number
    std::string strServerIpAddress = this->GetServerIpAddress();
    Word wServerPortNumber = this->GetServerPortNumber();
    std::string strEosb = this->GetEosb();
    // Prepare the API call
    std::string strVerb = "GET";
    std::string strApiUrl = "/SAIL/AuthenticationManager/GetBasicUserInformation?Eosb=" + strEosb;
    std::string strJsonBody = "";
    // Make the API call and get REST response
    std::vector<Byte> stlRestResponse = ::RestApiCall(strServerIpAddress, wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
    StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
    // Did the call succeed?
    _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "Error getting basic user information.", nullptr);
    
    return StructuredBuffer(oResponse);
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function RegisterUser
 * @brief Method used to register a new user. Must be called by an administrator
 * @param[in] c_oRegistrationParameters (StructuredBuffer) Registration parameters
 *
 ********************************************************************************************/
 
void __thiscall SailPlatformServicesSession::RegisterUser(
    _in const StructuredBuffer & c_oRegistrationParameters
    )
{
    __DebugFunction();
    _ThrowBaseExceptionIf((false == this->IsRunning()), "ERROR: Cannot register dataset before logging in.", nullptr);
    
    // Get the ip address and port number
    std::string strServerIpAddress = this->GetServerIpAddress();
    Word wServerPortNumber = this->GetServerPortNumber();
    std::string strEosb = this->GetEosb();
    // Prepare the API call
    std::string strVerb = "POST";
    std::string strApiUrl = "/SAIL/AccountManager/Admin/RegisterUser?Eosb=" + strEosb;
    std::string strJsonBody = ::ConvertStructuredBufferToJson(c_oRegistrationParameters);
    // Make the API call and get REST response
    std::vector<Byte> stlRestResponse = ::RestApiCall(strServerIpAddress, wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
    StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
    // Did the call succeed?
    _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Error registering new user.", nullptr);
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function RegisterDatasetFamily
 * @brief Method used to register a dataset family
 * @param[in] c_oRegistrationParameters (StructuredBuffer) Registration parameters
 *
 ********************************************************************************************/

std::string __thiscall SailPlatformServicesSession::RegisterDatasetFamily(
    _in const StructuredBuffer & c_oRegistrationParameters
    )
{
    __DebugFunction();
    _ThrowBaseExceptionIf((false == this->IsRunning()), "ERROR: Cannot register dataset before logging in.", nullptr);
    
    // Get the ip address and port number
    std::string strServerIpAddress = this->GetServerIpAddress();
    Word wServerPortNumber = this->GetServerPortNumber();
    std::string strEosb = this->GetEosb();
    // Prepare the API call
    std::string strVerb = "POST";
    std::string strApiUrl = "/SAIL/DatasetFamilyManager/RegisterDatasetFamily?Eosb=" + strEosb;
    std::string strJsonBody = ::ConvertStructuredBufferToJson(c_oRegistrationParameters);
    // Make the API call and get REST response
    std::vector<Byte> stlRestResponse = ::RestApiCall(strServerIpAddress, wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
    StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
    // Did the call succeed?
    _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Error registering new dataset family.", nullptr);
    _ThrowBaseExceptionIf((false == oResponse.IsElementPresent("DatasetFamilyIdentifier", ANSI_CHARACTER_STRING_VALUE_TYPE)), "ERROR: Missing return value of 'DatasetFamilyIdentifier'.", nullptr);
    
    return oResponse.GetString("DatasetFamilyIdentifier");
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function RegisterDataset
 * @brief Method used to register a new dataset
 * @param[in] c_oRegistrationParameters (StructuredBuffer) Registration parameters
 *
 ********************************************************************************************/
 
void __thiscall SailPlatformServicesSession::RegisterDataset(
    _in const Guid & c_oDatasetIdentifier,
    _in const StructuredBuffer & c_oDatasetMetadata
    )
{
    __DebugFunction();
    _ThrowBaseExceptionIf((false == this->IsRunning()), "ERROR: Cannot register dataset before logging in.", nullptr);
    
    // Get the ip address and port number
    std::string strServerIpAddress = this->GetServerIpAddress();
    Word wServerPortNumber = this->GetServerPortNumber();
    std::string strEosb = this->GetEosb();
    // Build the API call
    StructuredBuffer oRequestBody;
    oRequestBody.PutString("DatasetGuid", c_oDatasetIdentifier.ToString(eHyphensOnly));
    StructuredBuffer oDatasetMetadataToRegister;
    oDatasetMetadataToRegister.PutString("VersionNumber", "0.1.0");
    oDatasetMetadataToRegister.PutString("DatasetName", c_oDatasetMetadata.GetString("Title"));
    oDatasetMetadataToRegister.PutString("Description", c_oDatasetMetadata.GetString("Description"));
    oDatasetMetadataToRegister.PutString("Keywords", c_oDatasetMetadata.GetString("Tags"));
    oDatasetMetadataToRegister.PutUnsignedInt64("PublishDate", c_oDatasetMetadata.GetUnsignedInt64("PublishDate"));
    oDatasetMetadataToRegister.PutByte("PrivacyLevel", 1);
    oDatasetMetadataToRegister.PutString("JurisdictionalLimitations", "N/A");
    oDatasetMetadataToRegister.PutStructuredBuffer("Tables", c_oDatasetMetadata.GetStructuredBuffer("Tables"));
    oRequestBody.PutStructuredBuffer("DatasetData", oDatasetMetadataToRegister);
    // Prepare the API call
    std::string strVerb = "POST";
    std::string strApiUrl = "/SAIL/DatasetManager/RegisterDataset?Eosb=" + strEosb;
    std::string strJsonBody = ::ConvertStructuredBufferToJson(oRequestBody);
    // Make the API call and get REST response
    std::vector<Byte> stlRestResponse = ::RestApiCall(strServerIpAddress, wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
    StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
    // Did the call succeed?
    _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Error registering dataset.", nullptr);
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function ApplyForDigitalContract
 * @brief Method used by a researcher to apply for a digital contract
 * @param[in] c_oRegistrationParameters (StructuredBuffer) Registration parameters
 *
 ********************************************************************************************/
 
std::string __thiscall SailPlatformServicesSession::ApplyForDigitalContract(
    _in const StructuredBuffer & c_oRegistrationParameters
    )
{
    __DebugFunction();
    _ThrowBaseExceptionIf((false == this->IsRunning()), "ERROR: Cannot register dataset before logging in.", nullptr);
    
    // Get the ip address and port number
    std::string strServerIpAddress = this->GetServerIpAddress();
    Word wServerPortNumber = this->GetServerPortNumber();
    std::string strEosb = this->GetEosb();
    // Prepare the API call
    std::string strVerb = "POST";
    std::string strApiUrl = "/SAIL/DigitalContractManager/Applications?Eosb=" + strEosb;
    std::string strJsonBody = ::ConvertStructuredBufferToJson(c_oRegistrationParameters);
    // Make the API call and get REST response
    std::vector<Byte> stlRestResponse = ::RestApiCall(strServerIpAddress, wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
    StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
    // Did the call succeed?
    _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Error applying for a new digital contract.", nullptr);
    _ThrowBaseExceptionIf((false == oResponse.IsElementPresent("DigitalContractIdentifier", ANSI_CHARACTER_STRING_VALUE_TYPE)), "ERROR: Digital Contract Identifier missing from response", nullptr);
    
    return oResponse.GetString("DigitalContractIdentifier");
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function ApproveDigitalContract
 * @brief Method used by a data owner to approve a digital contract application
 * @param[in] c_oRegistrationParameters (StructuredBuffer) Registration parameters
 *
 ********************************************************************************************/
 
void __thiscall SailPlatformServicesSession::ApproveDigitalContract(
    _in const StructuredBuffer & c_oRegistrationParameters
    )
{
    __DebugFunction();
    _ThrowBaseExceptionIf((false == this->IsRunning()), "ERROR: Cannot approve a dataset before logging in.", nullptr);
    
    // Get the ip address and port number
    std::string strServerIpAddress = this->GetServerIpAddress();
    Word wServerPortNumber = this->GetServerPortNumber();
    std::string strEosb = this->GetEosb();
    // Prepare the API call
    std::string strVerb = "PATCH";
    std::string strApiUrl = "/SAIL/DigitalContractManager/DataOwner/Accept?Eosb=" + strEosb;
    std::string strJsonBody = ::ConvertStructuredBufferToJson(c_oRegistrationParameters);
    // Make the API call and get REST response
    std::vector<Byte> stlRestResponse = ::RestApiCall(strServerIpAddress, wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
    StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
    // Did the call succeed?
    _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "Error approving digital contract.", nullptr);
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function ActivateDigitalContract
 * @brief Method used by a researcher to activate a digital contract
 * @param[in] c_oRegistrationParameters (StructuredBuffer) Registration parameters
 *
 ********************************************************************************************/
 
void __thiscall SailPlatformServicesSession::ActivateDigitalContract(
    _in const StructuredBuffer & c_oRegistrationParameters
    )
{
    __DebugFunction();
    _ThrowBaseExceptionIf((false == this->IsRunning()), "ERROR: Cannot activate a dataset before logging in.", nullptr);
    
    // Get the ip address and port number
    std::string strServerIpAddress = this->GetServerIpAddress();
    Word wServerPortNumber = this->GetServerPortNumber();
    std::string strEosb = this->GetEosb();
    // Prepare the API call
    std::string strVerb = "PATCH";
    std::string strApiUrl = "/SAIL/DigitalContractManager/Researcher/Activate?Eosb=" + strEosb;
    std::string strJsonBody = ::ConvertStructuredBufferToJson(c_oRegistrationParameters);
    // Make the API call and get REST response
    std::vector<Byte> stlRestResponse = ::RestApiCall(strServerIpAddress, wServerPortNumber, strVerb, strApiUrl, strJsonBody, true);
    StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
    // Did the call succeed?
    _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "Error approving digital contract.", nullptr);
}

/********************************************************************************************
 *
 * @class SailPlatformServicesSession
 * @function StartSession
 * @brief Private method used to start a running session
 * @param[in] c_strEosb (string) EOSB for the current session
 *
 ********************************************************************************************/

void __thiscall SailPlatformServicesSession::StartSession(
    _in const std::string & c_strEosb
    )
{
    __DebugFunction();
    
    const std::lock_guard<std::mutex> stlLock(m_oLock);
    // Update the EOSB
    m_strEosb = c_strEosb;
    // If the update thread isn't running, start it now after setting the m_strEosb
    if (false == m_fIsRunning)
    {
        // Make sure the state variable is set to true before starting the thread, or else the
        // thread runs a chance of exiting immediately
        m_fIsRunning = true;
        // Start the maintenance thread
        m_oEosbMaintenanceThread = std::unique_ptr<std::thread>(new std::thread(&SailPlatformServicesSession::EosbMaintenanceFunction, this));
    }
}

/********************************************************************************************/

bool __thiscall SailPlatformServicesSession::IsRunning(void) const throw()
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
 * @class SailPlatformServicesSession
 * @function EosbMaintenanceFunction
 * @brief This function runs on it's own thread and continuously spins to maintain the freshness
 *        of the EOSB. This ensures that the EOSB is always fresh, even when an application
 *        goes idle for a while.
 * @note
 *     The function runs on it's own thread until the m_fIsRunning is set to false
 *
 ********************************************************************************************/

void __thiscall SailPlatformServicesSession::EosbMaintenanceFunction(void) throw()
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
                const std::lock_guard<std::mutex> stlLock(m_oLock);
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
