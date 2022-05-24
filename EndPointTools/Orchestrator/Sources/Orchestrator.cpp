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

#include "BinaryFileHandlers.h"
#include "CurlRest.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "HttpRequestParser.h"
#include "FileUtils.h"
#include "JsonParser.h"
#include "JobOutputParameter.h"
#include "Orchestrator.h"
#include "SocketClient.h"
#include "StructuredBuffer.h"
#include "TlsClient.h"
#include "TlsTransactionHelperFunctions.h"

#include <algorithm>
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
 * @function GetJsonForStructuredBufferMap
 * @brief Helper function to create a JSON str out of a map of GUID:StructuredBuffer pairs
 * @param [in] std::unordered_map - The map containg the GUID:StructuredBuffer pairs
 * @return std::string - The JSON representation of the map, or "" on error
 *
 ********************************************************************************************/
static std::string __stdcall GetJsonForStructuredBufferMap(
    _in const std::unordered_map<std::string, StructuredBuffer> & c_stlStructuredBufferMap
    ) throw()
{
    __DebugFunction();

    std::string strJson{""};

    try
    {
        if (0 < c_stlStructuredBufferMap.size())
        {
            StructuredBuffer oAllObjects;
            for (const auto & oElement: c_stlStructuredBufferMap)
            {
                Guid oEntryGuid(oElement.first);
                oAllObjects.PutStructuredBuffer(oEntryGuid.ToString(eHyphensOnly).c_str(), oElement.second);
            }

            strJson = ::ConvertStructuredBufferToJson(oAllObjects);
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

    return strJson;
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
    _in const std::unordered_map<std::string, TableInformation> & c_stlStructuredBufferMap
    ) throw()
{
    __DebugFunction();

    std::string strJson{""};

    try
    {
        if (0 < c_stlStructuredBufferMap.size())
        {
            StructuredBuffer oAllObjects;
            for (const auto & oElement: c_stlStructuredBufferMap)
            {
                oAllObjects.PutStructuredBuffer(oElement.first.c_str(), oElement.second.m_oInformation);
            }

            strJson = ::ConvertStructuredBufferToJson(oAllObjects);
        }
    }

    catch (const BaseException & oBaseException)
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return strJson;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function Default constructor
 *
 ********************************************************************************************/
Orchestrator::Orchestrator(void) throw()
{
    __DebugFunction();
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function Destructor
 *
 ********************************************************************************************/
Orchestrator::~Orchestrator(void) throw()
{
    __DebugFunction();

    //m_oSessionManager.Logout();
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function Login
 * @brief Log into the remote with the email and password supplied to the port and IP
 * @return unsigned int - status code of the login operation
 *
 ********************************************************************************************/
unsigned int __thiscall Orchestrator::Login(
    _in const std::string & c_strEmail,
    _in const std::string & c_strUserPassword,
    _in int nServerPort,
    _in const std::string & c_strServerIpAddress
    ) throw()
{
    __DebugFunction();

    // Regardless of the type of failure, authentication functions should always return either
    // 201 on success, or 401 on failure (regardless of the type of failure).
    uint64_t unStatus{401};

    try
    {
        // First we need to validate the incoming parameters
        _ThrowBaseExceptionIf((0 == c_strEmail.size()), "ERROR: Invalid email parameter (size = 0)", nullptr);
        _ThrowBaseExceptionIf((0 == c_strUserPassword.size()), "ERROR: Invalid password parameter (size = 0)", nullptr);
        _ThrowBaseExceptionIf((0 == c_strServerIpAddress.size()), "ERROR: Invalid server ip address parameter (size = 0)", nullptr);
        _ThrowBaseExceptionIf((0 >= nServerPort), "ERROR: Invalid server port number parameter (0 >= nServerPort)", nullptr);
        // Call the session manager to login
        _ThrowBaseExceptionIf((false == m_oSessionManager.Login(c_strEmail, c_strUserPassword, c_strServerIpAddress, (Word) LOWORD(nServerPort))), "ERROR: Failed to login", nullptr);
        // Get our list of digital contracts
        this->CacheDigitalContractsFromRemote();
        // Get our list of datasets
        this->CacheDatasetsFromRemote();
        // If we get here, everything was a success
        unStatus = 201;
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

    return unStatus;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function ExitCurrentSession
 * @brief Remove information related to our current lgoged in session, and stop EOSB rotation
 *
 ********************************************************************************************/
void __thiscall Orchestrator::ExitCurrentSession(void) throw()
{
    __DebugFunction();

    // First we need to logout
    m_oSessionManager.Logout();
    // Now we need to clean up cached information
    m_stlOutstandingImplicitPullRequests.clear();
    m_stlAvailableSafeFunctions.clear();
    m_stlDigitalContracts.clear();
    m_stlAvailableDatasets.clear();
    m_stlAvailableTables.clear();
    m_stlProvisionInformation.clear();
    m_stlJobInformation.clear();
    m_stlPushedData.clear();
    m_stlJobResults.clear();
    m_stlSecureNodeConnections.clear();
    m_oJobMessageQueue.ClearAllMessages();
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetCurrentEosb
 * @brief Return the EOSB currently being used
 * @return std::string - The value of the EOSB currently being used
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::GetCurrentAccessToken(void) const throw()
{
    __DebugFunction();

    return m_oSessionManager.GetAccessToken();
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetSafeFunctions
 * @brief Build a list of safe functions available
 * @return std::string - Containing a list of our safe functions in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::GetSafeFunctions(void) const throw()
{
    __DebugFunction();

    return ::GetJsonForStructuredBufferMap(m_stlAvailableSafeFunctions);
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetDatasets
 * @brief Lookup in our local cache for the datasets we have and return them as a JSON string
 * @return std::string - Containing a list of our datasets in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::GetDatasets(void) const throw()
{
    __DebugFunction();

    return ::GetJsonForStructuredBufferMap(m_stlAvailableDatasets);
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetDigitalContracts
 * @brief Lookup in our local cache for the digital contracts we have and return them as a JSON string
 * @return std::string - Containing a JSON dictionary of our DCs in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::GetDigitalContracts(void) const throw()
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
std::string __thiscall Orchestrator::GetTables(void) const throw()
{
    __DebugFunction();

    return ::GetJsonForStructuredBufferMap(m_stlAvailableTables);
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function LoadSafeObjects
 * @brief Cache all the safeobjects found in a local folder
 *
 ********************************************************************************************/
int __thiscall Orchestrator::LoadSafeObjects(
    _in const std::string & c_strSafeObjectDirectory
    ) throw()
{
    __DebugFunction();

    int nReturnValue{0};

    try
    {
        std::error_code stlFileErrorCode;
        if (false == std::filesystem::exists(c_strSafeObjectDirectory, stlFileErrorCode))
        {
            if (stlFileErrorCode)
            {
                nReturnValue = stlFileErrorCode.value();
            }
            else
            {
                nReturnValue = -1;
            }
        }
        else
        {
            for (const auto & oEntry : std::filesystem::directory_iterator(c_strSafeObjectDirectory))
            {
                // Only load objects that have the right extension
                if (oEntry.path().extension() == ".safe")
                {
                    // We use a nested try...catch block since it's possible that some of the
                    // safe functions are malformed and we don't want to end up skipping a whole
                    // bunch of files if only one is bad. This ensures that all safe function
                    // files that are loadable will in fact be loaded
                    try
                    {
                        BinaryFileReader oInputFile(oEntry.path().string());
                        std::vector<Byte> stlFileContents = oInputFile.ReadAll();
                        if (0 < stlFileContents.size())
                        {
                            StructuredBuffer oSafeObject(stlFileContents);
                            Guid oSafeObjectGuid(oSafeObject.GetString("Uuid"));
                            m_stlAvailableSafeFunctions.emplace(oSafeObjectGuid.ToString(eRaw), oSafeObject);
                            ++nReturnValue;
                        }
                    }

                    catch (const BaseException & oBaseException )
                    {
                        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
                    }

                    catch (const std::exception & c_oException)
                    {
                        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
                    }

                    catch ( ... )
                    {
                        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
                    }
                }
            }
        }
    }

    catch (const BaseException & oBaseException )
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }

    catch ( ... )
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return nReturnValue;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function ProvisionSecureComputationalNode
 * @brief Send a request to provision a Secure Computational Node (SCN)
 * @param[in] c_strDigitalContractIdentifier The GUID of the digital contract to provision with the SCN
 * @param[in] std::string - Eventually the GUID of the dataset in the family to provision, un-used today
 * @return std::string - Containing a list of our safe functions in the form: GUID:Metadata
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::ProvisionSecureComputationalNode(
    _in const std::string & c_strVirtualMachineName,
    _in const std::string & c_strDigitalContractIdentifier,
    _in const std::string & c_strDatasetIdentifier,
    _in const std::string & c_strVirtualMachineType
    )
{
    __DebugFunction();

    bool fProvisionResult{false};
    StructuredBuffer oReturnStructuredBuffer;

    try
    {
        Guid oDatasetGuid(c_strDatasetIdentifier);
        Guid oDigitalContractGuid(c_strDigitalContractIdentifier);

        // Prepare the API call
        std::string strVerb = "POST";
        std::string strApiUrl = "/secure-computation-node";

        StructuredBuffer oJsonRequest;
        oJsonRequest.PutString("name", c_strVirtualMachineName);
        oJsonRequest.PutString("digital_contract_id", oDigitalContractGuid.ToString(eHyphensOnly));
        oJsonRequest.PutString("dataset_id", oDatasetGuid.ToString(eHyphensOnly));
        oJsonRequest.PutString("type", c_strVirtualMachineType);
        std::string strContent = ::ConvertStructuredBufferToJson(oJsonRequest);
        std::vector<std::string> stlListOfHeaders;
        stlListOfHeaders.push_back("Authorization: Bearer " + this->GetCurrentAccessToken());
        stlListOfHeaders.push_back("Content-Type: application/json");

        // Make the API call and get REST response
        std::vector<Byte> stlRestResponse = ::RestApiCall(m_oSessionManager.GetServerIpAddress(), m_oSessionManager.GetServerPortNumber(), strVerb, strApiUrl, strContent, true, stlListOfHeaders);
        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());

        if (true == oResponse.IsElementPresent("detail", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            // If the API call contains a message, make sure to persist it inside the return
            // Json
            oReturnStructuredBuffer.PutString("detail", oResponse.GetString("detail"));
        }

        if (true == oResponse.IsElementPresent("id", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            std::string strRawProvisionGuid = oResponse.GetString("id");

            __DebugAssert(m_stlProvisionInformation.end() == m_stlProvisionInformation.find(strRawProvisionGuid));

            m_stlProvisionInformation[strRawProvisionGuid].strProvisionStatus = "REQUESTED";
            m_stlProvisionInformation[strRawProvisionGuid].oHostedDataset.strDatsetGuid = c_strDatasetIdentifier;
            m_stlProvisionInformation[strRawProvisionGuid].strDigitalContractGUID = c_strDigitalContractIdentifier;

            oReturnStructuredBuffer.PutString("SCNGuid", strRawProvisionGuid);
            // If we get here, everything has worked properly.
            fProvisionResult = true;
        }
    }

    catch (const BaseException & oBaseException )
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }

    catch ( ... )
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    // No matter what happens, we need to be able to return a Status on the provisioning
    // result. This needs to be done after the try..catch block, since throwing exceptions
    // should effectively return a Status of false
    oReturnStructuredBuffer.PutBoolean("Status", fProvisionResult);

    return ::ConvertStructuredBufferToJson(oReturnStructuredBuffer);
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
    _in const std::string & c_strSafeFunctionIdentifier
    )
{
    __DebugFunction();

    std::string strNewJobId{""};

    try
    {
        // We must be logged in to start a job
        if ("" != m_oSessionManager.GetAccessToken())
        {
            Guid oSafeFunctionGuid(c_strSafeFunctionIdentifier);
            if (m_stlAvailableSafeFunctions.end() != m_stlAvailableSafeFunctions.find(oSafeFunctionGuid.ToString(eRaw)))
            {
                std::vector<std::string> stlInputParameters;
                Guid oJobIdentifier(eJobIdentifier);
                StructuredBuffer oSafeFunction = m_stlAvailableSafeFunctions[oSafeFunctionGuid.ToString(eRaw)];
                StructuredBuffer oInputParameters = oSafeFunction.GetStructuredBuffer("InputParameters");
                for (const std::string & strInputParameterId : oInputParameters.GetNamesOfElements() )
                {
                    stlInputParameters.push_back(oInputParameters.GetStructuredBuffer(strInputParameterId.c_str()).GetString("Uuid"));
                }
                // When returning GUIDs to the user we return human readable versions
                strNewJobId = oJobIdentifier.ToString(eHyphensAndCurlyBraces);
                // We make a unique pointer because mutexes are not trivially copyable
                m_stlJobInformation.emplace(oJobIdentifier.ToString(eRaw), new JobInformation(oJobIdentifier, oSafeFunctionGuid, stlInputParameters, m_oJobMessageQueue));
            }
        }
    }

    catch (const BaseException& oBaseException)
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
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
 * @param[in] c_strJobIdentifier The GUID of the safe function to run
 * @return std::string - The status of the current job
 *
 ********************************************************************************************/
std::string Orchestrator::GetJobStatus(
    _in const std::string & c_strJobIdentifier
    ) const
{
    __DebugFunction();

    std::string strStatus = "Job not found";

    try
    {
        Guid oJobGuid(c_strJobIdentifier);

        if (m_stlJobInformation.end() != m_stlJobInformation.find(oJobGuid.ToString(eRaw)))
        {
            __DebugAssert(nullptr != m_stlJobInformation.at(oJobGuid.ToString(eRaw)).get());
            std::lock_guard<JobInformation> stlLock(*m_stlJobInformation.at(oJobGuid.ToString(eRaw)).get());
            strStatus = m_stlJobInformation.at(oJobGuid.ToString(eRaw))->GetJobStatus();
        }
    }

    catch (const BaseException& oBaseException)
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return strStatus;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function SetParameter
 * @brief Get the job status for a given job id
 * @param[in] c_strJobIdentifier The GUID of the job whose parameter to set
 * @param[in] c_strInputParamId The input parameter to set
 * @param[in] c_strParamValue The value for the input parameter
 * @return std::string - The ID for the parameter if it was set, blank if it wasn't
 *
 ********************************************************************************************/
std::string Orchestrator::SetParameter(
    _in const std::string & c_strJobIdentifier,
    _in const std::string & c_strInputParamId,
    _in const std::string & c_strParamValue
    )
{
    __DebugFunction();

    std::string strParameterIdentifier{""};

    try
    {
        Guid oJobIdentifier(c_strJobIdentifier);
        auto stlJobInformation = m_stlJobInformation.find(oJobIdentifier.ToString(eRaw));
        if (m_stlJobInformation.end() != stlJobInformation)
        {
            __DebugAssert(nullptr != stlJobInformation->second.get());

            JobInformation & oJobInformation = *stlJobInformation->second;
            std::lock_guard<JobInformation> stlLock(oJobInformation);
            Guid oInputParameterGuid(c_strInputParamId);

            if (false == ::IsJobOutputParameter(c_strParamValue))
            {
                Guid oParameterGuid(c_strParamValue);

                if (true == oJobInformation.SetInputParameter(c_strInputParamId, c_strParamValue))
                {
                    strParameterIdentifier = oJobIdentifier.ToString(eHyphensAndCurlyBraces) + "." + oInputParameterGuid.ToString(eHyphensAndCurlyBraces);
                    this->UpdateJobIPAddressForParameter(oJobInformation, oParameterGuid);
                }
            }
            else
            {
                // Convert from whatever format the user has passed in to Raw
                JobOutputParameter oJobOutputPieces = ::ParseStringToJobOutput(c_strParamValue);
                std::string strRawOutputParam = oJobOutputPieces.ToString();
                if (true == oJobInformation.SetInputParameter(c_strInputParamId, strRawOutputParam))
                {
                    strParameterIdentifier = oJobIdentifier.ToString(eHyphensAndCurlyBraces) + "." + oInputParameterGuid.ToString(eHyphensAndCurlyBraces);
                }

                // We aren't aware of this parameter yet, pull it
                if (m_stlJobResults.end() == m_stlJobResults.find(strRawOutputParam))
                {
                    // Sent an implicit pull to ensure the job engine encrypts the data sent back
                    this->PullJobData(strRawOutputParam, false);
                    m_stlOutstandingImplicitPullRequests.insert(strRawOutputParam);
                }
                else
                {
                    oJobInformation.SetOutputJobParameterReady(strRawOutputParam);
                }
            }

            // All our parameters are set, none require a dataset, and we don't have an IP try
            // to get one
            if ((true == oJobInformation.AllInputParametersSet())&&(false == oJobInformation.RequiresDataset())&&("" == oJobInformation.GetTargetIP()))
            {
                this->UpdateJobIPAddressForAnySecureComputationalNode(oJobInformation);
            }

            // We have everything we need to submit this job, start it up
            if (true == oJobInformation.ReadyToExcute())
            {
                StartJobRemoteExecution(oJobInformation);
            }
        }
    }

    catch (const BaseException & oBaseException)
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
        strParameterIdentifier = "";
    }

    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        strParameterIdentifier = "";
    }

    return strParameterIdentifier;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function UpdateJobIPAddressForParameter
 * @brief Given a job and Guid, update the IP if it's available
 * @param[in] oJob The job information object for the IP address to update
 * @param[in] c_oParameterGuid The value of the parameter whose IP address we want to update
 *
 ********************************************************************************************/
void __thiscall Orchestrator::UpdateJobIPAddressForParameter(
    _in JobInformation& oJob,
    _in const Guid& c_oParameterGuid
    )
{
    std::optional<Guid> oTargetSecureComputationalNode;

    if ( eTable == c_oParameterGuid.GetObjectType() )
    {
        oTargetSecureComputationalNode = GetSecureComputationalNodeServingTable(c_oParameterGuid);
    }
    else if ( eUserSuppliedData != c_oParameterGuid.GetObjectType() )
    {
        // Assume anything else is a dataset guid until we have the new types in the data annotation tool
        oTargetSecureComputationalNode = GetSecureComputationalNodeServingDataset(c_oParameterGuid);
    }

    if ( oTargetSecureComputationalNode.has_value() )
    {
        auto oSecureNodeInformation = m_stlProvisionInformation.find(oTargetSecureComputationalNode.value().ToString(eRaw));
        __DebugAssert(m_stlProvisionInformation.end() != oSecureNodeInformation);

        std::string strTargetIP = oSecureNodeInformation->second.strRemoteIpAddress;
        _ThrowBaseExceptionIf(((oJob.GetTargetIP() != "") && (oJob.GetTargetIP() != strTargetIP)), "Job already has an IP target", nullptr);

#ifdef DEBUG_PRINTS
        std::cout << "Assinging IP " << strTargetIP << " to job " << oJob.GetJobId().ToString(eHyphensAndCurlyBraces) << std::endl;
#endif
        oJob.SetTargetIP(strTargetIP);

        // We've assigned this dataset to a job, increase its usage count
        oSecureNodeInformation->second.oHostedDataset.unUsageCount++;
    }
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function UpdateJobIPAddressForAnySecureComputationalNode
 * @brief Try to find an IP of any SCN that can execute this job
 * @param[in] oJob The job information object for the IP address to update
 *
 ********************************************************************************************/
void Orchestrator::UpdateJobIPAddressForAnySecureComputationalNode(
    _in JobInformation & oJob
    )
{
    __DebugFunction();

    std::optional<Guid> oTargetSecureComputationalNode{GetSecureComputationalNodeWithoutDataset()};

    if ( oTargetSecureComputationalNode.has_value() )
    {
        auto oSecureNodeInformation = m_stlProvisionInformation.find(oTargetSecureComputationalNode.value().ToString(eRaw));
        __DebugAssert(m_stlProvisionInformation.end() != oSecureNodeInformation);

        std::string strTargetIP = oSecureNodeInformation->second.strRemoteIpAddress;
        _ThrowBaseExceptionIf(((oJob.GetTargetIP() != "") && (oJob.GetTargetIP() != strTargetIP)), "Job already has an IP target", nullptr);

#ifdef DEBUG_PRINTS
        std::cout << "Assinging IP " << strTargetIP << " to job " << oJob.GetJobId().ToString(eHyphensAndCurlyBraces) << std::endl;
#endif
        oJob.SetTargetIP(strTargetIP);

        // We've assigned this dataset to a job, increase its usage count
        oSecureNodeInformation->second.oHostedDataset.unUsageCount++;
    }
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function DeprovisionDigitalContract
 * @brief Deprovision the passed in digital contract GUID
 * @param[in] oJob The job information object for the IP address to update
 * @return Wether the deprovision was successful or not
 *
 ********************************************************************************************/
bool __thiscall Orchestrator::DeprovisionSecureComputationNode(
    _in const std::string & c_strSecureComputationNodeId
    )
{
    bool fRetrurnValue{false};
    try
    {
        std::string strVerb = "DELETE";
        std::string strApiUrl = "/secure-computation-node/" + c_strSecureComputationNodeId;

        std::vector<std::string> stlListOfHeaders;
        stlListOfHeaders.push_back("Authorization: Bearer " + m_oSessionManager.GetAccessToken());
        std::vector<Byte> stlRestResponse = ::RestApiCall(m_oSessionManager.GetServerIpAddress(), m_oSessionManager.GetServerPortNumber(), strVerb, strApiUrl, "", true, stlListOfHeaders);
        // TODO: Prawal check the response code
    }
    catch(const BaseException& oBaseException)
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
        fRetrurnValue = false;
    }
    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        fRetrurnValue = false;
    }

    return fRetrurnValue;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetIPAddressForJob
 * @brief Setup everything we need on the remote job engine to start a job
 * @param[in] c_strJobGUID The job GUID whose IP address we want to get
 * @return std::string - The IP address of the job, "" if none found or error
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::GetIPAddressForJob(
    _in const std::string& c_strJobGUID
    )
{
    std::string strReturn{""};
    try
    {

        Guid oJobGUID(c_strJobGUID);

        auto oJobItr = m_stlJobInformation.find(oJobGUID.ToString(eRaw));
        if ( m_stlJobInformation.end() != oJobItr )
        {
            strReturn = oJobItr->second->GetTargetIP();
        }
    }
    catch(const BaseException& oBaseException)
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
        strReturn = "";
    }
    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        strReturn = "";
    }
    return strReturn;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function StartJobRemoteExecution
 * @brief Setup everything we need on the remote job engine to start a job
 *
 ********************************************************************************************/
bool __thiscall Orchestrator::StartJobRemoteExecution(
    _in JobInformation & oJob
    ) throw()
{
    __DebugFunction();
    __DebugAssert(oJob.ReadyToExcute());

#ifdef DEBUG_PRINTS
    std::cout << "Job " << oJob.GetJobId().ToString(eHyphensAndCurlyBraces) << " is ready to execute on IP " << oJob.GetTargetIP() << std::endl;
#endif

    bool fJobStarted{false};
    try
    {
        _ThrowBaseExceptionIf((false == oJob.ReadyToExcute()), "Job is not ready to execute", nullptr);
        std::shared_ptr<JobEngineConnection> poJobEngineSocket;
        if ( m_stlSecureNodeConnections.end() == m_stlSecureNodeConnections.find(oJob.GetTargetIP()) )
        {
            std::shared_ptr<TlsNode> poNewSocketConnection{::TlsConnectToNetworkSocket(oJob.GetTargetIP(), REMOTE_JOB_PORT)};

            m_stlSecureNodeConnections.emplace(oJob.GetTargetIP(), new JobEngineConnection(poNewSocketConnection, m_oJobMessageQueue));
            poJobEngineSocket = m_stlSecureNodeConnections[oJob.GetTargetIP()];

            // Send a connect message to the JobEngine
            StructuredBuffer oPushBuffer;
            oPushBuffer.PutByte("RequestType", static_cast<Byte>(EngineRequest::eConnectVirtualMachine));
            oPushBuffer.PutString("Username", "TEST_USERNAME");
            oPushBuffer.PutString("Eosb", m_oSessionManager.GetAccessToken());
            oPushBuffer.PutString("EndPoint", "JobEngine");
            oPushBuffer.PutString("OrchestratorIdentifier", m_oOrchestratorIdentifier.ToString(eRaw));

            ::PutTlsTransaction(poNewSocketConnection.get(), oPushBuffer);
        }
        else
        {
#ifdef DEBUG_PRINTS
            std::cout << "Re-using existing connection" << std::endl;
#endif
            poJobEngineSocket = m_stlSecureNodeConnections[oJob.GetTargetIP()];
        }

        // Establish connection with the remote
        if ( nullptr == poJobEngineSocket )
        {
            std::cout << "Failed to connect to remote " << oJob.GetTargetIP() << std::endl;
        }
        else
        {
            _ThrowBaseExceptionIf((nullptr == poJobEngineSocket), "Failed to connect to remote job engine", nullptr);
            oJob.SetConnection(poJobEngineSocket);
        }

        // Send any data we had cached
        oJob.SendCachedMessages();

        SendSafeObjectToJobEngine(oJob);

        SubmitJob(oJob);

        for ( auto oParameterItr : oJob.GetInputParameterMap() )
        {
            __DebugAssert(oParameterItr.second.has_value());

            Guid oParameterGuid(oParameterItr.first);

            // Parameters that aren't the result of an output parameter can be run
            if ( !IsJobOutputParameter(oParameterItr.second.value()) )
            {
                Guid oParameterValueGuid(oParameterItr.second.value());

                // We need to push this to the remote job engine
                if ( eUserSuppliedData == oParameterValueGuid.GetObjectType() )
                {
                    PushUserDataToJob(oJob, oParameterValueGuid);
                }
                // Set the input parameters on the job engine
                SetParameterOnJob(oJob, oParameterGuid, oParameterValueGuid);
            }
            else
            {
                // We're assuming this is a job output
                __DebugAssert( IsJobOutputParameter(oParameterItr.second.value()));

                JobOutputParameter oOutputParameters = ParseStringToJobOutput(oParameterItr.second.value());
                std::string strParameterString = oOutputParameters.ToString();
                auto stlJobInformationItr = m_stlJobInformation.find(oOutputParameters.m_strJobIdentifier.ToString(eRaw));

                __DebugAssert(m_stlJobInformation.end() != stlJobInformationItr);

                SetJobParameterForJobOutput(oJob, oParameterGuid, strParameterString);
            }
        }

#ifdef DEBUG_PRINTS
        std::cout << "Job " << oJob.GetJobId().ToString(eHyphensAndCurlyBraces) << " has sent all parameters " << std::endl;
#endif

        fJobStarted = true;
    }

    catch(const BaseException& oBaseException)
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
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

    return fJobStarted;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetSecureComputationNodeInformation
 * @brief Get the information about an SCN
 * @param[in] Guid - The SCN's GUID
 * @return VirtualMachineState - The enum of the SCN VM status
 * @function SetParameter
 *
 ********************************************************************************************/
std::string __thiscall Orchestrator::GetSecureComputationNodeInformation(
    _in const std::string & c_strSecureNodeGuid
    )
{
    __DebugFunction();
    std::string strVerb = "GET";
    std::string strApiUrl = "/secure-computation-node/" + c_strSecureNodeGuid;
    std::vector<std::string> stlListOfHeaders;
    stlListOfHeaders.push_back("Authorization: Bearer " + m_oSessionManager.GetAccessToken());
    std::vector<Byte> stlRestResponse = ::RestApiCall(m_oSessionManager.GetServerIpAddress(), m_oSessionManager.GetServerPortNumber(), strVerb, strApiUrl, "", true, stlListOfHeaders);

    StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));
    _ThrowBaseExceptionIf((true != oResponse.IsElementPresent("id", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Error retrieving secure node provision status", nullptr);

    std::string strVirtualMachineState = oResponse.GetString("state");

    // Only extract the IP if this SCN is ready for use
    if ("WAITING_FOR_DATA" == strVirtualMachineState || "READY" == strVirtualMachineState)
    {
        if(true == oResponse.IsElementPresent("ipaddress", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            m_stlProvisionInformation[c_strSecureNodeGuid].strRemoteIpAddress = oResponse.GetString("ipaddress");
        }
    }
    if ( true == oResponse.IsElementPresent("detail", ANSI_CHARACTER_STRING_VALUE_TYPE))
    {
        m_stlProvisionInformation[c_strSecureNodeGuid].strProvisionMessage = oResponse.GetString("detail");
    }

    m_stlProvisionInformation[c_strSecureNodeGuid].strProvisionStatus = strVirtualMachineState;
    return strVirtualMachineState;
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
    if ( "" != m_oSessionManager.GetAccessToken())
    {
        try
        {
            StructuredBuffer oProvisionStatus;
            std::set<std::string> stlSucceededProvisions;
            std::set<std::string> stlInProgressProvisions;
            std::set<std::string> stlFailedProvisions;
            std::set<std::string> stlDeletedProvisions;
            bool fTimedOut{false};

            // We aren't ready, wait and check again
            while ( m_stlProvisionInformation.size() != (stlFailedProvisions.size() + stlSucceededProvisions.size() + stlDeletedProvisions.size()) && !fTimedOut )
            {
                for ( const auto& stlSecureComputationNodeItr : m_stlProvisionInformation )
                {
                    if ( stlSucceededProvisions.end() == stlSucceededProvisions.find(stlSecureComputationNodeItr.first) )
                    {
                        Guid oDigitalContractGuid(stlSecureComputationNodeItr.second.strDigitalContractGUID);
                        std::string strProvisionState = GetSecureComputationNodeInformation(stlSecureComputationNodeItr.first);

                        if ("READY" == strProvisionState || "IN_USE" == strProvisionState || "WAITING_FOR_DATA" == strProvisionState)
                        {
                            stlSucceededProvisions.insert(stlSecureComputationNodeItr.first);
                            stlInProgressProvisions.erase(stlSecureComputationNodeItr.first);
                            stlFailedProvisions.erase(stlSecureComputationNodeItr.first);
                        }
                        else if ( "REQUESTED" == strProvisionState ||
                                  "CREATING" == strProvisionState ||
                                  "INITIALIZING" == strProvisionState ||
                                  "WAITING_FOR_DATA" == strProvisionState )
                        {
                            stlInProgressProvisions.insert(stlSecureComputationNodeItr.first);
                        }
                        else if ( "FAILED" == strProvisionState )
                        {
                            stlFailedProvisions.insert(stlSecureComputationNodeItr.first);
                        }
                        else if ( "DELETED" == strProvisionState )
                        {
                            stlDeletedProvisions.insert(stlSecureComputationNodeItr.first);
                        }
                        else
                        {
                            _ThrowBaseException("Unknown Virtual Machine State %s", strProvisionState.c_str(), nullptr);
                        }
                    }
                }

                // A provision is considered complete whether it succeeded or failed
                if ( m_stlProvisionInformation.size() != (stlDeletedProvisions.size() + stlFailedProvisions.size() + stlSucceededProvisions.size()) )
                {
                    if ( 0 < nTimeoutInMs)
                    {
                        constexpr int c_nTimeoutThreshold{2000};
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
                oSucceededProvisions.PutString(oSucceededItr.c_str(), m_stlProvisionInformation[oSucceededItr].strProvisionMessage);
                ++unProvisionItr;

                // Any job that is waiting for this dataset should be assigned this IP
                for ( auto& oPendingJob : m_stlJobInformation)
                {
                    if (true == oPendingJob.second->JobParameterUsesGuid(Guid(m_stlProvisionInformation[oSucceededItr].oHostedDataset.strDatsetGuid)))
                    {
                        oPendingJob.second->SetTargetIP(m_stlProvisionInformation[oSucceededItr].strRemoteIpAddress);
                    }

                    if ((true == oPendingJob.second->ReadyToExcute())&&(false == oPendingJob.second->IsRunning()))
                    {
                        this->StartJobRemoteExecution(*oPendingJob.second);
                    }
                }
            }
            unProvisionItr = 0;
            for (auto & oInProgressItr : stlInProgressProvisions)
            {
                Guid oProvisionGuid(oInProgressItr);
                oInProgressProvisions.PutString(oProvisionGuid.ToString(eHyphensOnly).c_str(), m_stlProvisionInformation[oInProgressItr].strProvisionMessage);
                ++unProvisionItr;
            }
            unProvisionItr = 0;
            for ( auto& oFailedItr : stlFailedProvisions )
            {
                Guid oProvisionGuid(oFailedItr);
                oFailedProvisions.PutString(oProvisionGuid.ToString(eHyphensOnly).c_str(), m_stlProvisionInformation[oFailedItr].strProvisionMessage);
                ++unProvisionItr;
            }
            // For any SCNs that have gone away, don't report their status any more
            for ( auto& oDeletedItr : stlDeletedProvisions )
            {
                m_stlProvisionInformation.erase(oDeletedItr);
            }

            oProvisionStatus.PutBoolean("AllDone", fAllNodesReady);
            oProvisionStatus.PutStructuredBuffer("Succeeded", oSucceededProvisions);
            oProvisionStatus.PutStructuredBuffer("Failed", oFailedProvisions);
            oProvisionStatus.PutStructuredBuffer("InProgress", oInProgressProvisions);
            strProvisionStatus = ::ConvertStructuredBufferToJson(oProvisionStatus);
        }
        catch(const BaseException& oBaseException )
        {
            ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
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
 * @function GetSecureComputationalNodeServingDataset
 * @brief Get the IP address of a VM serving a dataset's GUID
 * @param[in] Guid - The GUID of the dataset we're looking for
 * @return std::optional<Guid> - An option of a GUID of the SCN serving the dataset
 * 
 * We iterate through SCNs serving datasets, and pick the one which has been used the least
 ********************************************************************************************/
std::optional<Guid> Orchestrator::GetSecureComputationalNodeServingDataset(
    _in const Guid& oDatasetGuid
    ) const
{
    __DebugFunction();
    // Disabled until new data annotation tool is in place
    //__DebugAssert(eDataset == oDatasetGuid.GetObjectType());

    std::optional<Guid> oSecureComputationalNodeGuid;
    unsigned int unMinUsageCount{UINT_MAX};
    for ( auto oDatasetItr : m_stlProvisionInformation)
    {
        if ( Guid(oDatasetItr.second.oHostedDataset.strDatsetGuid) == oDatasetGuid &&
            ( "READY" == oDatasetItr.second.strProvisionStatus) )
        {
            if ( oDatasetItr.second.oHostedDataset.unUsageCount < unMinUsageCount )
            {
                oSecureComputationalNodeGuid = oDatasetItr.first;
                unMinUsageCount = oDatasetItr.second.oHostedDataset.unUsageCount;
            }
        }
    }
    return oSecureComputationalNodeGuid;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetSecureComputationalNodeWithoutDataset
 * @brief Get the IP address of a VM without a dataset to run a job on
 * @param[in] Guid - The GUID of the dataset we're looking for
 * @return std::optional<Guid> - An option of a GUID of the SCN serving the dataset
 *
 * We iterate through SCNs serving datasets, and pick the one which has been used the least
 ********************************************************************************************/
std::optional<Guid> Orchestrator::GetSecureComputationalNodeWithoutDataset() const
{
    std::optional<Guid> oSecureComputationalNodeGuid;
    unsigned int unMinUsageCount{UINT_MAX};
    for ( auto oDatasetItr : m_stlProvisionInformation )
    {
        if ( ( oDatasetItr.second.strProvisionStatus == "READY") )
        {
            if ( oDatasetItr.second.oHostedDataset.unUsageCount < unMinUsageCount )
            {
                oSecureComputationalNodeGuid = oDatasetItr.first;
                unMinUsageCount = oDatasetItr.second.oHostedDataset.unUsageCount;
            }
        }
    }

    return oSecureComputationalNodeGuid;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function GetSecureComputationalNodeServingTable
 * @brief Get the IP address of a VM serving a table's GUID
 * @param[in] std::string - The GUID of the table we're looking for
 * @return std::string - The IP address of the VM hosting the table, "" if we don't find it
 ********************************************************************************************/
std::optional<Guid> Orchestrator::GetSecureComputationalNodeServingTable(
    _in const Guid& oTableGuid
    ) const
{
    __DebugFunction();
    __DebugAssert(eTable == oTableGuid.GetObjectType());

    std::optional<Guid> oSecureComputationalNodeGuid;
    for ( auto oTableItr : m_stlAvailableTables )
    {
        Guid oTableItrGuid(oTableItr.second.m_oInformation.GetString("TableIdentifier"));

        if ( oTableGuid == oTableItrGuid )
        {
            Guid oDatasetGuid(oTableItr.second.m_strParentDataset);
            oSecureComputationalNodeGuid = GetSecureComputationalNodeServingDataset(oDatasetGuid);
            break;
        }
    }

    return oSecureComputationalNodeGuid;
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
        _in const std::string& c_strOutputParameter,
        _in bool fExplicitPull
    ) throw()
{
    __DebugFunction();
    std::string strResult{"Invalid parameter"};
    try
    {
        JobOutputParameter oJobOutput = ::ParseStringToJobOutput(c_strOutputParameter);

        auto oStlJobInformationItr = m_stlJobInformation.find(oJobOutput.m_strJobIdentifier.ToString(eRaw));

        if ( m_stlJobInformation.end() == oStlJobInformationItr )
        {
            strResult = "Job not found";
        }
        else
        {
            __DebugAssert(nullptr != oStlJobInformationItr->second.get());

            std::lock_guard<JobInformation> stlLock(*oStlJobInformationItr->second);
            const std::string& c_strSafeFunctionIdentifier = oStlJobInformationItr->second->GetSafeFunctionId();
            auto oSafeFunctionItr = m_stlAvailableSafeFunctions.find(c_strSafeFunctionIdentifier);
            __DebugAssert(m_stlAvailableSafeFunctions.end() != oSafeFunctionItr);
            const StructuredBuffer& c_oOutputParameters = oSafeFunctionItr->second.GetStructuredBuffer("OutputParameters");

            auto oOutputParameterNames = c_oOutputParameters.GetNamesOfElements();
            std::optional<StructuredBuffer> oOutputParameterBuffer;

            for ( auto oOutputParameter : oOutputParameterNames )
            {
                const StructuredBuffer c_currentOutput = c_oOutputParameters.GetStructuredBuffer(oOutputParameter.c_str());
                if ( oJobOutput.m_strOutputIdentifier.ToString(eRaw) == c_currentOutput.GetString("Uuid") )
                {
                    oOutputParameterBuffer = c_currentOutput;
                    break;
                }
            }

            if ( !oOutputParameterBuffer.has_value() )
            {
                strResult = "Parameter not found in safe function: " + oJobOutput.m_strOutputIdentifier.ToString(eHyphensAndCurlyBraces);
            }
            else
            {
#ifdef DEBUG_PRINTS
                std::cout << oOutputParameterBuffer.value().ToString() << std::endl;
#endif
                if ( oOutputParameterBuffer.value().GetString("confidentiality") == "1" )
                {
                    strResult = "Parameter is confidential";
                }
                // TODO - We still let confidential parameters in so we can test things
               // else
                //{
                    StructuredBuffer oPushBuffer;
                    std::string strFilename = oJobOutput.ToString();
                    oPushBuffer.PutByte("RequestType", static_cast<Byte>(EngineRequest::ePullData));
                    oPushBuffer.PutString("EndPoint", "JobEngine");
                    oPushBuffer.PutString("Filename", strFilename.c_str());
                    oPushBuffer.PutBoolean("Explicit", fExplicitPull);

#ifdef DEBUG_PRINTS
                    std::cout << "Sent pull request for " << strFilename << std::endl;
#endif
                    oStlJobInformationItr->second->SendStructuredBufferToJobEngine(oPushBuffer);
                    strResult = "Success";
              //  }
            }
        }
    }
    catch(const BaseException& oBaseException )
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
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
    // The only thing we don't return is implicit pull results
    bool fReturnEventToUser{true};
    try
    {
        std::shared_ptr<StructuredBuffer> oDataResult;
        do
        {
            // By default assume we want to return this event
            fReturnEventToUser = true;
            oDataResult = m_oJobMessageQueue.WaitForMessage(nTimeoutInMs);
            if ( nullptr != oDataResult )
            {
                if ( oDataResult->IsElementPresent("SignalType", BYTE_VALUE_TYPE) )
                {
                    JobStatusSignals eStatusSignal = static_cast<JobStatusSignals>(oDataResult->GetByte("SignalType"));
                    if ( JobStatusSignals::ePostValue == eStatusSignal)
                    {
                        m_stlJobResults[oDataResult->GetString("ValueName")] = oDataResult->GetBuffer("FileData");
                        UpdateJobsWaitingForData(*oDataResult);
                        if ( 0 < m_stlOutstandingImplicitPullRequests.count(oDataResult->GetString("ValueName")) )
                        {
#ifdef DEBUG_PRINT
                            std::cout << "Post data was implicit, not returning " << oDataResult->GetString("ValueName") <<std::endl;
#endif
                            m_stlOutstandingImplicitPullRequests.erase(oDataResult->GetString("ValueName"));
                            fReturnEventToUser = false;
                        }
                    }
                    else if ( JobStatusSignals::eJobFail == eStatusSignal ||
                        JobStatusSignals::eJobDone == eStatusSignal ||
                        JobStatusSignals::eJobStart == eStatusSignal ||
                        JobStatusSignals::ePrivacyViolation == eStatusSignal )
                    {
                        Guid oJobIdentifier(oDataResult->GetString("JobUuid"));
                        auto oJobInformation = m_stlJobInformation.find(oJobIdentifier.ToString(eRaw));
                        if ( m_stlJobInformation.end() != oJobInformation )
                        {
                            oJobInformation->second->SetStatus(eStatusSignal);
                        }
                    }
                }
            }
        }
        while ( false == fReturnEventToUser && nullptr != oDataResult ); // Keep pulling of non-user events until we find one
        if ( true == fReturnEventToUser && nullptr != oDataResult)
        {
            strReturn = ::ConvertStructuredBufferToJson(*oDataResult);
        }
    }
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        strReturn = "";
    }
    catch ( ... )
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        strReturn = "";
    }

    return strReturn;
}

/********************************************************************************************
 *
 * @class Orchestrator
 * @function UpdateJobsWaitingForData
 * @brief Update any jobs who may have been waiting for a data push
 * TODO Complete this when we are talking to SCNs
 * @param[in] c_oPushDataMessage - The result of a parameter pushed to us
 *
 ********************************************************************************************/
void __thiscall Orchestrator::UpdateJobsWaitingForData(
    _in const StructuredBuffer& c_oPushDataMessage
    )
{
    std::string strValueParameter(c_oPushDataMessage.GetString("ValueName"));
    __DebugAssert(true == IsJobOutputParameter(strValueParameter));
    __DebugAssert(m_stlJobResults.end() != m_stlJobResults.find(strValueParameter));

    for ( auto& oJobInformation : m_stlJobInformation )
    {
        __DebugAssert(nullptr != oJobInformation.second.get());
        std::lock_guard<JobInformation> stlLock(*oJobInformation.second);

        // We only assign this to jobs that aren't already running
        if ( (oJobInformation.second->JobParameterUsesJobOutputParameter(strValueParameter)) && (false == oJobInformation.second->ReadyToExcute()) )
        {
            try
            {
                StructuredBuffer oPushDataBuffer;
                oPushDataBuffer.PutByte("RequestType", (Byte)EngineRequest::ePushdata);
                oPushDataBuffer.PutString("EndPoint", "JobEngine");
                oPushDataBuffer.PutString("DataId", strValueParameter);
                oPushDataBuffer.PutBuffer("Data", m_stlJobResults[strValueParameter]);

                oJobInformation.second->SendStructuredBufferToJobEngine(oPushDataBuffer);
                oJobInformation.second->SetOutputJobParameterReady(strValueParameter);

                // All our parameters are set, none require a dataset, and we don't have an IP try
                // to get one
                if ((true == oJobInformation.second->AllInputParametersSet())&&(false == oJobInformation.second->RequiresDataset())&&("" == oJobInformation.second->GetTargetIP()))
                {
                    this-> UpdateJobIPAddressForAnySecureComputationalNode(*oJobInformation.second);
                }

                // We have everything we need to submit this job, start it up
                if ( true == oJobInformation.second->ReadyToExcute() )
                {
                    StartJobRemoteExecution(*oJobInformation.second);
                }
            }
            catch(std::exception & e)
            {
                std::cout << "Exception: " << e.what() << '\n';
                ::RegisterUnknownException(__func__, __FILE__, __LINE__);
            }
            catch(const BaseException& oBaseException)
            {
                ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
            }
            catch(...)
            {
                ::RegisterUnknownException(__func__, __FILE__, __LINE__);
            }
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
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
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
void __thiscall Orchestrator::PushJobOutputParameterToJob(
    _in JobInformation& oJob,
    _in const std::string& strParameterIdentifier,
    _in const std::vector<Byte>& oOutputParameterData
    )
{
    __DebugFunction();
    __DebugAssert(IsJobOutputParameter(strParameterIdentifier));
    try
    {
        JobOutputParameter oJobOutputIdentifier = ::ParseStringToJobOutput(strParameterIdentifier);
        StructuredBuffer oPushDataBuffer;
        oPushDataBuffer.PutByte("RequestType", (Byte)EngineRequest::ePushdata);
        oPushDataBuffer.PutString("EndPoint", "JobEngine");
        oPushDataBuffer.PutString("DataId", oJobOutputIdentifier.ToString());
        oPushDataBuffer.PutBuffer("Data", oOutputParameterData);

        SendDataToJob(oJob, oPushDataBuffer);
    }
    catch(const BaseException& oBaseException)
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
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
        oSafeFunctionBuffer.PutStructuredBuffer("ParameterList", oCachedSafeFunction.GetStructuredBuffer("InputParameters"));
        oSafeFunctionBuffer.PutStructuredBuffer("OutputParameters", oCachedSafeFunction.GetStructuredBuffer("OutputParameters"));
        oSafeFunctionBuffer.PutString("Payload", oCachedSafeFunction.GetString("Payload"));

        oJob.SendStructuredBufferToJobEngine(oSafeFunctionBuffer);
    }
    catch(const BaseException& c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
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
 * @function SubmitJob
 * @param [in] JobInformation The job to send this data to
 * @brief Send a structured buffer to a job that contains the submit job message
 *
 ********************************************************************************************/
void __thiscall Orchestrator::SubmitJob(
    _in JobInformation& oJob
    )
{
    try
    {
        StructuredBuffer oParameterSubmitJob;
        oParameterSubmitJob.PutByte("RequestType", (Byte)EngineRequest::eSubmitJob);
        oParameterSubmitJob.PutString("EndPoint", "JobEngine");
        oParameterSubmitJob.PutString("JobUuid", oJob.GetJobId().ToString(eRaw));
        oParameterSubmitJob.PutString("SafeObjectUuid", oJob.GetSafeFunctionId());

        SendDataToJob(oJob, oParameterSubmitJob);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
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
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
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
 * @function SetJobParameterForJobOutput
 * @param [in] JobInformation The job to send this data to
 * @param [in] Guid The guid of the parameter to set
 * @param [in] std::string The value of the parameter's guid to set to
 * @brief Send a structured buffer to a job that will tell the job what the output parameter
 *        is for a job
 *
 ********************************************************************************************/
void __thiscall Orchestrator::SetJobParameterForJobOutput(
    _in JobInformation& oJob,
    _in Guid& oParameterGuid,
    _in std::string& strParameterValue
    )
{
    __DebugFunction();
    __DebugAssert(true == IsJobOutputParameter(strParameterValue));
    __DebugAssert(m_stlJobResults.end() != m_stlJobResults.find(strParameterValue));

    try
    {
        // Set the parameter, then send the data
        StructuredBuffer oParameterSetBuffer;
        oParameterSetBuffer.PutByte("RequestType", (Byte)EngineRequest::eSetParameters);
        oParameterSetBuffer.PutString("EndPoint", "JobEngine");
        oParameterSetBuffer.PutString("JobUuid", oJob.GetJobId().ToString(eRaw));
        oParameterSetBuffer.PutString("ParameterUuid", oParameterGuid.ToString(eRaw));
        oParameterSetBuffer.PutString("ValueUuid", strParameterValue);
        oParameterSetBuffer.PutUnsignedInt32("ValuesExpected", 1);
        oParameterSetBuffer.PutUnsignedInt32("ValueIndex", 0);

        SendDataToJob(oJob, oParameterSetBuffer);

        // Send the job data
        StructuredBuffer oPushDataBuffer;
        oPushDataBuffer.PutByte("RequestType", (Byte)EngineRequest::ePushdata);
        oPushDataBuffer.PutString("EndPoint", "JobEngine");
        oPushDataBuffer.PutString("DataId", strParameterValue);
        oPushDataBuffer.PutBuffer("Data", m_stlJobResults[strParameterValue]);

        SendDataToJob(oJob, oPushDataBuffer);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
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
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
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
 * @function CacheDigitalContractsFromRemote
 * @brief Call to our remote server to get all our digital contracts, and cached their SBs
 *        in a class member map
 *
 ********************************************************************************************/
void __thiscall Orchestrator::CacheDigitalContractsFromRemote(void)
{
    __DebugFunction();

    try
    {
        std::string strVerb = "GET";
        std::string strApiUrl = "/digital-contracts";
        std::vector<std::string> stlListOfHeaders;
        stlListOfHeaders.push_back("Authorization: Bearer " + this->GetCurrentAccessToken());
        stlListOfHeaders.push_back("Content-Type: application/json");
        std::vector<Byte> stlRestResponse = ::RestApiCall(m_oSessionManager.GetServerIpAddress(), m_oSessionManager.GetServerPortNumber(), strVerb, strApiUrl, "", true, stlListOfHeaders);
        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
        _ThrowBaseExceptionIf((true != oResponse.IsElementPresent("digital_contracts", INDEXED_BUFFER_VALUE_TYPE)), "Failed to retrieve digital contracts", nullptr);

        // Need to add an if statement here, since it's possible for the response to have NO digital contracts to
        // offer, in which case there is no "DigitalContracts" element at all. Trying to call oResponse.GetStructuredBuffer("DigitalContracts")
        // without checking will cause an exception
        if (true == oResponse.IsElementPresent("digital_contracts", INDEXED_BUFFER_VALUE_TYPE))
        {
            StructuredBuffer oDigitalContracts = oResponse.GetStructuredBuffer("digital_contracts");
            for (const std::string & strDcIndex : oDigitalContracts.GetNamesOfElements())
            {
                if ("__IsArray__" == strDcIndex)
                {
                    continue;
                }
                StructuredBuffer oDigitalContractRecord = oDigitalContracts.GetStructuredBuffer(strDcIndex.c_str());
                m_stlDigitalContracts.insert({oDigitalContractRecord.GetString("id"), oDigitalContractRecord});
            }
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
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
void Orchestrator::CacheDatasetsFromRemote(void)
{
    __DebugFunction();

    try
    {
        std::string strApiUrl = "/datasets";
        std::vector<std::string> stlListOfHeaders;
        stlListOfHeaders.push_back("Authorization: Bearer " + this->GetCurrentAccessToken());
        stlListOfHeaders.push_back("Content-Type: application/json");
        std::vector<Byte> stlRestResponse = ::RestApiCall(m_oSessionManager.GetServerIpAddress(), m_oSessionManager.GetServerPortNumber(), "GET", strApiUrl, "", true, stlListOfHeaders);

        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));
        _ThrowBaseExceptionIf((true != oResponse.IsElementPresent("datasets", INDEXED_BUFFER_VALUE_TYPE)), "Failed to retrieve datasets", nullptr);

        StructuredBuffer oDatasets = oResponse.GetStructuredBuffer("datasets");
        for (const std::string & strDatasetIndex : oDatasets.GetNamesOfElements())
        {
            if ("__IsArray__" == strDatasetIndex)
            {
                continue;
            }
            StructuredBuffer oDatasetRecord = oDatasets.GetStructuredBuffer(strDatasetIndex.c_str());
            m_stlAvailableDatasets.insert({oDatasetRecord.GetString("id"), oDatasetRecord});

            // Cache our tables
            StructuredBuffer oDatasetTables = oDatasetRecord.GetStructuredBuffer("tables");
            for (const auto & oTableItr : oDatasetTables.GetNamesOfElements())
            {
                if ("__IsArray__" == oTableItr)
                {
                    continue;
                }
                TableInformation oTableInfo(oDatasetRecord.GetString("id"), oDatasetTables.GetStructuredBuffer(oTableItr.c_str()));
                m_stlAvailableTables.insert({oDatasetTables.GetStructuredBuffer(oTableItr.c_str()).GetString("id"), oTableInfo});
            }
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
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