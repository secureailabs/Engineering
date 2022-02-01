/*********************************************************************************************
 *
 * @file Orchestrator.cpp
 * @author David Gascon & Jingwei Zhang
 * @date 15 Jan 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Class used for single job related issues
 *
 ********************************************************************************************/

#include "JsonParser.h"
#include "Orchestrator.h"
#include "StructuredBuffer.h"
#include "SocketClient.h"
#include "TlsClient.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "TlsTransactionHelperFunctions.h"
#include "HttpRequestParser.h"
#include "CurlRest.h"
#include "JsonValue.h"
#include "FileUtils.h"
#include <exception>
#include <iostream>
#include <fstream>
#include <set>
#include <vector>
#include <cstdlib>
#include <iterator>
#include <filesystem>
#include <chrono>
#include <thread>
#include <utility>

constexpr Word REMOTE_JOB_PORT{3500};

/********************************************************************************************
 *
 * @function GetJsonForStructuredBuffer
 * @brief Helper function to create a JSON str out of a StructuredBuffer
 * @param [in] StructuredBuffer - The StructuredBuffer to convert to a string
 * @return std::string - The JSON representation of the map, or "" on error
 *
 ********************************************************************************************/
std::string __stdcall GetJsonForStructuredBuffer(
    _in const StructuredBuffer& c_oStructuredBuffer
    )
{
    std::string strJSON{""};
    JsonValue* oJsonValue{nullptr};
    try
    {
        oJsonValue = JsonValue::ParseStructuredBufferToJson(c_oStructuredBuffer);
        strJSON = oJsonValue->ToString();
    }
    catch(const BaseException& oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
        strJSON.clear();
    }
    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        strJSON.clear();
    }

    if ( nullptr != oJsonValue )
    {
        oJsonValue->Release();
        oJsonValue = nullptr;
    }

    return strJSON;
}

/********************************************************************************************
 *
 * @function GetJsonForStructuredBufferMap
 * @brief Helper function to create a JSON str out of a map of GUID:StructuredBuffer pairs
 * @param [in] std::unordered_map - The map containg the GUID:StructuredBuffer pairs
 * @return std::string - The JSON representation of the map, or "" on error
 *
 ********************************************************************************************/
