/*********************************************************************************************
 *
 * @file DataFederationManager.cpp
 * @author David Gascon
 * @date 10 Mar 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 * @brief
 ********************************************************************************************/

#include <DataFederation.h>

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
 * @function SendRequestToDatabase
 * @brief Send a StructuredBuffer request over TLS to a remote database
 * @return Return the StructuredBuffer response, or throw on error
 *
 ********************************************************************************************/
static StructuredBuffer __stdcall SendRequestToDatabase(
    _in const StructuredBuffer& c_oRequest,
    _in const std::string& c_strDestinationIpAddress,
    _in const uint16_t c_unDestinationPort
    )
{
    std::vector<Byte> stlResponse;
    std::unique_ptr<TlsNode> poTlsNode{nullptr};
    std::vector<Byte> stlRequest = ::CreateRequestPacketFromStructuredBuffer(c_oRequest);
    poTlsNode.reset(::TlsConnectToNetworkSocket(c_strDestinationIpAddress.c_str(), c_unDestinationPort));
    // Send request packet
    poTlsNode->Write(stlRequest.data(), (stlRequest.size()));

    // Read header and body of the response
    std::vector<Byte> stlRestResponseLength = poTlsNode->Read(sizeof(uint32_t), 3000);
    _ThrowBaseExceptionIf((0 == stlRestResponseLength.size()), "Dead Packet.", nullptr);
    unsigned int unResponseDataSizeInBytes = *((uint32_t *)stlRestResponseLength.data());
    stlResponse = poTlsNode->Read(unResponseDataSizeInBytes, 100);
    _ThrowBaseExceptionIf((0 == stlResponse.size()), "Dead Packet.", nullptr);

    return StructuredBuffer(stlResponse);
}

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

    StructuredBuffer oRequiredStringElement;
    oRequiredStringElement.PutByte("ElementType", ANSI_CHARACTER_STRING_VALUE_TYPE);
    oRequiredStringElement.PutBoolean("IsRequired", true);

    StructuredBuffer oRequriedBufferElement;
    oRequriedBufferElement.PutByte("ElementType", BUFFER_VALUE_TYPE);
    oRequriedBufferElement.PutBoolean("IsRequired", true);

    StructuredBuffer oRequiredGuidElement;
    oRequiredGuidElement.PutByte("ElementType", GUID_VALUE_TYPE);
    oRequiredGuidElement.PutBoolean("IsRequired", true);

    StructuredBuffer oRegisterNewDataFederationParameters;
    oRegisterNewDataFederationParameters.PutStructuredBuffer("Eosb", oRequriedBufferElement);
    oRegisterNewDataFederationParameters.PutStructuredBuffer("DataFederationName",oRequiredStringElement);
    oRegisterNewDataFederationParameters.PutStructuredBuffer("DataFederationDescription", oRequiredStringElement);

    StructuredBuffer oListDataFederationParameters;
    oListDataFederationParameters.PutStructuredBuffer("Eosb", oRequriedBufferElement);

    StructuredBuffer oDeleteDataFederationParameters;
    oDeleteDataFederationParameters.PutStructuredBuffer("Eosb", oRequriedBufferElement);
    oDeleteDataFederationParameters.PutStructuredBuffer("DataFederationIdentifier", oRequiredGuidElement);

    m_oDictionary.AddDictionaryEntry("POST","/SAIL/DataFederationManager/RegisterDataFederation",oRegisterNewDataFederationParameters, 1);
    m_oDictionary.AddDictionaryEntry("GET","/SAIL/DataFederationManager/ListDataFederations",oListDataFederationParameters, 1);
    m_oDictionary.AddDictionaryEntry("DELETE", "/SAIL/DataFederationManager/DeleteDataFederation", oDeleteDataFederationParameters, 1);

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
        if ("/SAIL/DataFederationManager/ListDataFederations" == strResource)
        {
            stlResponseBuffer = ListDataFederations(c_oRequestStructuredBuffer);
        }
    }
    else if ("POST" == strVerb)
    {
        if ("/SAIL/DataFederationManager/RegisterDataFederation" == strResource)
        {
            stlResponseBuffer = RegisterDataFederation(c_oRequestStructuredBuffer);
        }
    }
    else if ("PUT" == strVerb)
    {

    }
    else if ("DELETE" == strVerb)
    {
        if ("/SAIL/DataFederationManager/DeleteDataFederation" == strResource)
        {
            stlResponseBuffer = DeleteDataFederation(c_oRequestStructuredBuffer);
        }
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

/********************************************************************************************
 *
 * @class DataFederationManager
 * @function RegisterDataFederation
 * @brief Method called by flat function SubmitRequest when a client requests for the plugin's resource
 * @param[in] c_oRequest the structued buffer that contains the request's information
 * @returns std::vector<Byte> stores the serialized response
 *
 ********************************************************************************************/
std::vector<Byte> __thiscall DataFederationManager::RegisterDataFederation(
    _in const StructuredBuffer & c_oRequest
    )
{
    __DebugFunction();

    StructuredBuffer oResponse;
    std::unique_ptr<TlsNode> poTlsNode{nullptr};
    Dword dwStatus{400};

    try
    {
        StructuredBuffer oUserInfo = ::GetUserInfoFromEosb(c_oRequest);
        if (200 == oUserInfo.GetDword("Status"))
        {
            // Create indentifiers for this new object
            Guid oNewFederationIdentifier{eDataFederation};
            Guid oDataFederationOwnerIdentifier{oUserInfo.GetGuid("OrganizationGuid")};
            std::string strDatasetFamilyOwner = oDataFederationOwnerIdentifier.ToString(eHyphensAndCurlyBraces);
            std::string strNewFederationIdentifier{oNewFederationIdentifier.ToString(eHyphensAndCurlyBraces)};

            // Validate the request
            std::string strNewFederationName = c_oRequest.GetString("DataFederationName");
            std::string strNewFederationDescription = c_oRequest.GetString("DataFederationDescription");

            _ThrowBaseExceptionIf(1 >= strNewFederationName.size(), "New name too small", nullptr);
            _ThrowBaseExceptionIf(255 < strNewFederationName.size(), "New name too large (255 max)", nullptr);
            _ThrowBaseExceptionIf(1 >= strNewFederationDescription.size(), "New description too small", nullptr);
            _ThrowBaseExceptionIf(1000 < strNewFederationDescription.size(), "New description too large (1000 max)", nullptr);

            // Build the new Data Federation Object
            DataFederation oNewDataFederation{oNewFederationIdentifier,
                oDataFederationOwnerIdentifier,
                strNewFederationName,
                strNewFederationDescription};

            // Submit the request to the database for storage
            StructuredBuffer oDatabaseRequest;
            oDatabaseRequest.PutString("PluginName", "DatabaseManager");
            oDatabaseRequest.PutString("Verb", "POST");
            oDatabaseRequest.PutString("Resource", "/SAIL/DatabaseManager/RegisterDataFederation");
            oDatabaseRequest.PutStructuredBuffer("DataFederation", oNewDataFederation.ToStructuredBuffer());

            StructuredBuffer oDatabaseResponse{::SendRequestToDatabase(oDatabaseRequest, m_strDatabaseServiceIpAddr, m_unDatabaseServiceIpPort)};

            if (201 == oDatabaseResponse.GetDword("Status") )
            {
                oResponse.PutBuffer("Eosb", oUserInfo.GetBuffer("Eosb"));
                dwStatus = 201;
            }
            else
            {
                dwStatus = oDatabaseResponse.GetDword("Status");
            }
        }
    }
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oResponse.Clear();
    }
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    oResponse.PutDword("Status", dwStatus);
    return oResponse.GetSerializedBuffer();
}

