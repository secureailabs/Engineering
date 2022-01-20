/*********************************************************************************************
 *
 * @file RootOfTrustCore.h
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "AuditEventManagedQueues.h"
#include "CoreTypes.h"
#include "Object.h"
#include "RootOfTrustCoreProperties.h"
#include "Socket.h"
#include "SmartMemoryAllocator.h"
#include "StructuredBuffer.h"
#include "ThreadManager.h"

#include <mutex>
#include <queue>
#include <string>
#include <vector>

/********************************************************************************************/

class RootOfTrustCore : public Object
{
    public:

        // Method used to fetch the singleton instance of this class
        static RootOfTrustCore * __stdcall GetInstance(void);

        // This function must be called as soon as the Initializer Process is done
        // collecting all initialization parameters. The initialization function
        // also spins up all of the necessary threads, etc...
        void __thiscall Initialize(
            _in const std::vector<Byte> & c_stlSerializedInitializationParameters
            );
        // Once the RootOfTrustCore is initialize, all processing is internalized. All the
        // main code can do is wait for the RootOfTrustCode to terminate
        void __thiscall WaitForTermination(void) throw();

        // Methods used to fetch information required to interact with other processes
        std::string __thiscall GetDataDomainIdentifier(void) const throw();
        std::string __thiscall GetComputationalDomainIdentifier(void) const throw();
        std::string __thiscall GetRootOfTrustIpcPath(void) const throw();

    private:

        // The constructor for this class is private because it is a singleton instance
        RootOfTrustCore(void);
        // The destructor for this class is also private and is called automatically
        // as soon as the WaitForTermination() method detects termination.
        virtual ~RootOfTrustCore(void);
        // This method runs on it's own thread and is responsible for dispatching
        // audit events on a periodic basis as well as dispatching of heartbeat events
        void __thiscall AuditEventDispatcher(void) throw();
        // Static methods used to spin up threads
        static void * __stdcall RootOfTrustIpcListenerThread(
            _in void * pParameter
            );
        static void * __stdcall RootOfTrustTransactionHandlerThread(
            _in void * pParameter
            );
        static void * __stdcall RootOfTrustAuditEventDispatcherThread(
            _in void * pParameter
            );
        // This method is responsible for listening to incoming transactions and dispatching
        // then to the HandleIncomingTransaction method
        void __thiscall RunIpcListener(void);
        void __thiscall HandleIncomingTransaction(
            _in Socket * poSocket
            );
        // The following set of methods are all of the individual methods used to handle
        // individual transactions
        std::vector<Byte> __thiscall HandleRegisterResearcherTransaction(
            _in const StructuredBuffer & c_oTransactionParameters
            ) throw();
        std::vector<Byte> __thiscall HandlePutDatasetTransaction(
            _in const StructuredBuffer & c_oTransactionParameters
            ) throw();
        std::vector<Byte> __thiscall HandleGetDatasetTransaction(
            _in const StructuredBuffer & c_oTransactionParameters
            ) throw();
        std::vector<Byte> __thiscall HandleAuditEventTransaction(
            _in const StructuredBuffer & c_oTransactionParameters
            ) throw();
        // Method used to record audit events generated within the RootOfTrustCore class
        void __thiscall RecordInternalAuditEvent(
            _in const char * c_szEventName,
            _in Word wTargetChannelsBitMask,
            _in Dword dwEventType,
            _in const StructuredBuffer & c_oEventData
            );
        // The following methods are specialized functions dedicated at the initialization
        // of different parts of the RootOfTrustCode. These particular methods are dedicated at
        // updating the state of the virtual machine
        bool __thiscall RegisterVirtualMachine(void);
        bool __thiscall RegisterDataOwnerEosb(void);
        bool __thiscall RegisterResearcherEosb(void);

        // Private Data members
        static RootOfTrustCore * ms_RootOfTrustCoreSingletonInstance;
        AuditEventManagedQueues m_oAuditEventManagedQueues;
        RootOfTrustCoreProperties m_oRootOfTrustCoreProperties;
        bool m_fIsInitialized;
        bool m_fIsRunning;
};