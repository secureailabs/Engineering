/*********************************************************************************************
 *
 * @file DataFederationManager.cpp
 * @author David Gascon
 * @date 10 Mar 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 * @brief
 ********************************************************************************************/

#include "DataFederationManager.h"
#include "64BitHashes.h"
#include "IpcTransactionHelperFunctions.h"
#include "RequestHelpers.h"
#include "SmartMemoryAllocator.h"
#include "SocketClient.h"
#include "ThreadManager.h"
#include "TlsClient.h"

static DataFederationManager * gs_oDataFederationManager = nullptr;

/*******************************************************************************
 * File constants
 ******************************************************************************/

/********************************************************************************************
 *
 * @function GetDataFederationManager
 * @brief Create a singleton object of DataFederationManager class
 * @throw OutOfMemoryException If there isn't enough memory left to create a new instance
 * @return Return the singleton object of DataFederationManager class
 *
 ********************************************************************************************/
DataFederationManager * __stdcall GetDataFederationManager(void)
{
    __DebugFunction();

    if (nullptr == gs_oDataFederationManager)
    {
        gs_oDataFederationManager = new DataFederationManager();
        _ThrowOutOfMemoryExceptionIfNull(gs_oDataFederationManager);
    }

    return gs_oDataFederationManager;
}

/********************************************************************************************
 *
 * @function ShutdownDataFederationManager
 * @brief Release the object resources and set global static pointer to NULL
 *
 ********************************************************************************************/
void __stdcall ShutdownDataFederationManager(void)
{
    __DebugFunction();

    if (nullptr != gs_oDataFederationManager)
    {
        gs_oDataFederationManager->TerminateSignalEncountered();
        gs_oDataFederationManager->Release();
        gs_oDataFederationManager = nullptr;
    }
}

/********************************************************************************************
 *
 * @class DataFederationManager
 * @function DataFederationManager
 * @brief Constructor
 *
 ********************************************************************************************/

DataFederationManager::DataFederationManager(void)
{
    __DebugFunction();

    m_sMutex = PTHREAD_MUTEX_INITIALIZER;
    m_unNextAvailableIdentifier = 0;
    m_fTerminationSignalEncountered = false;
}

/********************************************************************************************
 *
 * @class DataFederationManager
 * @function DataFederationManager
 * @brief Copy Constructor
 * @param[in] c_oDataFederationManager Another instance of the class
 * @note
 *      This constructor triggers an assertion failure if called.
 *
 ********************************************************************************************/

DataFederationManager::DataFederationManager(
    _in const DataFederationManager & c_oDataFederationManager
    )
{
    __DebugFunction();
    __DebugAssert(false);
}

/********************************************************************************************
 *
 * @class DataFederationManager
 * @function ~DataFederationManager
 * @brief Destructor
 *
 ********************************************************************************************/

DataFederationManager::~DataFederationManager(void)
{
    __DebugFunction();

    // Wait for all threads in the group to terminate
    ThreadManager * poThreadManager = ThreadManager::GetInstance();
    poThreadManager->JoinThreadGroup("DataFederationManagerPluginGroup");
}

/********************************************************************************************
 *
 * @class DataFederationManager
 * @function GetName
 * @brief Fetch the name of the plugin
 * @return Name of the plugin
 *
 ********************************************************************************************/

const char * __thiscall DataFederationManager::GetName(void) const throw()
{
    __DebugFunction();

    static const char * sc_szName = "DataFederationManager";

    return sc_szName;
}

/********************************************************************************************
 *
 * @class DataFederationManager
 * @function GetUuid
 * @brief Fetch the UUID of the plugin
 * @return UUID of the plugin
 *
 ********************************************************************************************/

const char * __thiscall DataFederationManager::GetUuid(void) const throw()
{
    __DebugFunction();

    // Generated with uuidgen
    static const char * sc_szUuid = "{43475787-0518-41d3-b382-110dd8f200be}";

    return sc_szUuid;
}

/********************************************************************************************
 *
 * @class DataFederationManager
 * @function GetVersion
 * @brief Fetch the current version of the plugin
 * @return Version of the plugin
 *
 ********************************************************************************************/

Qword __thiscall DataFederationManager::GetVersion(void) const throw()
{
    __DebugFunction();

    return 0x0000000100000001;
}

/********************************************************************************************
 *
 * @class DataFederationManager
 * @function GetDictionarySerializedBuffer
 * @brief Fetch the serialized buffer of the plugin's dictionary
 * @return Serialized buffer of the plugin's dictionary
 *
 ********************************************************************************************/

std::vector<Byte> __thiscall DataFederationManager::GetDictionarySerializedBuffer(void) const throw()
{
    __DebugFunction();

    return m_oDictionary.GetSerializedDictionary();
}