/********************************************************************************************
 *
 * @class DataFederationManager
 * @function ListDataFederations
 * @brief Method called by flat function SubmitRequest when a client requests for the plugin's resource
 * @param[in] c_oRequest the structued buffer that contains the request's information
 * @returns std::vector<Byte> stores the serialized response
 *
 ********************************************************************************************/
std::vector<Byte>__thiscall DataFederationManager::ListDataFederations(
    _in const StructuredBuffer & c_oRequest
    )
{
    __DebugFunction();

    StructuredBuffer oResponse;
    Dword dwStatus{400};
    try
    {
        StructuredBuffer oUserInfo = ::GetUserInfoFromEosb(c_oRequest);
        if (200 == oUserInfo.GetDword("Status"))
        {
            // Create a request to get the database manager to query for the organization GUID
            StructuredBuffer oDatabaseRequest;
            oDatabaseRequest.PutString("PluginName", "DatabaseManager");
            oDatabaseRequest.PutString("Verb", "GET");
            oDatabaseRequest.PutString("Resource", "/SAIL/DatabaseManager/DataFederations");
            oDatabaseRequest.PutGuid("RequestingUserOrganizationIdentifier", oUserInfo.GetGuid("OrganizationGuid"));

            StructuredBuffer oDatabaseResponse{::SendRequestToDatabase(oDatabaseRequest, m_strDatabaseServiceIpAddr, m_unDatabaseServiceIpPort)};

            if (200 == oDatabaseResponse.GetDword("Status"))
            {
                oResponse.PutBuffer("Eosb", oUserInfo.GetBuffer("Eosb"));
                oResponse.PutStructuredBuffer("DataFederations", oDatabaseResponse.GetStructuredBuffer("DataFederations"));
                dwStatus = 200;
            }
            else
            {
                dwStatus = oDatabaseResponse.GetDword("Status");
            }
        }
    }
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oResponse.Clear();
    }
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    oResponse.PutDword("Status", dwStatus);
    return oResponse.GetSerializedBuffer();
}


