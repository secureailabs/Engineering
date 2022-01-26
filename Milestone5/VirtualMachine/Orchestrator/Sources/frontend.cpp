/*********************************************************************************************
 *
 * @file frontend.cpp
 * @author Jingwei Zhang
 * @date 15 Jan 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Class used for single job related issues
 *
 ********************************************************************************************/

#include "frontend.h"
#include "JsonParser.h"
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
 * @class Frontend
 * @function Default constructor
 *
 ********************************************************************************************/
Frontend::Frontend(void):
    m_stlConnectionMap(),
    m_stlJobStatusMap(),
    m_stlDataTableMap(),
    m_stlFNTable(),
    m_stlResultSet(),
    m_fStop(false)
{
    __DebugFunction();
}

/********************************************************************************************
 *
 * @class Frontend
 * @function Destructor
 *
 ********************************************************************************************/
Frontend::~Frontend(void)
{
    __DebugFunction();
}

/********************************************************************************************
 *
 * @class Frontend
 * @function CacheDigitalContractsFromRemote
 * @brief Call to our remote server to get all our digital contracts, and cached their SBs
 *        in a class member map
 *
 ********************************************************************************************/
void __thiscall Frontend::CacheDigitalContractsFromRemote(
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
 * @class Frontend
 * @function CacheDatasetsFromRemote
 * @brief Call to our remote server to get all our datasets, and cached their SBs
 *        in a class member map
 *
 ********************************************************************************************/
void Frontend::CacheDatasetsFromRemote(
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
 * @class Frontend
 * @function GetDatasets
 * @brief Lookup in our local cache for the datasets we have and return them as a JSON string
 * @return std::string - Containing a list of our datasets in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Frontend::GetDatasets(void) const
{
    __DebugFunction();

    return ::GetJsonForStructuredBufferMap(m_stlAvailableDatasets);
}

/********************************************************************************************/

unsigned int Frontend::Login(
    _in const std::string& c_strEmail,
    _in const std::string& c_strUserPassword,
    _in const int c_wordServerPort,
    _in const std::string& c_strServerIPAddress
    )
{
    __DebugFunction();
    //__DebugAssert(0 < strlen(g_szServerIpAddress));
    //__DebugAssert(0 != g_unPortNumber);
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

    m_strUsername = c_strEmail;

    // Pull Datasets
    return unStatus;
}

/********************************************************************************************
 *
 * @class Frontend
 * @function GetDigitalContracts
 * @brief Lookup in our local cache for the digital contracts we have and return them as a JSON string
 * @return std::string - Containing a JSON dictionary of our DCs in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Frontend::GetDigitalContracts(void) const
{
    __DebugFunction();

    return ::GetJsonForStructuredBufferMap(m_stlDigitalContracts);
}

/********************************************************************************************
 *
 * @class Frontend
 * @function GetTables
 * @brief Lookup in our local cache for the digital contracts we have and return them as a JSON string
 * @return std::string - Containing a JSON dictionary of our DCs in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Frontend::GetTables(void) const
{
    __DebugFunction();

    return ::GetJsonForStructuredBufferMap(m_stlAvailableTables);
}

/********************************************************************************************
 *
 * @class Frontend
 * @function GetCurrentEosb
 * @brief Return the EOSB currently being used
 * @return std::string - The value of the EOSB currently being used
 *
 ********************************************************************************************/
std::string __thiscall Frontend::GetCurrentEosb(void) const
{
    __DebugFunction();

    return m_oEosbRotator.GetEosb();
}

/********************************************************************************************
 *
 * @class Frontend
 * @function ExitCurrentSession
 * @brief Remove information related to our current lgoged in session, and stop EOSB rotation
 *
 ********************************************************************************************/
void __thiscall Frontend::ExitCurrentSession(void)
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
 * @class Frontend
 * @function LoadSafeObjects
 * @brief Cache all the safeobjects found in a local folder
 *
 ********************************************************************************************/
int __thiscall Frontend::LoadSafeObjects(
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
 * @class Frontend
 * @function GetSafeFunctions
 * @brief Build a list of safe functions available
 * @return std::string - Containing a list of our safe functions in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Frontend::GetSafeFunctions(void) const
{
    __DebugFunction();

    return ::GetJsonForStructuredBufferMap(m_stlAvailableSafeFunctions);
}

/********************************************************************************************
 *
 * @class Frontend
 * @function ProvisionSecureComputationalNode
 * @brief Send a request to provision a Secure Computational Node (SCN)
 * @param[in] c_strDigitalContractGUID The GUID of the digital contract to provision with the SCN
 * @param[in] std::string - Eventually the GUID of the dataset in the family to provision, un-used today
 * @return std::string - Containing a list of our safe functions in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Frontend::ProvisionSecureComputationalNode(
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
 * @class Frontend
 * @function RunJob
 * @brief Start running a job for a given safe function
 * @param[in] c_strSafeFuncionGUID The GUID of the safe function to run
 * @return std::string - The GUID JobID
 *
 ********************************************************************************************/
std::string Frontend::RunJob(
    _in const std::string& c_strSafeFunctionId
    )
{
    __DebugFunction();


    std::string strNewJobId{""};
    try
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
 * @class Frontend
 * @function GetJobStatus
 * @brief Get the job status for a given job id
 * @param[in] c_strJobId The GUID of the safe function to run
 * @return std::string - The status of the current job
 *
 ********************************************************************************************/
std::string Frontend::GetJobStatus(
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
 * @class Frontend
 * @function SetParameter
 * @brief Get the job status for a given job id
 * @param[in] c_strJobId The GUID of the job whose parameter to set
 * @param[in] c_strInputParamId The input parameter to set
 * @param[in] c_strParamValue The value for the input parameter
 * @return std::string - The ID for the parameter if it was set, blank if it wasn't
 *
 ********************************************************************************************/
std::string Frontend::SetParameter(
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
 * @class Frontend
 * @function UpdateJobIPAddressForParameter
 * @brief Given a job and Guid, update the IP if it's available
 * @param[in] oJob The job information object for the IP address to update
 * @param[in] c_oParameterGuid The value of the parameter whose IP address we want to update
 * @return std::string - The ID for the parameter if it was set, blank if it wasn't
 *
 ********************************************************************************************/
void __thiscall Frontend::UpdateJobIPAddressForParameter(
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
 * @class Frontend
 * @function StartJobRemoteExecution
 * @brief Setup everything we need on the remote job engine to start a job
 *
 ********************************************************************************************/
bool __thiscall Frontend::StartJobRemoteExecution(
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
  * @class Frontend
- * @function GetDigitalContractProvisionStatus
- * @brief Get the provision status of a digital contract
- * @param[in] std::string - The Digital contract's GUID
- * @return DigitalContractProvisioningStatus - The enum of the digital contract status
+ * @function SetParameter
+ * @brief Get the job status for a given job id
+ * @return std::string - The ID for the parameter if it was set, blank if it wasn't
  *
  ********************************************************************************************/
DigitalContractProvisiongStatus __thiscall Frontend::GetProvisionStatus(
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
 * @class Frontend
 * @function WaitForAllSecureNodesToBeProvisioned
 * @brief Wait on our SCNs to be provisioned
 * @return std::string - The provision status of the SCNs
 *
 ********************************************************************************************/
std::string __thiscall Frontend::WaitForAllSecureNodesToBeProvisioned(
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
 * @class Frontend
 * @function PushData
 * @brief Save user data in the orchestrator and generate an ID for it
 * @return std::string - The ID for the pushed data
 *
 ********************************************************************************************/
std::string Frontend::PushUserData(
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
 * @class Frontend
 * @function GetIPServingDataset
 * @brief Get the IP address of a VM serving a dataset's GUID
 * @param[in] Guid - The GUID of the dataset we're looking for
 * @return std::string - The IP address of the VM hosting the dataset, "" if we don't find it
 ********************************************************************************************/
std::string Frontend::GetIPServingDataset(
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
 * @class Frontend
 * @function GetIPServingTable
 * @brief Get the IP address of a VM serving a table's GUID
 * @param[in] std::string - The GUID of the table we're looking for
 * @return std::string - The IP address of the VM hosting the table, "" if we don't find it
 ********************************************************************************************/
std::string Frontend::GetIPServingTable(
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
 * @class Frontend
 * @function PullJobData
 * @brief Register against the job engine to pull data for a job
 * @param[in] std::string - The ID for the parameter pull in form: "JobGUID.OutputParameterGuid"
 * @return std::string - The result of the request to pull, "success" if it went well, error
 *                       message otherwise
 ********************************************************************************************/
std::string __thiscall Frontend::PullJobData(
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
 * @class Frontend
 * @function WaitForData
 * @brief Wait on any job to return data through a StructuredBuffer
 * @param[in] int - The timeout in ms for how long to wait for a StructuredBuffer
 * @return std::string - The data found, "" if we didn't find a StructuredBuffer
 ********************************************************************************************/
std::string __thiscall Frontend::WaitForData(
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
 * @class Frontend
 * @function UpdateJobsWaitingForData
 * @brief Update any jobs who may have been waiting for a data push
 * TODO Complete this when we are talking to SCNs
 * @param[in] c_oPushDataMessage - The timeout in ms for how long to wait for a StructuredBuffer
 *
 ********************************************************************************************/
void __thiscall Frontend::UpdateJobsWaitingForData(
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

void __thiscall Frontend::Listener(
    _in std::string strVMID
)
{
    __DebugFunction();

    while (!m_fStop)
    {
        try
        {
            std::cout << "Waiting for data" << std::endl;
            fflush(stdout);
            std::vector<Byte> stlResponseBuffer = ::GetTlsTransaction(m_stlConnectionMap[strVMID].get(), 0);
            _ThrowBaseExceptionIf((0 == stlResponseBuffer.size()), "No data received.", nullptr);

            StructuredBuffer oResponse(stlResponseBuffer);
            JobStatusSignals eStatusSignalType = (JobStatusSignals)oResponse.GetByte("SignalType");

            switch(eStatusSignalType)
            {
                case JobStatusSignals::eJobStart:
                {
                    std::string strJobID = oResponse.GetString("JobUuid");
                    std::lock_guard<std::mutex> lock(m_stlJobStatusMapMutex);
                    //m_stlJobStatusMap.emplace(strJobID, JobStatusSignals::eJobStart);
                    m_stlJobStatusMap[strJobID] = JobStatusSignals::eJobStart;
                    break;
                }
                case JobStatusSignals::eJobDone:
                {
                    std::string strJobID = oResponse.GetString("JobUuid");
                    std::lock_guard<std::mutex> lock(m_stlJobStatusMapMutex);
                    m_stlJobStatusMap[strJobID] = JobStatusSignals::eJobDone;
                    std::cout<<"Job status of: "<<strJobID<<" set to: "<<(int)m_stlJobStatusMap[strJobID]<<std::endl;
                    break;
                }
                case JobStatusSignals::eJobFail:
                {
                    std::string strJobID = oResponse.GetString("JobUuid");
                    std::lock_guard<std::mutex> lock(m_stlJobStatusMapMutex);
                    m_stlJobStatusMap[strJobID] = JobStatusSignals::eJobFail;
                    break;
                }
                case JobStatusSignals::ePostValue:
                {
                    std::vector<Byte> stlData = oResponse.GetBuffer("FileData");
                    std::string strDataID = oResponse.GetString("ValueName");
                    std::cout<<"Get result posted: "<<strDataID<<" Data length: "<<stlData.size()<<std::endl;
                    //std::lock_guard<std::mutex> lock(m_stlResultMapMutex);
                    //m_stlResultMap.emplace(strDataID, stlData);
                    //m_stlResultMap[strDataID] = stlData;
                    SaveBuffer(strDataID, stlData);
                    m_stlResultSet.emplace(strDataID);
                    break;
                }
                case JobStatusSignals::eHeartBeatPing:
                {
                    // Send a response to the JobEngine to keep the connection alive
                    StructuredBuffer oResponse;
                    oResponse.PutString("EndPoint", "JobEngine");
                    oResponse.PutByte("RequestType", (Byte)EngineRequest::eHeartBeatPong);
                    this->SendDataToJobEngine(strVMID, oResponse);
                    break;
                }
                case JobStatusSignals::eVmShutdown: break;
                default: break;
            }
        }

        catch (const BaseException & c_oBaseException)
        {
            ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
        }

        catch (...)
        {
            ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        }
    }

    m_stlConnectionMap[strVMID].get()->Release();
    // for(auto const& i: m_stlConnectionMap)
    // {
    //     i.second->Release();
    // }
}

void __thiscall Frontend::SaveBuffer(
    std::string& strDataID,
    std::vector<Byte>& stlVars
    )
{
    std::ofstream stlVarFile;
    std::string strFilename = std::string("/tmp/"+strDataID);
    stlVarFile.open(strFilename.c_str(), std::ios::out | std::ios::binary);
    stlVarFile.write((char*)&stlVars[0], stlVars.size());
    stlVarFile.close();
    std::cout<<"writing data file: "<<strDataID<<std::endl;
}


void __thiscall Frontend::SetFrontend(
    _in std::string & strServerIP,
    _in Word wPort,
    _in std::string & strVMID
    )
{
    //if(m_strEOSB.empty())
    //{
    //    m_strEOSB = Login(strEmail, strPassword);
    //    std::cout<<"Login done"<<std::endl;
    //    std::cout<<"EOSB:"<<m_strEOSB<<std::endl;
    //}
    
    StructuredBuffer oBuffer;
    oBuffer.PutByte("RequestType", (Byte)EngineRequest::eConnectVirtualMachine);
    oBuffer.PutString("Eosb", m_oEosbRotator.GetEosb());
    oBuffer.PutString("Username", m_strUsername);

    TlsNode * poSocket = nullptr;

    try
    {
        if(m_stlConnectionMap.end()==m_stlConnectionMap.find(strVMID)){
            poSocket = ::TlsConnectToNetworkSocket(strServerIP.c_str(), wPort);
            _ThrowIfNull(poSocket, "Tls connection error for connectVM", nullptr);
            std::cout<<"connect to "<<strServerIP<<" successful"<<std::endl;

            oBuffer.PutString("EndPoint", "JobEngine");
            PutTlsTransaction(poSocket, oBuffer.GetSerializedBuffer());
            //std::vector<Byte> stlResponse = PutTlsTransactionAndGetResponse(poSocket, oBuffer, 2*60*1000);
            //if(0==stlResponse.size())
            //    _ThrowBaseException("No response for connectVM request", nullptr);

            auto stlResponse = GetTlsTransaction(poSocket, 0);
            _ThrowBaseExceptionIf((0 == stlResponse.size()), "No data received.", nullptr);

            StructuredBuffer oResponse(stlResponse);
            strVMID = oResponse.GetString("VirtualMachineUuid");

            std::map<std::string, std::string> stlDataMap;
            StructuredBuffer oDataset = oResponse.GetStructuredBuffer("Dataset");
            StructuredBuffer oTables = oDataset.GetStructuredBuffer("Tables");
            std::vector<std::string> stlNameList = oTables.GetNamesOfElements();
            
            for(size_t i = 0 ; i<stlNameList.size(); i++)
            {
                //stlDataGuid.push_back(oDataset.GetStructuredBuffer("Tables").GetString(stlNameList[i].c_str()));
                stlDataMap.emplace(stlNameList[i], oDataset.GetStructuredBuffer("Tables").GetString(stlNameList[i].c_str()));
            }

            m_stlDataTableMap.emplace(strVMID, stlDataMap);

            std::shared_ptr<TlsNode> stlSocket(poSocket);
            m_stlConnectionMap.emplace(strVMID, stlSocket);

            // Create and insert a mutex to m_stlConnectionMutexMap for this strVmID
            std::shared_ptr<std::mutex> stlMutex(new std::mutex);
            m_stlConnectionMutexMap.insert(std::make_pair(strVMID, stlMutex));
        }
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    std::thread(&Frontend::Listener, this, strVMID).detach();
}

/********************************************************************************************
 *
 * @class EngineCLI
 * @function HandleRun
 * @param [in] oBuffer Reference of the structured buffer going to be send
 * @param [in] argMap Reference of the user input argument map
 * @brief Prepare the structured buffer going to be send for running a job
 *
 ********************************************************************************************/

void __thiscall Frontend::HandleSubmitJob(
    _in std::string & strVMID,
    _in std::string & strFNID,
    _in std::string & strJobID
    )
{
    std::cout<<"submit job: "<<strJobID<<std::endl;
    StructuredBuffer oBuffer;
    oBuffer.PutString("EndPoint", "JobEngine");
    oBuffer.PutByte("RequestType", (Byte)EngineRequest::eSubmitJob);
    oBuffer.PutString("SafeObjectUuid", strFNID);
    oBuffer.PutString("JobUuid", strJobID);

    try
    {
        this->SendDataToJobEngine(strVMID, oBuffer);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
}

/********************************************************************************************
 *
 * @class EngineCLI
 * @function HandleCheck
 * @param [in] oBuffer Reference of the structured buffer going to be send
 * @param [in] argMap Reference of the user input argument map
 * @brief Prepare the structured buffer going to be send for checking a job result
 *
 ********************************************************************************************/

// void __thiscall Frontend::HandleInspect(
//     _in std::string & strVMID,
//     _inout std::string & strJobs
//     )
// {
//     StructuredBuffer oBuffer;
//     oBuffer.PutInt8("Type", eINSPECT);

//     TlsNode * poSocket =nullptr;
//     try
//     {
//         poSocket = TlsConnectToNetworkSocket(m_stlConnectionMap[strVMID].c_str(), m_stlPortMap[strVMID]);
//         _ThrowIfNull(poSocket, "Tls connection error for inspect request", nullptr);
//         std::vector<Byte> stlResponse = PutTlsTransactionAndGetResponse(poSocket,oBuffer,2*60*1000);
//         if(0==stlResponse.size())
//             _ThrowBaseException("No response for inspect request", nullptr);
        
//         StructuredBuffer oResponse(stlResponse);
//         strJobs = oResponse.GetString("Payload");
//         poSocket->Release();
//         poSocket = nullptr;
//     }
    
//     catch (const BaseException & c_oBaseException)
//     {
//         ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
//     }

//     catch (...)
//     {
//         ::RegisterUnknownException(__func__, __FILE__, __LINE__);
//     }
    
//     if (nullptr != poSocket)
//     {
//         poSocket->Release();
//         poSocket = nullptr;
//     }
// }

// void __thiscall Frontend::HandleGetTable(
//     _in std::string & strVMID,
//     _in std::string & strTables
//     )
// {
//     StructuredBuffer oBuffer;
//     oBuffer.PutInt8("Type", eGETTABLE);
    
//     TlsNode * poSocket = nullptr;
    
//     try
//     {
//         poSocket = TlsConnectToNetworkSocket(m_stlConnectionMap[strVMID].c_str(), m_stlPortMap[strVMID]);
//         _ThrowIfNull(poSocket, "Tls connection error for getTable", nullptr);
//         std::vector<Byte> stlResponse = PutTlsTransactionAndGetResponse(poSocket,oBuffer,2*60*1000);
//         if(0==stlResponse.size())
//             _ThrowBaseException("No response for getTable request", nullptr);

//         StructuredBuffer oResponse(stlResponse);
//         strTables = oResponse.GetString("Payload");
//         poSocket->Release();
//         poSocket = nullptr;
//     }
    
//     catch (const BaseException & c_oBaseException)
//     {
//         ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
//     }

//     catch (...)
//     {
//         ::RegisterUnknownException(__func__, __FILE__, __LINE__);
//     }
    
//     if (nullptr != poSocket)
//     {
//         poSocket->Release();
//         poSocket = nullptr;
//     }
// }

/********************************************************************************************
 *
 * @class EngineCLI
 * @function HandleQuit
 * @param [in] oBuffer Reference of the structured buffer going to be send
 * @brief Prepare the structured buffer going to be send for quitting
 *
 ********************************************************************************************/

void __thiscall Frontend::HandleQuit(void)
{
    StructuredBuffer oBuffer;

    oBuffer.PutString("EndPoint", "JobEngine");
    oBuffer.PutByte("RequestType", (Byte)EngineRequest::eVmShutdown);
    
    for(auto const& i : m_stlConnectionMap)
    {
        try
        {
            this->SendDataToJobEngine(i.first, oBuffer);
        }

        catch (const BaseException & c_oBaseException)
        {
            ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
        }

        catch (...)
        {
            ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        }
    }

    std::lock_guard<std::mutex> lock(m_stlFlagMutex);
    m_fStop = true;
}

void __thiscall Frontend::HandlePushData(
    _in std::string & strVMID,
    _in std::vector<std::string>& stlInputIds,
    _in std::vector<std::vector<Byte>> & stlInputVars
    )
{
    std::cout<<"push data: "<<std::endl;
    for(size_t i=0; i<stlInputIds.size(); i++)
    {
        StructuredBuffer oBuffer;
    
        oBuffer.PutByte("RequestType", (Byte)EngineRequest::ePushdata);
        oBuffer.PutString("EndPoint", "JobEngine");
        oBuffer.PutString("DataId", stlInputIds[i]);
        std::cout<<"dataid: "<<stlInputIds[i]<<"length: "<<stlInputVars[i].size()<<std::endl;
        oBuffer.PutBuffer("Data", stlInputVars[i]);

        try
        {
            this->SendDataToJobEngine(strVMID, oBuffer);
        }

        catch (const BaseException & c_oBaseException)
        {
            ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
        }

        catch (...)
        {
            ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        }
    }  
}

/********************************************************************************************
 *
 * @class Frontend
 * @function PushUserDataToJob
 * @brief Push cached user data to a job
 * @param[in] oJob - The job we want to push data to
 * @param[in] oUserParameter - The GUID of the user data to send to the job engine
 *
 ********************************************************************************************/
void __thiscall Frontend::PushUserDataToJob(
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

//do not know the purpose of "ValuesExpected" and "ValueIndex", disable?
void __thiscall Frontend::HandleSetParameters(
    _in std::string& strVMID, 
    _in std::string& strFNID, 
    _in std::string& strJobID, 
    _in std::vector<std::string>stlParams
    )
{
    std::vector<std::string> stlInputIds = m_stlFNTable[strFNID]->GetInput();
    std::cout<<"set parameter: "<<strJobID<<std::endl;

    for(size_t i=0; i<stlParams.size(); i++)
    {
        StructuredBuffer oBuffer;
        oBuffer.PutByte("RequestType", (Byte)EngineRequest::eSetParameters);
        oBuffer.PutString("EndPoint", "JobEngine");
        oBuffer.PutString("JobUuid", strJobID);
        oBuffer.PutString("ParameterUuid", stlInputIds[i]);
        oBuffer.PutString("ValueUuid", stlParams[i]);
        oBuffer.PutUnsignedInt32("ValuesExpected", 1);
        oBuffer.PutUnsignedInt32("ValueIndex", 0);
        
        try
        {
            this->SendDataToJobEngine(strVMID, oBuffer);
        }

        catch (const BaseException & c_oBaseException)
        {
            ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
        }

        catch (...)
        {
            ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        }

    }
}

void __thiscall Frontend::HandlePullData(
    _in std::string & strVMID,
    _in std::string & strJobID,
    _in std::string & strFNID
    )
{
    std::cout<<"pull data: "<<strJobID<<std::endl;
    std::vector<std::string> stlOutputIDs = m_stlFNTable[strFNID]->GetOutput();
    std::vector<std::string> stlOutputConf = m_stlFNTable[strFNID]->GetOutputConfidential();

    for(size_t i=0; i<stlOutputIDs.size(); i++)
    {
        if(stlOutputConf[i].compare("0")==0)
        {
            StructuredBuffer oBuffer;
            std::string strOutputFilename = strJobID + "." + stlOutputIDs[i];
        
            oBuffer.PutByte("RequestType", (Byte)EngineRequest::ePullData);
            oBuffer.PutString("EndPoint", "JobEngine");
            oBuffer.PutString("Filename", strOutputFilename);
            
            try
            {
                this->SendDataToJobEngine(strVMID, oBuffer);
                std::cout<<"pull data for: "<<strOutputFilename<<std::endl;
            }
            
            catch (const BaseException & c_oBaseException)
            {
                ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
            }

            catch (...)
            {
                ::RegisterUnknownException(__func__, __FILE__, __LINE__);
            }
        }
    }
}

void __thiscall Frontend::QueryResult(
    _in std::string& strJobID,
    _in std::string& strFNID,
    _inout std::map<std::string, int>& stlOutput
)
{
    std::cout<<"query result: "<<strJobID<<std::endl;
    std::vector<std::string> stlOutputID = m_stlFNTable[strFNID]->GetOutput();
    std::vector<std::string> stlOutputConf = m_stlFNTable[strFNID]->GetOutputConfidential();

    for(size_t i =0; i<stlOutputID.size(); i++)
    {
    
        std::string strDataID = strJobID + "." + stlOutputID[i];

        std::cout<<"query result data id: "<<strDataID<<std::endl;

        if(stlOutputConf[i].compare("0")==0)
        {
            while(m_stlResultSet.end()==m_stlResultSet.find(strDataID))
            {
                std::this_thread::sleep_for(std::chrono::milliseconds(2000));
                std::cout<<"waiting for result: "<<strDataID<<std::endl;
            }
            stlOutput.emplace(strDataID, 0);
        }
        else
        {
            stlOutput.emplace(strDataID, 1);
        }
    }
}

JobStatusSignals __thiscall Frontend::QueryJobStatus(
    _in std::string& strJobID
)
{
    //std::cout<<"query job status: "<<strJobID<<" : "<<m_stlJobStatusMap[strJobID]<<std::endl;
    std::lock_guard<std::mutex> lock(m_stlJobStatusMapMutex);
    return m_stlJobStatusMap[strJobID];
}

std::map<std::string, std::string> __thiscall Frontend::QueryDataset(
    _in std::string& strVMID
)
{
    return m_stlDataTableMap[strVMID];
}

// void __thiscall Frontend::HandleDeleteData(
//     _in std::string & strVMID,
//     _in std::vector<std::string> & stlvarID   
//     )
// {
//     //TODO
//     StructuredBuffer oBuffer;
    
//     oBuffer.PutInt8("Type", eDELETEDATA);
//     oBuffer.PutString("VMID", strVMID);
    
//     StructuredBuffer oVars;
//     VecToBuf<std::vector<std::string>>(stlvarID, oVars);
//     oBuffer.PutStructuredBuffer("Vars", oVars);
    
//     TlsNode * poSocket = nullptr;
    
//     try
//     {
//         poSocket = TlsConnectToNetworkSocket(m_stlConnectionMap[strVMID].c_str(), m_stlPortMap[strVMID]);
//         _ThrowIfNull(poSocket, "Tls connection error for DeleteData", nullptr);
//         std::vector<Byte> stlResponse = PutTlsTransactionAndGetResponse(poSocket,oBuffer,2*60*1000);
//         // Make sure to release the socket
//         poSocket->Release();
//         poSocket = nullptr;
//     }
    
//     catch (const BaseException & c_oBaseException)
//     {
//         ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
//     }

//     catch (...)
//     {
//         ::RegisterUnknownException(__func__, __FILE__, __LINE__);
//     }

//     if (nullptr != poSocket)
//     {
//         poSocket->Release();
//         poSocket = nullptr;
//     }
// }

//msg field
//"SafeObjectUuid"
//"Payload"
//"InputParameterList"
//"OutputParameterList"
//The last two to substitue "ParameterList", need to have a module in structuredbuffer to handle vector of string.

void __thiscall Frontend::HandlePushSafeObject(
    _in std::string & strVMID,
    _in std::string & strFNID
    )
{
    std::cout<<"push safe object: "<<strFNID<<std::endl;
    StructuredBuffer oBuffer;

    oBuffer.PutByte("RequestType", (Byte)EngineRequest::ePushSafeObject);
    oBuffer.PutString("EndPoint", "JobEngine");

    oBuffer.PutString("SafeObjectUuid", strFNID);
    oBuffer.PutString("Title", m_stlFNTable[strFNID]->GetTitle());
    oBuffer.PutString("Description", m_stlFNTable[strFNID]->GetDescription());

    std::string strCode =  m_stlFNTable[strFNID]->GetScript();
    oBuffer.PutBuffer("Payload", (Byte*)strCode.c_str(), strCode.size());

    std::vector<std::string> stlInputIDs = m_stlFNTable[strFNID]->GetInput();
    std::vector<std::string> stlOutputIDs = m_stlFNTable[strFNID]->GetOutput();

    StructuredBuffer oInputParams;
    for(size_t i = 0; i<stlInputIDs.size(); i++)
    {
        StructuredBuffer oInputElement;
        oInputElement.PutString("Uuid", stlInputIDs[i]);
        //oInputElement.PutString("Description", "");
        oInputParams.PutStructuredBuffer(std::to_string(i).c_str(), oInputElement);
    }
    oBuffer.PutStructuredBuffer("ParameterList", oInputParams);

    StructuredBuffer oOutputParams;
    for(size_t i = 0; i<stlOutputIDs.size(); i++)
    {
        StructuredBuffer oOutputElement;
        oOutputElement.PutString("Uuid", stlOutputIDs[i]);
        //oInputElement.PutString("Description", "");
        oOutputParams.PutStructuredBuffer(std::to_string(i).c_str(), oOutputElement);
    }
    oBuffer.PutStructuredBuffer("OutputParameters", oOutputParams);

    try
    {
        this->SendDataToJobEngine(strVMID, oBuffer);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
}

void __thiscall Frontend::RegisterSafeObject(
    _in std::string& strFilePath
    )
{
    for (const auto & entry : std::filesystem::directory_iterator(strFilePath))
    {
        std::cout<<"start"<<std::endl;
        std::string strFilename = entry.path().string();
        std::cout<<strFilename<<std::endl;
        std::ifstream stlFNFile;
        stlFNFile.open(strFilename, (std::ios::in | std::ios::binary | std::ios::ate));
        unsigned int unFileSizeInBytes = (unsigned int)stlFNFile.tellg();
        std::cout<<unFileSizeInBytes<<std::endl;
        std::vector<Byte> stlBuffer;
        stlBuffer.resize(unFileSizeInBytes);
        //stlFNFile.unsetf(std::ios::skipws);
        stlFNFile.seekg(0, std::ios::beg);
        stlFNFile.read((char*)stlBuffer.data(), unFileSizeInBytes);
        //stlBuffer.insert(stlBuffer.begin(),std::istream_iterator<Byte>(stlFNFile), std::istream_iterator<Byte>());
        stlFNFile.close();

        std::cout<<"file read done"<<std::endl;
        StructuredBuffer oSafeObject(stlBuffer);
        std::cout<<"safe obj created"<<std::endl;
        std::unique_ptr<SafeObject> poFN = std::make_unique<SafeObject>(oSafeObject);
        std::string strFNID = poFN->GetSafeObjectID();
        std::cout<<strFNID<<" created"<<std::endl;
        m_stlFNTable.emplace(strFNID, std::move(poFN));
        std::cout<<"end"<<std::endl;
    }
}


/********************************************************************************************
 *
 * @class Frontend
 * @function SendDataToJobEngine
 * @param [in] strVMID Id of the VM to send the data to to
 * @param [in] c_oStructuredBuffer StructuredBUffer to send
 * @brief Prepare the structured buffer going to be send for quitting
 *
 ********************************************************************************************/
void __thiscall Frontend::SendDataToJobEngine(
    _in const std::string& strVMID,
    _in StructuredBuffer & c_oStructuredBuffer
)
{
    __DebugFunction();

    try
    {
        std::lock_guard<std::mutex> lock(*m_stlConnectionMutexMap.at(strVMID).get());
        ::PutTlsTransaction(m_stlConnectionMap[strVMID].get(), c_oStructuredBuffer);
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
 * @class Frontend
 * @function SendSafeObjectToJobEngine
 * @param [in] JobInformation The job to send this data to
 * @brief Send a structured buffer to a job that contains our safe object
 *
 ********************************************************************************************/
void __thiscall Frontend::SendSafeObjectToJobEngine(
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
 * @class Frontend
 * @function SetParameterOnJob
 * @param [in] JobInformation The job to send this data to
 * @param [in] Guid The guid of the parameter to set
 * @param [in] Guid The value of the parameter's guid to set to
 * @brief Send a structured buffer to a job that will tell the job what the GUID for an input
 *        parameter is
 *
 ********************************************************************************************/
void __thiscall Frontend::SetParameterOnJob(
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
 * @class Frontend
 * @function SendDataToJob
 * @param [in] JobInformation The job to send this data to
 * @param [in] StructuredBuffer The data to send
 * @brief Send a structured buffer to a job
 *
 ********************************************************************************************/
void __thiscall Frontend::SendDataToJob(
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