/********************************************************************************************
 *
 * @class DataFederationManager
 * @function TerminateSignalEncountered
 * @brief Set termination signal
 *
 ********************************************************************************************/

void __thiscall DataFederationManager::TerminateSignalEncountered(void)
{
    __DebugFunction();

    m_fTerminationSignalEncountered = true;
}

/********************************************************************************************
 *
 * @class DataFederationManager
 * @function InitializePlugin
 * @brief Initializer that initializes the plugin's dictionary
 *
 ********************************************************************************************/

void __thiscall DataFederationManager::InitializePlugin(const StructuredBuffer& oInitializationVectors)
{
    __DebugFunction();

    m_strDatabaseServiceIpAddr = oInitializationVectors.GetString("DatabaseServerIp");
    m_unDatabaseServiceIpPort = oInitializationVectors.GetUnsignedInt32("DatabaseServerPort");

}



/********************************************************************************************
 *
 * @class DataFederationManager
 * @function SubmitRequest
 * @brief Method called by flat function SubmitRequest when a client requests for the plugin's resource
 * @param[in] c_oRequestStructuredBuffer points to the request body
 * @param[out] punSerializedResponseSizeInBytes stores the size of the response
 * @throw BaseException Element not found
 * @throw BaseException Error generating challenge nonce
 * @returns a 64 bit unique transaction identifier
 *
 ********************************************************************************************/

uint64_t __thiscall DataFederationManager::SubmitRequest(
    _in const StructuredBuffer & c_oRequestStructuredBuffer,
    _out unsigned int * punSerializedResponseSizeInBytes
    )
{
    __DebugFunction();

    __DebugAssert(punSerializedResponseSizeInBytes != nullptr);

    uint64_t un64Identifier = 0xFFFFFFFFFFFFFFFF;
    std::string strVerb = c_oRequestStructuredBuffer.GetString("Verb");
    std::string strResource = c_oRequestStructuredBuffer.GetString("Resource");
    // TODO: As an optimization, we should make sure to convert strings into 64 bit hashes
    // in order to speed up comparison. String comparisons WAY expensive.
    std::vector<Byte> stlResponseBuffer;

    TlsNode * poTlsNode{nullptr};
    StructuredBuffer responseBuffer;

    if ( "GET" == strVerb)
    {

    }
    else if ("POST" == strVerb)
    {

    }
    else if ("PUT" == strVerb)
    {

    }
    else if ("DELETE" == strVerb)
    {

    }

    // Return size of response buffer
    *punSerializedResponseSizeInBytes = stlResponseBuffer.size();
    __DebugAssert(0 < *punSerializedResponseSizeInBytes);

    // Save the response buffer and increment transaction identifier which will be assigned to the next transaction
    ::pthread_mutex_lock(&m_sMutex);
    if (0xFFFFFFFFFFFFFFFF == m_unNextAvailableIdentifier)
    {
        m_unNextAvailableIdentifier = 0;
    }
    un64Identifier = m_unNextAvailableIdentifier;
    m_unNextAvailableIdentifier++;
    m_stlCachedResponse[un64Identifier] = stlResponseBuffer;
    ::pthread_mutex_unlock(&m_sMutex);

    return un64Identifier;
}


/********************************************************************************************
 *
 * @class DataFederationManager
 * @function GetResponse
 * @brief Method called by flat function GetResponse to get plugin's response
 * @param[in] un64Identifier is the transaction identifier
 * @param[out] c_pbSerializedResponseBuffer points to the GetResponse
 * @params[in] unSerializedResponseBufferSizeInBytes is used to verify the request
 * @returns a boolean that represents status of the request
 *
********************************************************************************************/

bool __thiscall DataFederationManager::GetResponse(
    _in uint64_t un64Identifier,
    _out Byte * pbSerializedResponseBuffer,
    _in unsigned int unSerializedResponseBufferSizeInBytes
    )
{
    __DebugFunction();
    __DebugAssert(0xFFFFFFFFFFFFFFFF != un64Identifier);
    __DebugAssert(nullptr != pbSerializedResponseBuffer);
    __DebugAssert(0 < unSerializedResponseBufferSizeInBytes);

    bool fSuccess = false;

    ::pthread_mutex_lock(&m_sMutex);
    if (m_stlCachedResponse.end() != m_stlCachedResponse.find(un64Identifier))
    {
        __DebugAssert(0 < m_stlCachedResponse[un64Identifier].size());

        ::memcpy((void *) pbSerializedResponseBuffer, (const void *) m_stlCachedResponse[un64Identifier].data(), m_stlCachedResponse[un64Identifier].size());
        m_stlCachedResponse.erase(un64Identifier);
        fSuccess = true;
    }
    ::pthread_mutex_unlock(&m_sMutex);

    return fSuccess;
}