/********************************************************************************************
 *
 * @class DataFederationManager
 * @function DeleteDataFederation
 * @brief Method called by flat function SubmitRequest when a client requests for the plugin's resource
 * @param[in] c_oRequest the structued buffer that contains the request's information
 * @returns std::vector<Byte> stores the serialized response
 *
 ********************************************************************************************/
std::vector<Byte> __thiscall DataFederationManager::DeleteDataFederation(
    _in const StructuredBuffer & c_oRequest
    )
{
    __DebugFunction();

    StructuredBuffer oResponse;
    Dword dwStatus{400};
    try
    {
        StructuredBuffer oUserInfo = ::GetUserInfoFromEosb(c_oRequest);
        if (200 == oUserInfo.GetDword("Status"))
        {
            // TODO - There are additional rules to determine when we can delete that are not scoped out yet
            bool fValidatedDeleteRequest{true};
            if (true == fValidatedDeleteRequest)
            {
                // Create a request to get the database manager to query for the organization GUID
                StructuredBuffer oDatabaseRequest;
                oDatabaseRequest.PutString("PluginName", "DatabaseManager");
                oDatabaseRequest.PutString("Verb", "GET");
                oDatabaseRequest.PutString("Resource", "/SAIL/DatabaseManager/DataFederation");
                oDatabaseRequest.PutGuid("DataFederationIdentifier", c_oRequest.GetGuid("DataFederationIdentifier"));

                StructuredBuffer oDatabaseResponse{::SendRequestToDatabase(oDatabaseRequest, m_strDatabaseServiceIpAddr, m_unDatabaseServiceIpPort)};

                if (200 == oDatabaseResponse.GetDword("Status"))
                {
                    // Set this federation to inactive if we own it
                    DataFederation oReturnedFederation{oDatabaseResponse.GetStructuredBuffer("DataFederation")};
                    if (oReturnedFederation.OrganizationOwnerIdentifier() == oUserInfo.GetGuid("OrganizationGuid"))
                    {
                        oReturnedFederation.SetInactive();
                        // Create a request to get the database manager to store the updated object
                        StructuredBuffer oDataStoreRequest;
                        oDataStoreRequest.PutString("PluginName", "DatabaseManager");
                        oDataStoreRequest.PutString("Verb", "PUT");
                        oDataStoreRequest.PutString("Resource", "/SAIL/DatabaseManager/UpdateDataFederation");
                        oDataStoreRequest.PutStructuredBuffer("DataFederation", oReturnedFederation.ToStructuredBuffer());

                        StructuredBuffer oDatabaseResponse{::SendRequestToDatabase(oDataStoreRequest, m_strDatabaseServiceIpAddr, m_unDatabaseServiceIpPort)};
                        dwStatus = oDatabaseResponse.GetDword("Status");
                        if (200 == dwStatus)
                        {
                            oResponse.PutBuffer("Eosb", oUserInfo.GetBuffer("Eosb"));
                        }
                    }
                    else
                    {
                        dwStatus = 403;
                    }
                }
                else
                {
                    dwStatus = oDatabaseResponse.GetDword("Status");
                }
            }
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    catch(std::exception & e)
    {
        std::cout << "Exception: " << e.what() << '\n';
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    oResponse.PutDword("Status", dwStatus);
    return oResponse.GetSerializedBuffer();
}
