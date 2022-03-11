/*********************************************************************************************
 *
 * @file DataFederationManager.h
 * @author David Gascon
 * @date 10 Mar 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/
#pragma once

#include "DebugLibrary.h"
#include "EntityTypes.h"
#include "ExceptionRegister.h"
#include "Exceptions.h"
#include "Object.h"
#include "PluginDictionary.h"
#include "RestFrameworkSharedFunctions.h"
#include "StructuredBuffer.h"
#include "Socket.h"
#include "SocketServer.h"
#include "ThreadManager.h"

#include <pthread.h>
#include <string.h>

#include <iostream>
#include <map>
#include <vector>

/********************************************************************************************/

class DataFederationManager : public Object
{
    public:
        // Constructor and destructor
        DataFederationManager(void);
        DataFederationManager(
            _in const DataFederationManager & c_oAuditLogManager
          );
        virtual ~DataFederationManager(void);

        // Property accessor methods
        const char * __thiscall GetName(void) const throw();
        const char * __thiscall GetUuid(void) const throw();
        Qword __thiscall GetVersion(void) const throw();
        std::vector<Byte> __thiscall GetDictionarySerializedBuffer(void) const throw();

        void __thiscall TerminateSignalEncountered(void);

        void __thiscall InitializePlugin(const StructuredBuffer& oInitializationVectors);

        uint64_t __thiscall SubmitRequest(
            _in const StructuredBuffer & c_oRequestStructuredBuffer,
            _out unsigned int * punSerializedResponseSizeInBytes
            );

        bool __thiscall GetResponse(
            _in uint64_t un64Identifier,
            _out Byte * pbSerializedResponseBuffer,
            _in unsigned int unSerializedResponseBufferSizeInBytes
            );

    private:

        // FILL IN API CALLS HERE

        // Private data members
        mutable pthread_mutex_t m_sMutex;
        std::map<Qword, std::vector<Byte>> m_stlCachedResponse;
        uint64_t m_unNextAvailableIdentifier;
        PluginDictionary m_oDictionary;
        bool m_fTerminationSignalEncountered;

        std::string m_strDatabaseServiceIpAddr;
        uint32_t m_unDatabaseServiceIpPort;
};

/********************************************************************************************/

extern DataFederationManager * __stdcall GetDataFederationManager(void);
extern void __stdcall ShutdownDataFederationManager(void);
