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
#include "JobOutputParameter.h"
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

    return fHasIp && AllInputParametersSet();
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function AllInputParametersSet
 * @brief Determine if all the input parameters for a job are set
 * @return bool - True if this job's input parameters are all set
 ********************************************************************************************/
bool __thiscall JobInformation::AllInputParametersSet() const
{
    // For any outputs that are waiting on output from another job, make sure they are set
    bool fAllJobOutputsReady = std::all_of(m_stlOutputJobParameterData.begin(), m_stlOutputJobParameterData.end(),
        [] (const auto& value) { return value.second;} );

    return fAllJobOutputsReady && std::all_of(m_stlInputParameterData.begin(), m_stlInputParameterData.end(),
        [] ( const auto& value ) { return value.second.has_value(); } );
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function RequiresDataset
 * @brief Determine if any of this job's parameters
 * @return bool - True if this job's input parameters are all set
 ********************************************************************************************/
bool __thiscall JobInformation::RequiresDataset() const
{
    // Construct a lambda function to pass into the any_of algorithm to determine
    // if any of our parameters are datasets or tables
    auto oCheckForDatasetFunc = [] ( const auto& value)
    {
        bool fIsDataset{false};
        if ( value.second.has_value() )
        {
            if ( false == IsJobOutputParameter(value.second.value()) )
            {
                Guid oValueIdentifier{value.second.value()};
                fIsDataset = ( eDataset == oValueIdentifier.GetObjectType() ) || (eTable == oValueIdentifier.GetObjectType());
            }
        }
        return fIsDataset;
    };

    bool fRequiresDataset{false};

    try
    {
        // Check that any of our input parameters are a dataset
        fRequiresDataset = std::any_of(m_stlInputParameterData.begin(), m_stlInputParameterData.end(), oCheckForDatasetFunc);
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

    return fRequiresDataset;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function JobParameterUsesGuid
 * @brief Determine if this job uses the passed in parameter value
 * @param[in] Guid - The guid value to check against
 * @return bool - True if the parameter is used or not
 ********************************************************************************************/
bool __thiscall JobInformation::JobParameterUsesGuid(
    _in const Guid & c_oParameterGuid
    ) const
{
    bool fUsesParameter{false};

    for ( const auto& oInputParameter : m_stlInputParameterData )
    {
        if ( oInputParameter.second.has_value() )
        {
            if ( oInputParameter.second.value() == c_oParameterGuid.ToString(eRaw) )
            {
                fUsesParameter = true;
                break;
            }
        }
    }
    return fUsesParameter;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function JobParameterUsesJobOutputParameter
 * @brief Determine if this job uses a given output parameter
 * @param[in] Guid - The guid value to check against
 * @return bool - True if the parameter is used or not
 ********************************************************************************************/
bool __thiscall JobInformation::JobParameterUsesJobOutputParameter(
    _in const std::string & c_strJobOutputParameter
    ) const
{
    bool fUsesParameter{false};

    for ( const auto& oInputParameter : m_stlInputParameterData )
    {
        if ( oInputParameter.second.has_value() )
        {
            if ( oInputParameter.second.value() == c_strJobOutputParameter )
            {
                fUsesParameter = true;
                break;
            }
        }
    }
    return fUsesParameter;
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

        if ( ::IsJobOutputParameter(strValue) )
        {
            m_stlOutputJobParameterData.emplace(strValue, false);
        }
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

/********************************************************************************************
 *
 * @class JobInformation
 * @function IsRunning
 * @brief Determine if the current job is running
 * @return bool - Whether the Job is running or not
 ********************************************************************************************/
bool __thiscall JobInformation::IsRunning() const
{
    return m_eJobStatus.has_value();
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function SendCachedMessages
 * @brief Send the messages we have cached for this job
 * @return bool - Whether the cached messages were sent
 ********************************************************************************************/
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
            m_poJobEngineConnection->SendStructuredBufferToJobEngine(c_oBufferToSend);
            fSent = true;
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

/********************************************************************************************
 *
 * @class JobInformation
 * @function SetStatus
 * @brief Set the current status of this job
 * @param[in] JobStatusSignals The Status of the job
 ********************************************************************************************/
void __thiscall JobInformation::SetStatus(
    _in JobStatusSignals eJobStatus
)
{
    __DebugFunction();

    m_eJobStatus = eJobStatus;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function SetOutputJobParameterData
 * @brief For a job's output parameter cached the data in the job to be pushed when the
 *        job runs
 * @param[in] c_strOutputParameterId The ID of the parameter
 ********************************************************************************************/
void __thiscall JobInformation::SetOutputJobParameterReady(
    _in const std::string& c_strOutputParameterId
    )
{
    __DebugFunction();

    if ( m_stlOutputJobParameterData.end() != m_stlOutputJobParameterData.find(c_strOutputParameterId) )
    {
        m_stlOutputJobParameterData[c_strOutputParameterId] = true;
    }
}