#include "DebugLibrary.h"
#include "ExceptionRegister.h"
#include "JobEngineConnection.h"
#include "OrchestratorTypes.h"
#include "StructuredBufferLockedQueue.h"
#include "TlsTransactionHelperFunctions.h"

#include <iostream>
#include <mutex>
#include <thread>
#include <vector>


JobEngineConnection::JobEngineConnection(
    std::shared_ptr<TlsNode> stlConnectionPointer,
    StructuredBufferLockedQueue& oQueueToOrchestrator
    ) :
    m_stlConnectionPointer{stlConnectionPointer},
    m_oStructuredBufferQueue{oQueueToOrchestrator}
{
    __DebugFunction();

    m_pstlListenerThread.reset(new std::thread(&JobEngineConnection::JobEngineConnectionThread, this));
    m_fStopRequest = false;
}
/********************************************************************************************
 *
 * @class JobInformation
 * @function SendStructuredBufferToJobEngine
 * @brief Sends a structured buffer to the remote job engine
 * @param[in] c_oBufferToSend The buffer to send
 ********************************************************************************************/
bool __thiscall JobEngineConnection::SendStructuredBufferToJobEngine(
    _in const StructuredBuffer& c_oBufferToSend
    )
{
    __DebugFunction();

    bool fSent{false};
    try
    {
        ::PutTlsTransaction(m_stlConnectionPointer.get(), c_oBufferToSend);
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
 * @class JobEngineConnection
 * @function GetConnection
 * @brief Gets the TLS connection pointer for this job
 * @return std::shared_ptr<TlsNode> The target IP address for this job wrapped in a shared_ptr
 ********************************************************************************************/
std::shared_ptr<TlsNode> __thiscall JobEngineConnection::GetConnection() const
{
    __DebugFunction();
    return m_stlConnectionPointer;
}

bool __thiscall JobEngineConnection::IsRunning() const
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
void __thiscall JobEngineConnection::JobEngineConnectionThread()
{
    __DebugFunction();
    // TODO - Re-enable when we can talk to an SCN
    //__DebugAssert(nullptr != m_poTlsConnection.get());

    if ( nullptr == m_stlConnectionPointer )
    {
        std::cout << "No connection to job engine" << std::endl;
    }
    constexpr unsigned int unWaitOnMessageTimeoutInMilliseconds{1000};
    int nTestCounter{0};

    while( !m_fStopRequest )
    {
        std::vector<Byte> stlJobEngineMessage;
        {
            std::cout << "Waiting on message " << std::endl;
            if ( nullptr != m_stlConnectionPointer.get() )
            {
                stlJobEngineMessage = ::GetTlsTransaction( m_stlConnectionPointer.get(), unWaitOnMessageTimeoutInMilliseconds);
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
                if ( oJobEngineMessage.IsElementPresent("SignalType", BYTE_VALUE_TYPE))
                {
                    JobStatusSignals eJobEngineStatus = static_cast<JobStatusSignals>(oJobEngineMessage.GetByte("SignalType"));

                    switch (eJobEngineStatus)
                    {
                        case JobStatusSignals::eJobFail:
                        case JobStatusSignals::eJobDone:
                        case JobStatusSignals::eJobStart:
                        {
                            // Push to queue
                            m_oStructuredBufferQueue.CopyAndPushMessage(oJobEngineMessage);
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
                            m_oStructuredBufferQueue.CopyAndPushMessage(oJobEngineMessage);
                            break;
                        }
                        case JobStatusSignals::eVmShutdown:
                        {
                            // Push to queue
                            m_oStructuredBufferQueue.CopyAndPushMessage(oJobEngineMessage);
                            break;
                        }
                        default:
                        {
                            std::cout << "Unknown state " << static_cast<Byte>(eJobEngineStatus) << std::endl;
                        }
                    }
                }
                else
                {
                    std::cout << "Message without signal type " << oJobEngineMessage.ToString() << std::endl;
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
    }
}

/********************************************************************************************
 *
 * @class JobEngineConnection
 * @function StartJobEngineListenerThread
 * @brief Starts the listening thread for the job engine communication

 ********************************************************************************************/
void __thiscall JobEngineConnection::StartJobEngineListenerThread()
{
    __DebugFunction();
    __DebugAssert(nullptr == m_pstlListenerThread.get());

    m_pstlListenerThread.reset(new std::thread(&JobEngineConnection::JobEngineConnectionThread, this));
    m_fStopRequest = false;
}