static std::string __stdcall GetJsonForStructuredBufferMap(
    _in const std::unordered_map<std::string, StructuredBuffer>& stlStructuredBufferMap
)
{
    __DebugFunction();

    std::string strJSON{""};
    try
    {
        StructuredBuffer oBufferWithAllObjects;
        for ( const auto& oStructuredBufferItr : stlStructuredBufferMap )
        {
            Guid oEntryGuid(oStructuredBufferItr.first);
            oBufferWithAllObjects.PutStructuredBuffer(oEntryGuid.ToString(eHyphensAndCurlyBraces).c_str(), oStructuredBufferItr.second);
        }

        if ( 0 < oBufferWithAllObjects.GetNamesOfElements().size() )
        {
            strJSON = GetJsonForStructuredBuffer(oBufferWithAllObjects);
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
        strJSON.clear();
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        strJSON.clear();
    }

    return strJSON;
}

/********************************************************************************************
 *
 * @function GetJsonForStructuredBufferMap
 * @brief Helper function to create a JSON str out of a map that has a string as the first item,
 *        and a TableInformation
 * @param [in] std::unordered_map - The map containg the GUID:pair<Something,StructuredBuffer>
 *                                  pairs
 * @return std::string - The JSON representation of the map, or "" on error
 *
 ********************************************************************************************/
static std::string __stdcall GetJsonForStructuredBufferMap(
    _in const std::unordered_map<std::string, TableInformation>& stlStructuredBufferMap
)
{
    __DebugFunction();

    std::string strJSON{""};
    try
    {
        StructuredBuffer oBufferWithAllObjects;
        for ( const auto& oStructuredBufferItr : stlStructuredBufferMap )
        {
            oBufferWithAllObjects.PutStructuredBuffer(oStructuredBufferItr.first.c_str(),
                oStructuredBufferItr.second.m_oInformation);
        }

        if ( 0 < oBufferWithAllObjects.GetNamesOfElements().size() )
        {
            strJSON = GetJsonForStructuredBuffer(oBufferWithAllObjects);
        }
    }
    catch(const BaseException& oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
        strJSON.clear();
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        strJSON.clear();
    }

    return strJSON;
}
/********************************************************************************************
 *
 * @class Orchestrator
 * @function Default constructor
 *
 ********************************************************************************************/
Orchestrator::Orchestrator(void)
{
    __DebugFunction();
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function Destructor
 *
 ********************************************************************************************/
Orchestrator::~Orchestrator(void)
{
    __DebugFunction();
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function CacheDigitalContractsFromRemote
 * @brief Call to our remote server to get all our digital contracts, and cached their SBs
 *        in a class member map
 *
 ********************************************************************************************/
void __thiscall Orchestrator::CacheDigitalContractsFromRemote(
    _in const std::string& c_strServerIpAddress,
    _in unsigned long unServerPort
    )
{
    __DebugFunction();
    __DebugAssert(unServerPort < 65536);

    try
    {
        std::string strApiUrl = "/SAIL/DigitalContractManager/DigitalContracts?Eosb=" + m_oEosbRotator.GetEosb();
        std::vector<Byte> stlRestResponse = ::RestApiCall(c_strServerIpAddress, unServerPort, "GET", strApiUrl, "", true);
        std::string strUnescapedResponse = ::UnEscapeJsonString((const char *) stlRestResponse.data());
        StructuredBuffer oDigitalContractResponse(JsonValue::ParseDataToStructuredBuffer(strUnescapedResponse.c_str()));
        _ThrowBaseExceptionIf((200 != oDigitalContractResponse.GetFloat64("Status")), "Failed to retrieve digital contracts", nullptr);

        if ( oDigitalContractResponse.IsElementPresent("Eosb", ANSI_CHARACTER_STRING_VALUE_TYPE) )
        {
            m_oEosbRotator.SetEosb(oDigitalContractResponse.GetString("Eosb"));
        }

        StructuredBuffer oDigitalContracts = oDigitalContractResponse.GetStructuredBuffer("DigitalContracts");
        for (const std::string& strDcGuid : oDigitalContracts.GetNamesOfElements())
        {
            StructuredBuffer oDigitalContractRecord = oDigitalContracts.GetStructuredBuffer(strDcGuid.c_str());
            m_stlDigitalContracts.insert({strDcGuid, oDigitalContractRecord});
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
        m_stlDigitalContracts.clear();
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        m_stlDigitalContracts.clear();
    }
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function CacheDatasetsFromRemote
 * @brief Call to our remote server to get all our datasets, and cached their SBs
 *        in a class member map
 *
 ********************************************************************************************/
void Orchestrator::CacheDatasetsFromRemote(
    _in const std::string& c_strServerIpAddress,
    _in unsigned long unServerPort
    )
{
    __DebugFunction();
    __DebugAssert(unServerPort < 65536);

    try
    {
        std::string strApiUrl = "/SAIL/DatasetManager/ListDatasets?Eosb=" + m_oEosbRotator.GetEosb();
        StructuredBuffer oDatasetRequest;
        std::vector<Byte> stlRestResponse = ::RestApiCall(c_strServerIpAddress, unServerPort, "GET", strApiUrl, "", true);
        std::string strUnescapedResponse = ::UnEscapeJsonString((const char *)stlRestResponse.data());
        StructuredBuffer oDatasetResponse(JsonValue::ParseDataToStructuredBuffer(strUnescapedResponse.c_str()));
        _ThrowBaseExceptionIf((200 != oDatasetResponse.GetFloat64("Status")), "Failed to retrieve datasets", nullptr);

        if ( oDatasetResponse.IsElementPresent("Eosb", ANSI_CHARACTER_STRING_VALUE_TYPE) )
        {
            m_oEosbRotator.SetEosb(oDatasetResponse.GetString("Eosb"));
        }

        StructuredBuffer oDatasets = oDatasetResponse.GetStructuredBuffer("Datasets");
        for (const std::string& strDatasetGuid : oDatasets.GetNamesOfElements())
        {
            StructuredBuffer oDatasetRecord = oDatasets.GetStructuredBuffer(strDatasetGuid.c_str());
            Guid oDatasetGuid(strDatasetGuid.c_str());
            m_stlAvailableDatasets.insert({oDatasetGuid.ToString(eRaw), oDatasetRecord});

            // Cache our tables
            StructuredBuffer oDatasetTables = oDatasetRecord.GetStructuredBuffer("Tables");
            for ( const auto& oTableItr : oDatasetTables.GetNamesOfElements() )
            {
                TableInformation oTableInfo(oDatasetGuid.ToString(eRaw), oDatasetTables.GetStructuredBuffer(oTableItr.c_str()));
                m_stlAvailableTables.insert({oTableItr, oTableInfo});
            }
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
        m_stlAvailableDatasets.clear();
        m_stlAvailableTables.clear();
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        m_stlAvailableDatasets.clear();
        m_stlAvailableTables.clear();
    }
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetDatasets
 * @brief Lookup in our local cache for the datasets we have and return them as a JSON string
 * @return std::string - Containing a list of our datasets in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::GetDatasets(void) const
{
    __DebugFunction();

    return ::GetJsonForStructuredBufferMap(m_stlAvailableDatasets);
}

/********************************************************************************************/

/********************************************************************************************
 *
 * @class Orchestrator
 * @function Login
 * @brief Log into the remote with the email and password supplied to the port and IP
 * @return unsigned int - status code of the login operation
 *
 ********************************************************************************************/
unsigned int Orchestrator::Login(
    _in const std::string& c_strEmail,
    _in const std::string& c_strUserPassword,
    _in const int c_wordServerPort,
    _in const std::string& c_strServerIPAddress
    )
{
    __DebugFunction();
    __DebugAssert(0 < c_strEmail.size());
    __DebugAssert(0 < c_strUserPassword.size());

    std::string strEosb;
    uint64_t unStatus{401};
    try
    {
        std::string strVerb = "POST";
        std::string strApiUrl = "/SAIL/AuthenticationManager/User/Login?Email="+ c_strEmail +"&Password="+ c_strUserPassword;
        std::string strJsonBody = "";
        // Make the API call and get REST response
        std::vector<Byte> stlRestResponse = ::RestApiCall(c_strServerIPAddress, c_wordServerPort, strVerb, strApiUrl, strJsonBody, true);
        std::string strUnescapedResponse = ::UnEscapeJsonString((const char *) stlRestResponse.data());
        StructuredBuffer oResponse(JsonValue::ParseDataToStructuredBuffer(strUnescapedResponse.c_str()));
        unStatus = static_cast<uint64_t>(oResponse.GetFloat64("Status"));
        _ThrowBaseExceptionIf((201 != unStatus), "Error logging in.", nullptr);
        strEosb = oResponse.GetString("Eosb");

        if ( m_oEosbRotator.IsRunning() )
        {
            std::cout << "Replacing existing session" << std::endl;
            m_oEosbRotator.Stop();
        }
        m_oEosbRotator.SetEosb(strEosb);

        // Start the periodic rotation of EOSBs
        m_oEosbRotator.Start(c_strServerIPAddress, c_wordServerPort);

        // Get our list of digital contracts
        CacheDigitalContractsFromRemote(c_strServerIPAddress, c_wordServerPort);

        CacheDatasetsFromRemote(c_strServerIPAddress, c_wordServerPort);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return unStatus;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetDigitalContracts
 * @brief Lookup in our local cache for the digital contracts we have and return them as a JSON string
 * @return std::string - Containing a JSON dictionary of our DCs in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::GetDigitalContracts(void) const
{
    __DebugFunction();

    return ::GetJsonForStructuredBufferMap(m_stlDigitalContracts);
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetTables
 * @brief Lookup in our local cache for the digital contracts we have and return them as a JSON string
 * @return std::string - Containing a JSON dictionary of our DCs in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::GetTables(void) const
{
    __DebugFunction();

    return ::GetJsonForStructuredBufferMap(m_stlAvailableTables);
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetCurrentEosb
 * @brief Return the EOSB currently being used
 * @return std::string - The value of the EOSB currently being used
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::GetCurrentEosb(void) const
{
    __DebugFunction();

    return m_oEosbRotator.GetEosb();
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function ExitCurrentSession
 * @brief Remove information related to our current lgoged in session, and stop EOSB rotation
 *
 ********************************************************************************************/
void __thiscall Orchestrator::ExitCurrentSession(void)
{
    __DebugFunction();

    if ( true == m_oEosbRotator.IsRunning() )
    {
        m_oEosbRotator.Stop();
        m_oEosbRotator.SetEosb("");
    }
    m_stlDigitalContracts.clear();
    m_stlAvailableDatasets.clear();
    m_stlAvailableTables.clear();
    m_stlProvisionInformation.clear();
    m_stlAvailableSafeFunctions.clear();
    m_stlPushedData.clear();

    m_stlJobInformation.clear();
    m_oJobMessageQueue.ClearAllMessages();
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function LoadSafeObjects
 * @brief Cache all the safeobjects found in a local folder
 *
 ********************************************************************************************/
int __thiscall Orchestrator::LoadSafeObjects(
    _in const std::string& c_strSafeObjectDirectory
    )
{
    __DebugFunction();

    int nReturnValue{0};
    std::error_code stlFileErrorCode;

    bool fDirectoryExists = std::filesystem::exists(c_strSafeObjectDirectory, stlFileErrorCode);

    if ( fDirectoryExists )
    {
        for ( const auto & oEntry : std::filesystem::directory_iterator(c_strSafeObjectDirectory) )
        {
            // Only load objects that have the right extension
            if ( oEntry.path().extension() == ".safe" )
            {
                try
                {
                    std::string strFilename = oEntry.path().string();
                    std::vector<Byte> stlFileContents = ::ReadFileAsByteBuffer(strFilename);
 
                    if ( stlFileContents.size() > 0 )
                    {
                        StructuredBuffer oSafeObject(stlFileContents);
                        Guid oSafeObjectGuid(oSafeObject.GetString("Uuid"));
                        m_stlAvailableSafeFunctions.emplace(oSafeObjectGuid.ToString(eRaw), oSafeObject);
                        ++nReturnValue;
                    }
                }
                catch(const BaseException& oBaseException )
                {
                    ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
                }

                catch( ... )
                {
                    ::RegisterUnknownException(__func__, __FILE__, __LINE__);
                }
            }
        }
    }
    else
    {
        if ( stlFileErrorCode )
        {
            nReturnValue = stlFileErrorCode.value();
        }
        else
        {
            nReturnValue = -1;
        }
    }

    return nReturnValue;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetSafeFunctions
 * @brief Build a list of safe functions available
 * @return std::string - Containing a list of our safe functions in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::GetSafeFunctions(void) const
{
    __DebugFunction();

    return ::GetJsonForStructuredBufferMap(m_stlAvailableSafeFunctions);
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function ProvisionSecureComputationalNode
 * @brief Send a request to provision a Secure Computational Node (SCN)
 * @param[in] c_strDigitalContractGUID The GUID of the digital contract to provision with the SCN
 * @param[in] std::string - Eventually the GUID of the dataset in the family to provision, un-used today
 * @return std::string - Containing a list of our safe functions in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::ProvisionSecureComputationalNode(
    _in const std::string & c_strDigitalContractGUID,
    _in const std::string & c_strDatasetGUID,
    _in const std::string & c_strVmType
    )
{
    __DebugFunction();
    unsigned int unStatus{404};
    bool fProvisionResult{false};
    Guid oScnProvisionGuid(eOrchestratorProvisionTask);
    StructuredBuffer oReturnStructuredBuffer;
    const std::string c_strRawProvisionGuid{oScnProvisionGuid.ToString(eRaw)};

    try
    {
        Guid oDatasetGuid(c_strDatasetGUID);
        Guid oDigitalContractGuid(c_strDigitalContractGUID);
        const std::string c_strRawDigitalContractGuid{oDigitalContractGuid.ToString(eRaw)};
        m_stlProvisionInformation[c_strRawProvisionGuid].strDigitalContractGUID = c_strRawDigitalContractGuid;
        DigitalContractProvisiongStatus eProvisionStatus = GetProvisionStatus(c_strRawProvisionGuid);

        // First check if this DC is already provisioned
        if ( (DigitalContractProvisiongStatus::eProvisioning == eProvisionStatus) || (DigitalContractProvisiongStatus::eReady == eProvisionStatus) )
        {
            // Right now SCN provision and DC are linked 1:1, but we want to expand it to allow multiple
            // SCNs to have the same DC
            m_stlProvisionInformation[c_strRawProvisionGuid].eProvisionStatus = eProvisionStatus;

            // Once we have DCs based more on families this will have to be changed
            if ( (m_stlProvisionInformation[c_strRawProvisionGuid].strDatasetGUID != oDatasetGuid.ToString(eRaw)) &&
                m_stlProvisionInformation[c_strRawProvisionGuid].strDatasetGUID != "" )
            {
                _ThrowBaseException("Digital contract already assigned to dataset %s", m_stlProvisionInformation[c_strRawProvisionGuid].strDatasetGUID);
            }
            m_stlProvisionInformation[c_strRawProvisionGuid].strProvisionMessage = "";
            m_stlProvisionInformation[c_strRawProvisionGuid].strDatasetGUID = oDatasetGuid.ToString(eRaw);
            unStatus = 200;
        }
        else
        {
            std::string strVerb = "POST";
            std::string strApiUrl = "/SAIL/DigitalContractManager/Provision?Eosb=" + m_oEosbRotator.GetEosb();
            StructuredBuffer oJsonRequest;
            oJsonRequest.PutString("DigitalContractGuid", oDigitalContractGuid.ToString(eHyphensAndCurlyBraces));
            oJsonRequest.PutString("DatasetGuid", oDatasetGuid.ToString(eHyphensAndCurlyBraces));
            oJsonRequest.PutString("VirtualMachineType", c_strVmType);
            std::string strContent = ::ConvertStructuredBufferToJson(oJsonRequest);

            std::vector<Byte> stlRestResponse = ::RestApiCall(m_oEosbRotator.GetServerIp(), (Word) m_oEosbRotator.GetServerPort(), strVerb, strApiUrl, strContent, true);
            StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));

            if ( oResponse.IsElementPresent("Status", FLOAT64_VALUE_TYPE) )
            {
                unStatus = oResponse.GetFloat64("Status");
            }
            else
            {
                std::cout << "No provision status?" << std::endl;
            }

            if ( oResponse.IsElementPresent("Message", ANSI_CHARACTER_STRING_VALUE_TYPE) )
            {
                m_stlProvisionInformation[c_strRawProvisionGuid].strProvisionMessage = oResponse.GetString("Message");
            }
            if ( (200 == unStatus) || (201 == unStatus) )
            {
                fProvisionResult = true;
                m_stlProvisionInformation[c_strRawProvisionGuid].eProvisionStatus = DigitalContractProvisiongStatus::eProvisioning;
                m_stlProvisionInformation[c_strRawProvisionGuid].strDatasetGUID = oDatasetGuid.ToString(eRaw);
            }
        }
    }
    catch(const BaseException& oBaseException )
    {
        ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
        unStatus = 404;
    }
    catch( ... )
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        unStatus = 404;
    }

    oReturnStructuredBuffer.PutBoolean("Status", fProvisionResult);
    oReturnStructuredBuffer.PutString("Message", m_stlProvisionInformation[c_strRawProvisionGuid].strProvisionMessage);
    if ( true == fProvisionResult )
    {
        oReturnStructuredBuffer.PutString("ScnId", oScnProvisionGuid.ToString(eHyphensAndCurlyBraces));
    }

    return GetJsonForStructuredBuffer(oReturnStructuredBuffer);
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function RunJob
 * @brief Start running a job for a given safe function
 * @param[in] c_strSafeFuncionGUID The GUID of the safe function to run
 * @return std::string - The GUID JobID
 *
 ********************************************************************************************/
std::string Orchestrator::RunJob(
    _in const std::string& c_strSafeFunctionId
    )
{
    __DebugFunction();


    std::string strNewJobId{""};
    try
    {
        // We must be logged in to start a job
        if ( "" != m_oEosbRotator.GetEosb() )
        {
            Guid oSafeFunctionGuid(c_strSafeFunctionId);
            if ( m_stlAvailableSafeFunctions.end() != m_stlAvailableSafeFunctions.find(oSafeFunctionGuid.ToString(eRaw)) )
            {

                    std::vector<std::string> stlInputParameters;
                    Guid oJobId(eJobIdentifier);
                    StructuredBuffer oSafeFunction = m_stlAvailableSafeFunctions[oSafeFunctionGuid.ToString(eRaw)];
                    StructuredBuffer oInputParameters = oSafeFunction.GetStructuredBuffer("InputParameters");
                    for (const std::string& strInputParameterId : oInputParameters.GetNamesOfElements() )
                    {
                        stlInputParameters.push_back(oInputParameters.GetStructuredBuffer(strInputParameterId.c_str()).GetString("Uuid"));
                    }
                    // When returning GUIDs to the user we return human readable versions
                    strNewJobId = oJobId.ToString(eHyphensAndCurlyBraces);

                    // We make a unique pointer because mutexes are not trivially copyable
                    m_stlJobInformation.emplace(oJobId.ToString(eRaw), new JobInformation(oJobId, oSafeFunctionGuid, stlInputParameters, m_oJobMessageQueue));
            }
        }
    }
    catch(const BaseException& oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return strNewJobId;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetJobStatus
 * @brief Get the job status for a given job id
 * @param[in] c_strJobId The GUID of the safe function to run
 * @return std::string - The status of the current job
 *
 ********************************************************************************************/
std::string Orchestrator::GetJobStatus(
    _in const std::string& c_strJobId
) const
{
    __DebugFunction();

    std::string strStatus = "Job not found";
    try
    {
        Guid oJobGuid(c_strJobId);

        if ( m_stlJobInformation.end() != m_stlJobInformation.find(oJobGuid.ToString(eRaw)) )
        {
            __DebugAssert(nullptr != m_stlJobInformation.at(oJobGuid.ToString(eRaw)).get());
            std::lock_guard<JobInformation> stlLock(*m_stlJobInformation.at(oJobGuid.ToString(eRaw)).get());
             strStatus = m_stlJobInformation.at(oJobGuid.ToString(eRaw))->GetJobStatus();
        }
    }
    catch(const BaseException& oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
        strStatus = "Job not found";
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        strStatus = "Job not found";
    }
    return strStatus;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function SetParameter
 * @brief Get the job status for a given job id
 * @param[in] c_strJobId The GUID of the job whose parameter to set
 * @param[in] c_strInputParamId The input parameter to set
 * @param[in] c_strParamValue The value for the input parameter
 * @return std::string - The ID for the parameter if it was set, blank if it wasn't
 *
 ********************************************************************************************/
std::string Orchestrator::SetParameter(
    _in const std::string& c_strJobId,
    _in const std::string& c_strInputParamId,
    _in const std::string& c_strParamValue
    )
{
    __DebugFunction();

    std::string strParameterId{""};
    try
    {
        Guid oJobId(c_strJobId);
        auto stlJobInformation = m_stlJobInformation.find(oJobId.ToString(eRaw));
        if ( m_stlJobInformation.end() != stlJobInformation )
        {
            __DebugAssert( nullptr != stlJobInformation->second.get() );
            Guid oParameterGuid(c_strParamValue);
            Guid oInputParameterGuid(c_strInputParamId);

            JobInformation& oJobInformation = *stlJobInformation->second;
            std::lock_guard<JobInformation> stlLock(oJobInformation);
            if ( true == oJobInformation.SetInputParameter(c_strInputParamId, c_strParamValue) )
            {
                strParameterId = oJobId.ToString(eHyphensAndCurlyBraces) + "." + oInputParameterGuid.ToString(eHyphensAndCurlyBraces);

                UpdateJobIPAddressForParameter(oJobInformation, oParameterGuid);

                // We have everything we need to submit this job, start it up
                if ( true == oJobInformation.ReadyToExcute() )
                {
                    StartJobRemoteExecution(oJobInformation);
                }
            }
        }
    }
    catch(const BaseException& oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
        m_stlDigitalContracts.clear();
    }
    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        m_stlDigitalContracts.clear();
    }
    return strParameterId;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function UpdateJobIPAddressForParameter
 * @brief Given a job and Guid, update the IP if it's available
 * @param[in] oJob The job information object for the IP address to update
 * @param[in] c_oParameterGuid The value of the parameter whose IP address we want to update
 * @return std::string - The ID for the parameter if it was set, blank if it wasn't
 *
 ********************************************************************************************/
void __thiscall Orchestrator::UpdateJobIPAddressForParameter(
    _in JobInformation& oJob,
    _in const Guid& c_oParameterGuid
    )
{
    if ( eDataset == c_oParameterGuid.GetObjectType() )
    {
        std::string strTargetIP = GetIPServingDataset(c_oParameterGuid);
        if ( "" != strTargetIP )
        {
            _ThrowBaseExceptionIf(((oJob.GetTargetIP() != "") && (oJob.GetTargetIP() != strTargetIP)), "Job already has an IP target", nullptr);
            oJob.SetTargetIP(strTargetIP);
        }
    }
    else if ( eTable == c_oParameterGuid.GetObjectType() )
    {
        std::string strTargetIP = GetIPServingTable(c_oParameterGuid);

        if ( "" != strTargetIP )
        {
            _ThrowBaseExceptionIf(((oJob.GetTargetIP() != "") && (oJob.GetTargetIP() != strTargetIP)), "Job already has an IP target", nullptr);
            oJob.SetTargetIP(strTargetIP);
        }
    }
    else if ( eUserSuppliedData != c_oParameterGuid.GetObjectType() )
    {
        // Try to see if this is a an old dataset
        std::string strTargetIP = GetIPServingDataset(c_oParameterGuid);
        if ( "" != strTargetIP )
        {
            _ThrowBaseExceptionIf(((oJob.GetTargetIP() != "") && (oJob.GetTargetIP() != strTargetIP)), "Job already has an IP target", nullptr);
            oJob.SetTargetIP(strTargetIP);
        }
    }
}
/********************************************************************************************
 *
 * @class Orchestrator
 * @function StartJobRemoteExecution
 * @brief Setup everything we need on the remote job engine to start a job
 *
 ********************************************************************************************/
bool __thiscall Orchestrator::StartJobRemoteExecution(
    _in JobInformation& oJob
    ) throw()
{
    __DebugFunction();

    std::cout << "Job " << oJob.GetJobId().ToString(eHyphensAndCurlyBraces) << " is ready to execute on IP " << oJob.GetTargetIP() << std::endl;

    bool fJobStarted{false};
    try
    {
        // Establish connection with the remote
        TlsNode* poJobEngineSocket =::TlsConnectToNetworkSocket(oJob.GetTargetIP(), REMOTE_JOB_PORT);
        if ( nullptr == poJobEngineSocket )
        {
            std::cout << "Failed to connect to remote " << oJob.GetTargetIP() << std::endl;
        }
        // TODO Put this back in once we can talk to SCNs
        //_ThrowBaseExceptionIf((nullptr == poJobEngineSocket), "Failed to connect to remote job engine", nullptr);

        // Start the listener thread for the job
        oJob.StartJobEngineListenerThread();

        SendSafeObjectToJobEngine(oJob);

        for ( auto oParameterItr : oJob.GetInputParameterMap() )
        {
            __DebugAssert(oParameterItr.second.has_value());
            Guid oParameterGuid(oParameterItr.first);
            Guid oParameterValueGuid(oParameterItr.second.value());

            // We need to push this to the remote job engine
            if ( eUserSuppliedData == oParameterGuid.GetObjectType() )
            {
                PushUserDataToJob(oJob, oParameterGuid);
            }

            // Set the input parameters on the job engine
            SetParameterOnJob(oJob, oParameterGuid, oParameterValueGuid);
        }

        std::cout << "Job " << oJob.GetJobId().ToString(eHyphensAndCurlyBraces) << " has sent all parameters " << std::endl;
        fJobStarted = true;
    }

    catch(const BaseException& oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
    }
    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return fJobStarted;
}

 /********************************************************************************************
  *
  * @class Orchestrator
- * @function GetDigitalContractProvisionStatus
- * @brief Get the provision status of a digital contract
- * @param[in] std::string - The Digital contract's GUID
- * @return DigitalContractProvisioningStatus - The enum of the digital contract status
+ * @function SetParameter
+ * @brief Get the job status for a given job id
+ * @return std::string - The ID for the parameter if it was set, blank if it wasn't
  *
  ********************************************************************************************/
DigitalContractProvisiongStatus __thiscall Orchestrator::GetProvisionStatus(
    const Guid& c_oSecureNodeProvisionGUID
    )
{
    __DebugFunction();

    const std::string c_strRawSecureNodeProvisionGuid{c_oSecureNodeProvisionGUID.ToString(eRaw)};
    Guid oDigitalContractGuid(m_stlProvisionInformation[c_strRawSecureNodeProvisionGuid].strDigitalContractGUID);
    const std::string c_strRawDigitalContractGuid{oDigitalContractGuid.ToString(eRaw)};
    std::string strVerb = "GET";
    std::string strApiUrl = "/SAIL/DigitalContractManager/GetProvisioningStatus?Eosb=" + m_oEosbRotator.GetEosb();
    std::string strContent = "{\n   \"DigitalContractGuid\":\"" + oDigitalContractGuid.ToString(eHyphensAndCurlyBraces) + "\"\n}";
    std::vector<Byte> stlRestResponse = ::RestApiCall(m_oEosbRotator.GetServerIp(), (Word) m_oEosbRotator.GetServerPort(), strVerb, strApiUrl, strContent, true);
    std::string strUnescapedResponse = ::UnEscapeJsonString((const char *) stlRestResponse.data());
    StructuredBuffer oResponse(JsonValue::ParseDataToStructuredBuffer(strUnescapedResponse.c_str()));
    _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "Error retrieving digital contract provision status", nullptr);

    DigitalContractProvisiongStatus eProvisionStatus = ::ProvisioningStatusFromFloat(oResponse.GetFloat64("ProvisioningStatus"));

    m_stlProvisionInformation[c_strRawSecureNodeProvisionGuid].eProvisionStatus = eProvisionStatus;

    if ( oResponse.IsElementPresent("VirtualMachines", INDEXED_BUFFER_VALUE_TYPE) )
    {
        if ( "" == m_stlProvisionInformation[c_strRawSecureNodeProvisionGuid].strRemoteIpAddress )
        {
            StructuredBuffer oVirtualMachines = oResponse.GetStructuredBuffer("VirtualMachines");

            // We expect at most 1 VM per provision
            __DebugAssert(oVirtualMachines.GetNamesOfElements().size() == 1);
            m_stlProvisionInformation[c_strRawSecureNodeProvisionGuid].strVMGUID = oVirtualMachines.GetNamesOfElements()[0];
            m_stlProvisionInformation[c_strRawSecureNodeProvisionGuid].strRemoteIpAddress = oVirtualMachines.GetString(m_stlProvisionInformation[c_strRawSecureNodeProvisionGuid].strVMGUID.c_str());
            std::cout << "DC " << c_strRawDigitalContractGuid << " has IP " << m_stlProvisionInformation[c_strRawSecureNodeProvisionGuid].strRemoteIpAddress << std::endl;
        }
        else
        {
            std::cout << "DC " << c_strRawDigitalContractGuid << " already has an IP" << std::endl;
        }
    }

    // We intentially do not catch exceptions here as we want to return a DigitalContractProvisioningStatus
    // enum, and if we fail there's no proper enum value to return
    return eProvisionStatus;
 }

/********************************************************************************************
 *
 * @class Orchestrator
 * @function WaitForAllSecureNodesToBeProvisioned
 * @brief Wait on our SCNs to be provisioned
 * @return std::string - The provision status of the SCNs
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::WaitForAllSecureNodesToBeProvisioned(
    _in int nTimeoutInMs
    )
{
    std::string strProvisionStatus{""};

    // If we aren't logged in, don't return anything
    if ( "" != m_oEosbRotator.GetEosb())
    {
        try
        {
            StructuredBuffer oProvisionStatus;
            std::set<std::string> stlSucceededProvisions;
            std::set<std::string> stlInProgressProvisions;
            std::set<std::string> stlFailedProvisions;
            bool fTimedOut{false};

            // We aren't ready, wait and check again
            while ( m_stlProvisionInformation.size() != (stlFailedProvisions.size() + stlSucceededProvisions.size()) && !fTimedOut )
            {
                for ( const auto& stlSecureComputationNodeItr : m_stlProvisionInformation )
                {
                    if ( stlSucceededProvisions.end() == stlSucceededProvisions.find(stlSecureComputationNodeItr.first) )
                    {
                        Guid oDigitalContractGuid(stlSecureComputationNodeItr.second.strDigitalContractGUID);
                        Guid oSecureComputationalNodeGuid(stlSecureComputationNodeItr.first);
                        DigitalContractProvisiongStatus eProvisionStatus = GetProvisionStatus(oSecureComputationalNodeGuid);
                        if ( DigitalContractProvisiongStatus::eReady == eProvisionStatus )
                        {
                            stlSucceededProvisions.insert(stlSecureComputationNodeItr.first);
                            stlInProgressProvisions.erase(stlSecureComputationNodeItr.first);
                            stlFailedProvisions.erase(stlSecureComputationNodeItr.first);
                        }
                        else if ( DigitalContractProvisiongStatus::eProvisioning == eProvisionStatus )
                        {
                            stlInProgressProvisions.insert(stlSecureComputationNodeItr.first);
                        }
                        else
                        {
                            stlFailedProvisions.insert(stlSecureComputationNodeItr.first);
                        }
                    }
                }

                // A provision is considered complete whether it succeeded or failed
                if ( m_stlProvisionInformation.size() != (stlFailedProvisions.size() + stlSucceededProvisions.size()) )
                {
                    if ( 0 < nTimeoutInMs)
                    {
                        constexpr int c_nTimeoutThreshold{100};
                        int64_t nCurrentTimeout = std::min(nTimeoutInMs, c_nTimeoutThreshold);
                        std::this_thread::sleep_for(std::chrono::milliseconds(nCurrentTimeout));
                        nTimeoutInMs -= nCurrentTimeout;
                    }

                    if ( 0 >= nTimeoutInMs )
                    {
                        fTimedOut = true;
                    }
                }
            }

            bool fAllNodesReady = ( stlSucceededProvisions.size() == m_stlProvisionInformation.size() );
            StructuredBuffer oSucceededProvisions;
            StructuredBuffer oFailedProvisions;
            StructuredBuffer oInProgressProvisions;
            unsigned int unProvisionItr{0};
            for ( auto& oSucceededItr : stlSucceededProvisions )
            {
                Guid oProvisionGuid(oSucceededItr);
                oSucceededProvisions.PutString(oProvisionGuid.ToString(eHyphensAndCurlyBraces).c_str(), m_stlProvisionInformation[oSucceededItr].strProvisionMessage);
                ++unProvisionItr;
            }
            unProvisionItr = 0;
            for ( auto& oInProgressItr : stlInProgressProvisions )
            {
                Guid oProvisionGuid(oInProgressItr);
                oInProgressProvisions.PutString(oProvisionGuid.ToString(eHyphensAndCurlyBraces).c_str(), m_stlProvisionInformation[oInProgressItr].strProvisionMessage);
                ++unProvisionItr;
            }
            unProvisionItr = 0;
            for ( auto& oFailedItr : stlFailedProvisions )
            {
                Guid oProvisionGuid(oFailedItr);
                oInProgressProvisions.PutString(oProvisionGuid.ToString(eHyphensAndCurlyBraces).c_str(), m_stlProvisionInformation[oFailedItr].strProvisionMessage);
                ++unProvisionItr;
            }

            oProvisionStatus.PutBoolean("AllDone", fAllNodesReady);
            oProvisionStatus.PutStructuredBuffer("Succeeded", oSucceededProvisions);
            oProvisionStatus.PutStructuredBuffer("Failed", oFailedProvisions);
            oProvisionStatus.PutStructuredBuffer("InProgress", oInProgressProvisions);
            strProvisionStatus = ::GetJsonForStructuredBuffer(oProvisionStatus);
        }
        catch(const BaseException& oBaseException )
        {
            ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
            strProvisionStatus = "";
        }
        catch( ... )
        {
            ::RegisterUnknownException(__func__, __FILE__, __LINE__);
            strProvisionStatus = "";
        }
    }
    return strProvisionStatus;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function PushData
 * @brief Save user data in the orchestrator and generate an ID for it
 * @return std::string - The ID for the pushed data
 *
 ********************************************************************************************/
std::string Orchestrator::PushUserData(
    _in const std::vector<Byte>& c_stlIncomingData
    )
{
    __DebugFunction();

    Guid oDataId(eUserSuppliedData);
    std::string strDataId = oDataId.ToString(eHyphensAndCurlyBraces);
    __DebugAssert(m_stlPushedData.end() == m_stlPushedData.find(strDataId));

    m_stlPushedData[strDataId] = c_stlIncomingData;

    return strDataId;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetIPServingDataset
 * @brief Get the IP address of a VM serving a dataset's GUID
 * @param[in] Guid - The GUID of the dataset we're looking for
 * @return std::string - The IP address of the VM hosting the dataset, "" if we don't find it
 ********************************************************************************************/
std::string Orchestrator::GetIPServingDataset(
    _in const Guid& oDatasetGuid
    ) const
{
    __DebugFunction();
    // Disabled until new data annotation tool is in place
    //__DebugAssert(eDataset == oDatasetGuid.GetObjectType());

    std::string strIpAddress{""};

    for ( auto oDatasetItr : m_stlProvisionInformation)
    {
        if ( oDatasetItr.second.strDatasetGUID == oDatasetGuid.ToString(eRaw))
        {
            strIpAddress = oDatasetItr.second.strRemoteIpAddress;
        }
    }
    return strIpAddress;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetIPServingTable
 * @brief Get the IP address of a VM serving a table's GUID
 * @param[in] std::string - The GUID of the table we're looking for
 * @return std::string - The IP address of the VM hosting the table, "" if we don't find it
 ********************************************************************************************/
std::string Orchestrator::GetIPServingTable(
    _in const Guid& oTableGuid
    ) const
{
    __DebugFunction();
    // Disabled until new dataset annotation tool is in place
    //__DebugAssert(eTable == oTableGuid.GetObjectType());

    std::string strIpAddress{""};
    for ( auto oTableItr : m_stlAvailableTables )
    {
        if ( oTableGuid.ToString(eRaw) == oTableItr.second.m_strParentDataset )
        {
            Guid oDatasetGuid(oTableItr.second.m_strParentDataset);
            strIpAddress = GetIPServingDataset(oDatasetGuid);
        }
    }

    return strIpAddress;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function PullJobData
 * @brief Register against the job engine to pull data for a job
 * @param[in] std::string - The ID for the parameter pull in form: "JobGUID.OutputParameterGuid"
 * @return std::string - The result of the request to pull, "success" if it went well, error
 *                       message otherwise
 ********************************************************************************************/
std::string __thiscall Orchestrator::PullJobData(
        _in const std::string& c_strOutputParameter
    ) throw()
{
    __DebugFunction();
    std::string strResult{"Invalid parameter"};
    try
    {
        size_t unFirstPeriod = c_strOutputParameter.find_first_of(".");
        size_t unLastPeriod = c_strOutputParameter.find_last_of(".");
        _ThrowBaseExceptionIf( (std::string::npos == unFirstPeriod) || (unFirstPeriod != unLastPeriod),
            "Invalid parameter specifier", nullptr);
        const std::string& c_strJobId = c_strOutputParameter.substr(0, unFirstPeriod);
        const std::string& c_strParameterId = c_strOutputParameter.substr(unFirstPeriod + 1, std::string::npos);
        std::cout << "Pulling data for job " << c_strJobId << " parameter " << c_strParameterId << std::endl;

        auto oStlJobInformationItr = m_stlJobInformation.find(c_strJobId);
        if ( m_stlJobInformation.end() == oStlJobInformationItr )
        {
            strResult = "Job not found";
        }
        else
        {
            __DebugAssert(nullptr != oStlJobInformationItr->second.get());

            std::lock_guard<JobInformation> stlLock(*oStlJobInformationItr->second);
            const std::string& c_strSafeFunctionId = oStlJobInformationItr->second->GetSafeFunctionId();
            auto oSafeFunctionItr = m_stlAvailableSafeFunctions.find(c_strSafeFunctionId);
            __DebugAssert(m_stlAvailableSafeFunctions.end() != oSafeFunctionItr);
            const StructuredBuffer& c_oOutputParameters = oSafeFunctionItr->second.GetStructuredBuffer("OutputParamters");
            if ( false == c_oOutputParameters.IsElementPresent(c_strParameterId.c_str(), INDEXED_BUFFER_VALUE_TYPE) )
            {
                strResult = "Parameter not found in safe function";
            }
            else
            {
                const StructuredBuffer& c_oOutputParameter = c_oOutputParameters.GetStructuredBuffer(c_strParameterId.c_str());
                if ( c_oOutputParameter.GetString("Confidentiality") == "1" )
                {
                    strResult = "Parameter is confidential";
                }
                else
                {
                    StructuredBuffer oPushBuffer;
                    oPushBuffer.PutByte("RequestType", static_cast<Byte>(EngineRequest::ePullData));
                    oPushBuffer.PutString("EndPoint", "JobEngine");
                    oPushBuffer.PutString("Filename", c_strOutputParameter);

                    oStlJobInformationItr->second->SendStructuredBufferToJobEngine(oPushBuffer);
                    strResult = "Success";
                }
            }
        }
    }
    catch(const BaseException& oBaseException )
    {
        ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
        strResult = "Error";
    }
    catch( ... )
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        strResult = "Error";
    }

    return strResult;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function WaitForData
 * @brief Wait on any job to return data through a StructuredBuffer
 * @param[in] int - The timeout in ms for how long to wait for a StructuredBuffer
 * @return std::string - The data found, "" if we didn't find a StructuredBuffer
 ********************************************************************************************/
std::string __thiscall Orchestrator::WaitForData(
    _in int nTimeoutInMs
    ) throw()
{
    std::string strReturn{""};
    std::shared_ptr<StructuredBuffer> oDataResult = m_oJobMessageQueue.WaitForMessage(nTimeoutInMs);

    try
    {
        if ( nullptr != oDataResult )
        {
            if ( oDataResult->IsElementPresent("SignalType", BYTE_VALUE_TYPE) )
            {
                if ( static_cast<Byte>(JobStatusSignals::ePostValue) == oDataResult->GetByte("SignalType"))
                {
                    UpdateJobsWaitingForData(*oDataResult);
                }
            }
            strReturn = GetJsonForStructuredBuffer(*oDataResult);
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
        strReturn = "";

    }
    catch ( ... )
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        strReturn = "";
    }

    // TODO Check if this is data for another job
    return strReturn;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function UpdateJobsWaitingForData
 * @brief Update any jobs who may have been waiting for a data push
 * TODO Complete this when we are talking to SCNs
 * @param[in] c_oPushDataMessage - The timeout in ms for how long to wait for a StructuredBuffer
 *
 ********************************************************************************************/
void __thiscall Orchestrator::UpdateJobsWaitingForData(
    _in const StructuredBuffer& c_oPushDataMessage
    )
{
    std::cout << "Looking to update jobs for data" << std::endl;

    for ( auto& oJobInformation : m_stlJobInformation )
    {
        __DebugAssert(nullptr != oJobInformation.second.get());

        std::lock_guard<JobInformation> stlLock(*oJobInformation.second);
        if ( oJobInformation.second->GetInputParameterMap().end() != oJobInformation.second->GetInputParameterMap().find(c_oPushDataMessage.GetString("ValueName") ) )
        {
            std::cout << "Found a parameter that needs an implicit push " << std::endl;
        }
    }
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function PushUserDataToJob
 * @brief Push cached user data to a job
 * @param[in] oJob - The job we want to push data to
 * @param[in] oUserParameter - The GUID of the user data to send to the job engine
 *
 ********************************************************************************************/
void __thiscall Orchestrator::PushUserDataToJob(
    _in JobInformation& oJob,
    _in Guid& oUserParameter
    )
{
    __DebugFunction();
    try
    {
        _ThrowBaseExceptionIf(m_stlPushedData.end() == m_stlPushedData.find(oUserParameter.ToString(eHyphensAndCurlyBraces)), "User parameter not filled in", nullptr);
        StructuredBuffer oPushDataBuffer;
        oPushDataBuffer.PutByte("RequestType", (Byte)EngineRequest::ePushdata);
        oPushDataBuffer.PutString("EndPoint", "JobEngine");
        oPushDataBuffer.PutString("DataId", oUserParameter.ToString(eRaw));
        oPushDataBuffer.PutBuffer("Data", m_stlPushedData[oUserParameter.ToString(eHyphensAndCurlyBraces)]);

        SendDataToJob(oJob, oPushDataBuffer);
    }
    catch(const BaseException& oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function SendSafeObjectToJobEngine
 * @param [in] JobInformation The job to send this data to
 * @brief Send a structured buffer to a job that contains our safe object
 *
 ********************************************************************************************/
void __thiscall Orchestrator::SendSafeObjectToJobEngine(
    _in JobInformation& oJob
    )
{
    __DebugFunction();
    try
    {
        _ThrowBaseExceptionIf( m_stlAvailableSafeFunctions.end() == m_stlAvailableSafeFunctions.find(oJob.GetSafeFunctionId()), "Failed to find safe function", nullptr);

        const StructuredBuffer& oCachedSafeFunction = m_stlAvailableSafeFunctions[oJob.GetSafeFunctionId()];
        StructuredBuffer oSafeFunctionBuffer;
        oSafeFunctionBuffer.PutByte("RequestType", (Byte)EngineRequest::ePushSafeObject);
        oSafeFunctionBuffer.PutString("EndPoint", "JobEngine");
        oSafeFunctionBuffer.PutString("SafeObjectUuid", oCachedSafeFunction.GetString("Uuid"));
        oSafeFunctionBuffer.PutString("Title", oCachedSafeFunction.GetString("Title"));
        oSafeFunctionBuffer.PutString("Description", oCachedSafeFunction.GetString("Description"));
        oSafeFunctionBuffer.PutStructuredBuffer("InputParameters", oCachedSafeFunction.GetStructuredBuffer("InputParameters"));
        oSafeFunctionBuffer.PutStructuredBuffer("OutputParameters", oCachedSafeFunction.GetStructuredBuffer("OutputParameters"));

        SendDataToJob(oJob, oSafeFunctionBuffer);
    }
    catch(const BaseException& c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    catch(std::exception & e)
    {
        std::cout << "Exception: " << e.what() << '\n';
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function SetParameterOnJob
 * @param [in] JobInformation The job to send this data to
 * @param [in] Guid The guid of the parameter to set
 * @param [in] Guid The value of the parameter's guid to set to
 * @brief Send a structured buffer to a job that will tell the job what the GUID for an input
 *        parameter is
 *
 ********************************************************************************************/
void __thiscall Orchestrator::SetParameterOnJob(
    _in JobInformation& oJob,
    _in Guid& oParameterGuid,
    _in Guid& oParameterValueGuid
    )
{
    try
    {
        StructuredBuffer oParameterSetBuffer;
        oParameterSetBuffer.PutByte("RequestType", (Byte)EngineRequest::eSetParameters);
        oParameterSetBuffer.PutString("EndPoint", "JobEngine");
        oParameterSetBuffer.PutString("JobUuid", oJob.GetJobId().ToString(eRaw));
        oParameterSetBuffer.PutString("ParameterUuid", oParameterGuid.ToString(eRaw));
        oParameterSetBuffer.PutString("ValueUuid", oParameterValueGuid.ToString(eRaw));
        oParameterSetBuffer.PutUnsignedInt32("ValuesExpected", 1);
        oParameterSetBuffer.PutUnsignedInt32("ValueIndex", 0);

        SendDataToJob(oJob, oParameterSetBuffer);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (const std::exception & c_oException)
    {
        std::cout << "Exception: " << c_oException.what() << '\n';
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function SendDataToJob
 * @param [in] JobInformation The job to send this data to
 * @param [in] StructuredBuffer The data to send
 * @brief Send a structured buffer to a job
 *
 ********************************************************************************************/
void __thiscall Orchestrator::SendDataToJob(
    _in JobInformation& oJob,
    _in const StructuredBuffer& c_oStructuredBuffer
    )
{
    __DebugFunction()
    try
    {
        std::shared_ptr<TlsNode> poJobEngineConnection = oJob.GetConnection();
        if ( nullptr != poJobEngineConnection.get())
        {
            ::PutTlsTransaction(poJobEngineConnection.get(), c_oStructuredBuffer);
        }
        else
        {
            std::cout << "NO CONNECTION TO JOB ENGINE " << std::endl;
        }
    }
    catch(const BaseException& oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
    }
    catch(std::exception & e)
    {
        std::cout << "Exception: " << e.what() << '\n';
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
}
