#include <chrono>
#include <iostream>
#include <vector>

#include "CurlRest.h"
#include "DebugLibrary.h"
#include "EosbRotationManager.h"
#include "ExceptionRegister.h"
#include "JsonValue.h"
#include "StructuredBuffer.h"

/********************************************************************************************
 *
 * @class EosbRotationManager
 * @function EosbRotationManager
 * @brief Constructor
 * @param[in] strServerIp Ip address of the server we authenticate with
 * @param[in] unServerPort Port of the server we authenticate with
 *
 ********************************************************************************************/
EosbRotationManager::EosbRotationManager(
    void
    )
{
    __DebugFunction();
}

/********************************************************************************************
 *
 * @class EosbRotationManager
 * @function EosbRotationManager
 * @brief Destructor, ensures our running thread is stopped
 *
 ********************************************************************************************/
EosbRotationManager::~EosbRotationManager(void)
{
    __DebugFunction();
    Stop();
}

/********************************************************************************************
 *
 * @class EosbRotationManager
 * @function PeriodicEosbUpdate
 * @brief Waits for a period of time, then requests an EOSB check on the remote, and stores
 *        the updated EOSB
 *
 ********************************************************************************************/
void __thiscall EosbRotationManager::PeriodicEosbUpdate()
{
    __DebugFunction();
    while ( !fStopRequest )
    {
        using namespace std::literals;
        std::unique_lock<std::mutex> oMutexLock(m_oLock);
        m_oTimedWait.wait_for(oMutexLock, 10min, [&] { return fStopRequest; });
        if ( !fStopRequest )
        {
            // We aren't stopping, update the EOSB
            std::string strVerb = "GET";
            std::string strApiUrl = "/SAIL/AuthenticationManager/CheckEosb";
            std::string strJsonBody = "{\"Eosb\" : \"" + m_strEosb + "\"}";
            // Make the API call and get REST response
            try
            {
                std::vector<Byte> stlRestResponse = ::RestApiCall(m_strServerIp, m_unServerPort, strVerb, strApiUrl, strJsonBody, true);
                std::string strUnescapedResponse = ::UnEscapeJsonString((const char *) stlRestResponse.data());
                StructuredBuffer oResponse(JsonValue::ParseDataToStructuredBuffer(strUnescapedResponse.c_str()));
                _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "Error updating EOSB in.", nullptr);
                m_strEosb = oResponse.GetString("Eosb");
            }
            catch(BaseException oBaseException)
            {
                ::RegisterException(oBaseException, __func__, __FILE__, __LINE__);
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
 * @class EosbRotationManager
 * @function Stop
 * @brief Issues a stop request to our thread, and then waits to join the thread
 *
 ********************************************************************************************/
void __thiscall EosbRotationManager::Stop()
{
    __DebugFunction();
    {
        std::lock_guard<std::mutex> oMutexLock{m_oLock};
        fStopRequest = true;
    }

    // Ensure to notify after the mutex is released to ensure the CV wakes up
    // with an unlocked mutex
    m_oTimedWait.notify_all();

    if ( m_oRotatingThread )
    {
        m_oRotatingThread->join();
        m_oRotatingThread.release();
    }
}

/********************************************************************************************
 *
 * @class EosbRotationManager
 * @function Start
 * @brief Starts up our rotation thread
 *
 ********************************************************************************************/
void __thiscall EosbRotationManager::Start(
    _in const std::string& c_strServerIpAddress,
    _in unsigned int c_unServerPort
)
{
    __DebugFunction();
    __DebugAssert(nullptr == m_oRotatingThread);

    m_strServerIp = c_strServerIpAddress;
    m_unServerPort = c_unServerPort;

    fStopRequest = false;
    m_oRotatingThread = std::unique_ptr<std::thread>(new std::thread(&EosbRotationManager::PeriodicEosbUpdate, this));
}

/********************************************************************************************
 *
 * @class EosbRotationManager
 * @function Start
 * @brief Starts up our rotation thread
 * @return std::string - The most up to date EOSB
 ********************************************************************************************/
std::string __thiscall EosbRotationManager::GetEosb() const
{
    __DebugFunction();
    std::lock_guard<std::mutex> oMutexLock{m_oLock};
    return m_strEosb;
}

/********************************************************************************************
 *
 * @class EosbRotationManager
 * @function SetEosb
 * @brief Sets the EOSB value from outside
 * @param[in] strEosb The new EOSB
 ********************************************************************************************/
void __thiscall EosbRotationManager::SetEosb(const std::string& strEosb)
{
    __DebugFunction();
    std::lock_guard<std::mutex> oMutexLock{m_oLock};
    m_strEosb = strEosb;
}

/********************************************************************************************
 *
 * @class EosbRotationManager
 * @function IsRunning
 * @brief Determine if the rotation thread is running
 * @return bool - Whether the thread is running
 ********************************************************************************************/
bool __thiscall EosbRotationManager::IsRunning() const
{
    __DebugFunction();

    return m_oRotatingThread != nullptr;
}
