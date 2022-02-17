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
    m_strTargetIP = "192.168.0.244";
    __DebugFunction();
    //__DebugAssert("" == m_strTargetIP);
    //m_strTargetIP = c_strTargetIP;
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
void __thiscall JobInformation::SetConnection(std::shared_ptr<TlsNode> poTlsConnection)
{
    __DebugFunction();
    m_poTlsConnection = poTlsConnection;
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
    return m_poTlsConnection;
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
 * @function StartJobEngineListenerThread
 * @brief Starts the listening thread for the job engine communication

 ********************************************************************************************/
void __thiscall JobInformation::StartJobEngineListenerThread()
{
    __DebugFunction();
    __DebugAssert(nullptr == m_pstlListenerThread.get());

    m_pstlListenerThread.reset(new std::thread(&JobInformation::JobEngineListener, this));
    m_fStopRequest = false;
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
    __DebugAssert( nullptr != m_poTlsConnection );

    bool fSent{false};
    try
    {
        std::lock_guard<JobInformation> jobLock(*this);
        // TODO Remove this check when we can talk to an SCN
        if ( nullptr != m_poTlsConnection.get() )
        {
            ::PutTlsTransaction(m_poTlsConnection.get(), c_oBufferToSend);
        }
        else
        {
            std::cout << "NO CONNECTION " << std::endl;
        }
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

bool __thiscall JobInformation::IsRunning() const
{
    return nullptr != m_pstlListenerThread;
}

/********************************************************************************************
 *
 * @class JobInformation
 * @function JobEngineListener
 * @brief The listen function for a job engine connection, intended to be run on a thread.
 *        To stop the thread set m_fStopRequest to true
 ********************************************************************************************/
void __thiscall JobInformation::JobEngineListener()
{
    __DebugFunction();
    // TODO - Re-enable when we can talk to an SCN
    //__DebugAssert(nullptr != m_poTlsConnection.get());

    if ( nullptr == m_poTlsConnection.get() )
    {
        std::cout << "No connection to job engine" << std::endl;
    }
    constexpr unsigned int unWaitOnMessageTimeoutInMilliseconds{1000};
    int nTestCounter{0};
    std::cout << "Listener has started " << std::endl;
    while( !m_fStopRequest )
    {
        std::vector<Byte> stlJobEngineMessage;
        {
            std::cout << "Waiting on message " << std::endl;
            std::lock_guard<JobInformation>(*this);
            if ( nullptr != m_poTlsConnection.get() )
            {
                stlJobEngineMessage = ::GetTlsTransaction( m_poTlsConnection.get(), unWaitOnMessageTimeoutInMilliseconds);
            }
            else
            {
                std::this_thread::sleep_for(std::chrono::milliseconds(unWaitOnMessageTimeoutInMilliseconds));
            }
        }
        // Not getting a message is not an error, we have short timeouts to allow other users
        // to take ownershipe of the JobInformation if needed
        if ( 0 != stlJobEngineMessage.size() )
        {
            std::cout << "Received a message " << stlJobEngineMessage.size() << std::endl;
            try
            {

                // We have a message, load it into a StructuredBuffer
                StructuredBuffer oJobEngineMessage(stlJobEngineMessage);
                JobStatusSignals eJobEngineStatus = static_cast<JobStatusSignals>(oJobEngineMessage.GetByte("SignalType"));

                switch (eJobEngineStatus)
                {
                    case JobStatusSignals::eJobFail:
                    case JobStatusSignals::eJobDone:
                    case JobStatusSignals::eJobStart:
                    {
                        std::lock_guard<JobInformation> oLock(*this);
                        m_eJobStatus = eJobEngineStatus;
                        // Push to queue
                        m_oQueueToOrchestrator.CopyAndPushMessage(oJobEngineMessage);
                        break;
                    }
                    case JobStatusSignals::eHeartBeatPing:
                    {
                        // Reply to the ping to keep the connection alive
                        StructuredBuffer oHeartBeatPong;
                        oHeartBeatPong.PutString("EndPoint", "JobEngine");
                        oHeartBeatPong.PutByte("RequestType", static_cast<Byte>(EngineRequest::eHeartBeatPong));
                        SendStructuredBufferToJobEngine(oHeartBeatPong);
                        break;
                    }
                    case JobStatusSignals::ePostValue:
                    {
                        std::vector<Byte> stlPushedData = oJobEngineMessage.GetBuffer("FileData");
                        std::string strDataId = oJobEngineMessage.GetString("ValueName");
                        oJobEngineMessage.PutString("JobUuid", m_oJobId.ToString(eRaw));
                        // We haven't seen this before
                        if ( m_stlOutputResults.end() == m_stlOutputResults.find(strDataId) )
                        {
                            std::lock_guard<JobInformation> oLock(*this);
                            m_stlOutputResults[strDataId] = stlPushedData;
                            // Push to queue
                        }
                        else
                        {
                            std::cout << "Got post value for existing data " << strDataId << std::endl;
                        }
                        m_oQueueToOrchestrator.CopyAndPushMessage(oJobEngineMessage);
                        break;
                    }
                    case JobStatusSignals::eVmShutdown:
                    {
                        std::cout << "Job " << m_oJobId.ToString(eHyphensAndCurlyBraces) << " has shutdown " << std::endl;
                        // Push to queue
                        m_oQueueToOrchestrator.CopyAndPushMessage(oJobEngineMessage);
                        break;
                    }
                    default:
                    {
                        std::cout << "Unknown state " << static_cast<Byte>(eJobEngineStatus) << std::endl;
                    }
                }
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
        // This is temporary code to produce messages until we can talk to an SCN
        /*else
        {
            StructuredBuffer oTestBuffer;
            oTestBuffer.PutString("TestMessage", "Hello");
            oTestBuffer.PutString("JobGuid", m_oJobId.ToString(eHyphensAndCurlyBraces));
            oTestBuffer.PutInt32("TestValue", nTestCounter);
            m_oQueueToOrchestrator.CopyAndPushMessage(oTestBuffer);
            ++nTestCounter;
            std::cout << "No message, sending dummy to orchestrator " << std::endl;
            if ( false == m_eJobStatus.has_value() )
            {
                // Ping pong a value to help test job status functions
                m_eJobStatus = (nTestCounter & 0x01) ? JobStatusSignals::eJobStart : JobStatusSignals::ePrivacyViolation;
            }
        }*/
    }
}
