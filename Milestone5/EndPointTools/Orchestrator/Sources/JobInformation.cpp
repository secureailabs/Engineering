/*********************************************************************************************
 *
 * @file JobInformation.cpp
 * @author David Gascon
 * @date 10 Jan, 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/
#include "DebugLibrary.h"
#include "ExceptionRegister.h"
#include "Guid.h"
#include "JobEngineConnection.h"
#include "JobInformation.h"
#include "OrchestratorTypes.h"
#include "StructuredBuffer.h"
#include "StructuredBufferLockedQueue.h"
#include "TlsNode.h"
#include "TlsTransactionHelperFunctions.h"

#include <algorithm>
#include <chrono>
#include <iostream>
#include <thread>
#include <vector>

/********************************************************************************************
 *
 * @class JobInformation
 * @function JobInformation
 * @brief Constructor
 * @param[in] std::vector<std::string> - A vector of all the input parameters we need to track for this
 *                                       job
 *
 ********************************************************************************************/
JobInformation::JobInformation(
    const Guid& c_oJobId,
    const Guid& c_oSafeFunctionId,
    const std::vector<std::string>& c_stlInputParameters,
    StructuredBufferLockedQueue& oQueueToOrchestrator
    ):
    m_oJobId(c_oJobId),
    m_oSafeFunctionId(c_oSafeFunctionId),
    m_oQueueToOrchestrator(oQueueToOrchestrator)
{

    __DebugFunction();

    for ( auto strInputGUID : c_stlInputParameters )
    {
        m_stlInputParameterData.emplace(strInputGUID, std::optional<std::string>());
    }
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function JobInformation
 * @brief Destructor
 *
 ********************************************************************************************/
JobInformation::~JobInformation()
{
    __DebugFunction();

    m_fStopRequest = true;
    if ( nullptr != m_pstlListenerThread.get() )
    {
        m_pstlListenerThread->join();
    }
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function ReadyToExecute
 * @brief Determine if this job is ready to execute.  Ready to execute is define as having
 *        values set for all input parameters
 * @return bool - True if this job is prepared to execute, false otherwise
 ********************************************************************************************/
bool __thiscall JobInformation::ReadyToExcute(
    void
    ) const
{
    __DebugFunction();
    bool fHasIp = ( "" != m_strTargetIP );

    // Iterate through all our input parameters and make sure they have values, if they
    // do and we know where we have to execute this job is ready to execute
    return fHasIp && std::all_of(m_stlInputParameterData.begin(), m_stlInputParameterData.end(),
        [] ( const auto& value ) { return value.second.has_value(); } );
}

bool __thiscall JobInformation::JobUsesDataset(
    _in const Guid & c_oDatasetGuid
    ) const
{
    bool fUsesDataset{false};

    for ( const auto& oInputParameter : m_stlInputParameterData )
    {
        if ( oInputParameter.second.has_value() )
        {
            if ( oInputParameter.second.value() == c_oDatasetGuid.ToString(eRaw) )
            {
                fUsesDataset = true;
                break;
            }
            // TODO also handle tables
        }
    }
    return fUsesDataset;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function SetInputParameter
 * @brief Set the value for an input parameter
 * @param[in] strInputParameterId The ID of the input parameter this job wants to set
 * @param[in] strValue The new value for the input parameter
 * @return bool - True if the parameter was found, false if not
 ********************************************************************************************/
bool __thiscall JobInformation::SetInputParameter(
    _in const std::string& strInputParameterId,
    _in const std::string& strValue
    )
{
    __DebugFunction();

    bool fSetValue{false};
    if ( m_stlInputParameterData.end() != m_stlInputParameterData.find(strInputParameterId) )
    {
        m_stlInputParameterData[strInputParameterId] = strValue;
        fSetValue = true;
    }
    return fSetValue;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function GetInputParameterMap
 * @brief Get the input parameter map

 * @return std::unordered_map<std::string, std::optional<std::string>> - A const reference
 *         of the internal parameter setting map
 ********************************************************************************************/
const std::unordered_map<std::string, std::optional<std::string>>& __thiscall JobInformation::GetInputParameterMap(void) const
{
    __DebugFunction();
    return m_stlInputParameterData;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function SetTargetIp
 * @brief Set the target IP address for this job
 * @param[in] c_strTargetIp The target IP address for this job
 ********************************************************************************************/
void __thiscall JobInformation::SetTargetIP(
    _in const std::string& c_strTargetIP
    )
{
    __DebugFunction();
    __DebugAssert("" == m_strTargetIP);
    m_strTargetIP = c_strTargetIP;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function GetTargetIp
 * @brief Gets the target IP address for this job
 * @return std::string The target IP address for this job
 ********************************************************************************************/
std::string __thiscall JobInformation::GetTargetIP(void) const
{
    __DebugFunction();
    return m_strTargetIP;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function SetConnection
 * @brief Sets the TLS connection pointer for this job
 * @param[in] poTlsConnection The TLS connection for this job
 ********************************************************************************************/
void __thiscall JobInformation::SetConnection(
    _in std::shared_ptr<JobEngineConnection> poTlsConnection)
{
    __DebugFunction();

    m_poJobEngineConnection = poTlsConnection;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function GetConnection
 * @brief Gets the TLS connection pointer for this job
 * @return std::shared_ptr<TlsNode> The target IP address for this job wrapped in a shared_ptr
 ********************************************************************************************/
std::shared_ptr<TlsNode> __thiscall JobInformation::GetConnection() const
{
    __DebugFunction();
    return m_poJobEngineConnection->GetConnection();
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function lock
 * @brief Locks the underlying mutex
 ********************************************************************************************/
void __thiscall JobInformation::lock(void)
{
    __DebugFunction();
    m_stlLock.lock();
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function unlock
 * @brief Locks the underlying mutex
 ********************************************************************************************/
void __thiscall JobInformation::unlock(void)
{
    __DebugFunction();
    m_stlLock.unlock();
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function GetSafeFunctionId
 * @brief Gets the SafeFunction ID this job is to run with
 * @return std::string The ID for the Safefunction this job is targeting
 ********************************************************************************************/
std::string __thiscall JobInformation::GetSafeFunctionId(void) const
{
    __DebugFunction();
    return m_oSafeFunctionId.ToString(eRaw);
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function GetJobId
 * @brief Gets the Job ID for this job
 * @return const Guid& The ID for this job
 ********************************************************************************************/
const Guid& __thiscall JobInformation::GetJobId() const
{
    __DebugFunction();

    return m_oJobId;
}

bool __thiscall JobInformation::IsRunning() const
{
    return m_eJobStatus.has_value();
}

bool __thiscall JobInformation::SendCachedMessages(void)
{
    __DebugFunction();

    bool fSent{false};
    try
    {
        std::lock_guard<JobInformation> jobLock(*this);
        for ( auto c_oBufferToSend : m_stlCachedStructuredBuffers )
        {
            m_poJobEngineConnection->SendStructuredBufferToJobEngine(c_oBufferToSend);
        }
        m_stlCachedStructuredBuffers.clear();
        fSent = true;
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
    return fSent;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function SendStructuredBufferToJobEngine
 * @brief Sends a structured buffer to the remote job engine
 * @param[in] c_oBufferToSend The buffer to send
 ********************************************************************************************/
bool __thiscall JobInformation::SendStructuredBufferToJobEngine(
    _in const StructuredBuffer& c_oBufferToSend
    )
{
    __DebugFunction();

    bool fSent{false};
    try
    {
        std::lock_guard<JobInformation> jobLock(*this);
        if ( m_poJobEngineConnection != nullptr )
        {
            // TODO Remove this check when we can talk to an SCN
            m_poJobEngineConnection->SendStructuredBufferToJobEngine(c_oBufferToSend);
        }
        else
        {
            m_stlCachedStructuredBuffers.push_back(c_oBufferToSend);
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
    return fSent;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function GetJobStatus
 * @brief Gets a string representing the status of the job
 * @param[in] c_oBufferToSend The buffer to send
 ********************************************************************************************/
std::string __thiscall JobInformation::GetJobStatus(void) const
{
    std::string strJobStatus{""};

    bool fAllInputParametersSet = std::all_of(m_stlInputParameterData.begin(), m_stlInputParameterData.end(),
        [] ( const auto& value ) { return value.second.has_value(); } );

    bool fHasIp = ( "" != m_strTargetIP );

    if ( !fAllInputParametersSet )
    {
        strJobStatus = "Missing Input Parameters";
    }
    else
    {
        if ( !fHasIp )
        {
            strJobStatus = "Missing SCN IP Address";
        }
        else if ( m_eJobStatus.has_value() )
        {
            switch ( m_eJobStatus.value() )
            {
                case JobStatusSignals::eJobStart
                :
                    strJobStatus = "Job Started";
                    break;
                case JobStatusSignals::eJobDone
                :
                    strJobStatus = "Job Done";
                    break;
                case JobStatusSignals::eJobFail
                :
                    strJobStatus = "Job Fail";
                    break;
                case JobStatusSignals::ePrivacyViolation
                :
                    strJobStatus = "Privacy Violation";
                    break;
                case JobStatusSignals::eVmShutdown
                :
                    strJobStatus = "SCN Shutdown";
                    break;
                default
                :
                    strJobStatus = "SCN in Unknown state";
            }
        }
        else
        {
            strJobStatus = "Waiting on SCN to report status";
        }
    }

    return strJobStatus;
}
