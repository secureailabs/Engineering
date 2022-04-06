#include <chrono>
#include <iostream>
#include <vector>

#include "CurlRest.h"
#include "DebugLibrary.h"
#include "EosbRotationManager.h"
#include "ExceptionRegister.h"
#include "JsonParser.h"
#include "StructuredBuffer.h"

/********************************************************************************************
 *
 * @class EosbRotationManager
 * @function EosbRotationManager
 * @brief Constructor
 *
 ********************************************************************************************/
EosbRotationManager::EosbRotationManager(void)
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
void __thiscall EosbRotationManager::PeriodicEosbUpdate(void)
{
    __DebugFunction();
    
    while (false == fStopRequest)
    {
        using namespace std::literals;
        std::unique_lock<std::mutex> oMutexLock(m_oLock);
        m_oTimedWait.wait_for(oMutexLock, 10min, [&] { return fStopRequest; });
        if (false == fStopRequest)
        {
            // We aren't stopping, update the EOSB
            std::string strVerb = "GET";
            std::string strApiUrl = "/SAIL/AuthenticationManager/CheckEosb";
            std::string strJsonBody = "{\"Eosb\" : \"" + m_strEosb + "\"}";
            // Make the API call and get REST response
            try
            {
                std::vector<Byte> stlRestResponse = ::RestApiCall(m_strServerIp, m_unServerPort, strVerb, strApiUrl, strJsonBody, true);
                StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer(reinterpret_cast<const char*>(stlRestResponse.data()));
                _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "Error updating EOSB in.", nullptr);
                m_strEosb = oResponse.GetString("Eosb");
            }
            
            catch (const BaseException & c_oBaseException)
            {
                ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
            }

            catch (...)
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
void __thiscall EosbRotationManager::Stop(void)
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
 * @param[in] c_strServerIpAddress Ip address of the server we authenticate with
 * @param[in] unServerPort Port of the server we authenticate with
 *
 ********************************************************************************************/
void __thiscall EosbRotationManager::Start(
    _in const std::string& c_strServerIpAddress,
    _in unsigned int unServerPort
)
{
    __DebugFunction();
    __DebugAssert(nullptr == m_oRotatingThread);

    m_strServerIp = c_strServerIpAddress;
    m_unServerPort = unServerPort;

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
std::string __thiscall EosbRotationManager::GetEosb(void) const
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
bool __thiscall EosbRotationManager::IsRunning(void) const
{
    __DebugFunction();

    return m_oRotatingThread != nullptr;
}

/********************************************************************************************
 *
 * @class EosbRotationManager
 * @function GetServerIp
 * @brief Return the IP address of the remote that this EOSB is associated with
 * @return std::string - The IP address for this EOSB
 ********************************************************************************************/
const std::string & EosbRotationManager::GetServerIp(void) const
{
    __DebugFunction();
    return m_strServerIp;
}

/********************************************************************************************
 *
 * @class EosbRotationManager
 * @function GetServerPort
 * @brief Return the port of the remote that this EOSB is associated with
 * @return unsigned int - The port for this EOSB
 ********************************************************************************************/
unsigned int EosbRotationManager::GetServerPort(void) const
{
    __DebugFunction();
    return m_unServerPort;
}
