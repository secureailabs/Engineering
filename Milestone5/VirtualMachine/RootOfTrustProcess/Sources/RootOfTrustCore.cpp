/*********************************************************************************************
 *
 * @file RootOfTrustCore.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "64BitHashes.h"
#include "ApiCallHelpers.h"
#include "Base64Encoder.h"
#include "DateAndTime.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "HardCodedCryptographicKeys.h"
#include "IpcTransactionHelperFunctions.h"
#include "RootOfTrustCore.h"
#include "SmartMemoryAllocator.h"
#include "SocketServer.h"
#include "StatusMonitor.h"
#include "ThreadManager.h"
#include "CurlRest.h"
#include "Utils.h"
#include "JsonValue.h"

#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>

#include <iostream>
#include <mutex>

// Global smart memory allocator that is used to allocate and deallocate RootOfTrustTransactionPacket
// memory blocks
static std::mutex gs_stlMutex;
RootOfTrustCore * RootOfTrustCore::ms_RootOfTrustCoreSingletonInstance = nullptr;

/********************************************************************************************/

RootOfTrustCore * __stdcall RootOfTrustCore::GetInstance(void)
{
    __DebugFunction();

    const std::lock_guard<std::mutex> lock(gs_stlMutex);
    if (nullptr == ms_RootOfTrustCoreSingletonInstance)
    {
        ms_RootOfTrustCoreSingletonInstance = new RootOfTrustCore();
    }

    return ms_RootOfTrustCoreSingletonInstance;
}

/********************************************************************************************/

RootOfTrustCore::RootOfTrustCore(void)
{
    __DebugFunction();
    __DebugAssert(nullptr == ms_RootOfTrustCoreSingletonInstance);

    ms_RootOfTrustCoreSingletonInstance = this;
    m_fIsInitialized = false;
    m_fIsRunning = false;
}

/********************************************************************************************/

RootOfTrustCore::~RootOfTrustCore(void)
{
    __DebugFunction();
    __DebugAssert(false == m_fIsRunning);

    // Wait for all of our threads to end
    ThreadManager * poThreadManager = ThreadManager::GetInstance();
    if (nullptr != poThreadManager)
    {
        poThreadManager->JoinThreadGroup("RootOfTrustCoreThreadGroup");
    }
    // Singleton instance is dying
    ms_RootOfTrustCoreSingletonInstance = nullptr;
}

/********************************************************************************************/

void __thiscall RootOfTrustCore::Initialize(
    _in const std::vector<Byte> & c_stlSerializedInitializationParameters
    )
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(false == m_fIsInitialized);
    __DebugAssert(false == m_fIsRunning);

    StructuredBuffer oInitializationParameters(c_stlSerializedInitializationParameters);
    // Reality check, to make sure that everything is where it is supposed to be
    m_oRootOfTrustCoreProperties.SetProperty("SailPlatformServicesIpAddress", oInitializationParameters.GetString("SailPlatformServicesIpAddress"));
    m_oRootOfTrustCoreProperties.SetProperty("VirtualMachineName", oInitializationParameters.GetString("VirtualMachineName"));
    m_oRootOfTrustCoreProperties.SetProperty("VirtualMachineIpAddress", oInitializationParameters.GetString("VirtualMachineIpAddress"));
    m_oRootOfTrustCoreProperties.SetProperty("VirtualMachineIdentifier", oInitializationParameters.GetString("VirtualMachineIdentifier"));
    m_oRootOfTrustCoreProperties.SetProperty("VirtualMachineClusterIdentifier", oInitializationParameters.GetString("VirtualMachineClusterIdentifier"));
    m_oRootOfTrustCoreProperties.SetProperty("RootOfTrustDomainIdentifier", oInitializationParameters.GetString("RootOfTrustDomainIdentifier"));
    m_oRootOfTrustCoreProperties.SetProperty("ComputationalDomainIdentifier", oInitializationParameters.GetString("VirtualMachineName"));
    m_oRootOfTrustCoreProperties.SetProperty("DataDomainIdentifier", oInitializationParameters.GetString("DataDomainIdentifier"));
    m_oRootOfTrustCoreProperties.SetProperty("DigitalContractIdentifier", oInitializationParameters.GetString("DigitalContractIdentifier"));
    m_oRootOfTrustCoreProperties.SetProperty("DatasetIdentifier", oInitializationParameters.GetString("DatasetIdentifier"));
    // Add some values to RootOfTrustCoreProperties which were not sent in by the
    // remote initializer
    m_oRootOfTrustCoreProperties.SetProperty("RootOfTrustIpcPath", Guid().ToString(eRaw));
    m_oRootOfTrustCoreProperties.SetProperty("ComputationalDomainIpcPath", Guid().ToString(eRaw));
    m_oRootOfTrustCoreProperties.SetProperty("DataDomainIpcPath", Guid().ToString(eRaw));
    // Make sure to register the IP address of the SAIL Platform Services API Portal before we start
    ::SetIpAddressOfSailWebApiPortalGateway(m_oRootOfTrustCoreProperties.GetProperty("SailPlatformServicesIpAddress"), 6200);
    // Okay, we are fully initialized
    m_fIsInitialized = true;
    // Let's initialize this virtual machine (causes API call into SAIL Platform Services API Portal)
    this->RegisterVirtualMachine();
    __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineAuditEventParentBranchNodeIdentifier").size());
    // Now, we initialize our threads
    m_fIsRunning = true;
    ThreadManager * poThreadManager = ThreadManager::GetInstance();
    _ThrowBaseExceptionIf((0xFFFFFFFFFFFFFFFF == poThreadManager->CreateThread("RootOfTrustCoreThreadGroup", RootOfTrustAuditEventDispatcherThread, (void *) this)), "Failed to start the audit event dispacher thread", nullptr);
    _ThrowBaseExceptionIf((0xFFFFFFFFFFFFFFFF == poThreadManager->CreateThread("RootOfTrustCoreThreadGroup", RootOfTrustIpcListenerThread, (void *) this)), "Failed to start the Root of Trust Listener Thread", nullptr);
}

/********************************************************************************************/

void __thiscall RootOfTrustCore::WaitForTermination(void) throw()
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);
    __DebugAssert(true == m_fIsRunning);

    StatusMonitor oStatusMonitor("void __thiscall RootOfTrustCore::WaitForTermination(void)");
    ThreadManager * poThreadManager = ThreadManager::GetInstance();
    // Wait for ALL threads started by the RootOfTrustCore object. This is a blocking functions
    poThreadManager->JoinThreadGroup("RootOfTrustCoreThreadGroup");
    // All threads are done/
    m_fIsRunning = false;
}

/********************************************************************************************/

std::string __thiscall RootOfTrustCore::GetDataDomainIdentifier(void) const throw()
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);

    // Make sure to make our data access thread safe

    return m_oRootOfTrustCoreProperties.GetProperty("DataDomainIdentifier");
}

/********************************************************************************************/

std::string __thiscall RootOfTrustCore::GetComputationalDomainIdentifier(void) const throw()
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);

    return m_oRootOfTrustCoreProperties.GetProperty("ComputationalDomainIdentifier");
}

/********************************************************************************************/

std::string __thiscall RootOfTrustCore::GetRootOfTrustIpcPath(void) const throw()
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);

    return m_oRootOfTrustCoreProperties.GetProperty("RootOfTrustIpcPath");
}

/********************************************************************************************/

void __thiscall RootOfTrustCore::AuditEventDispatcher(void) throw()
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);
    __DebugAssert(true == m_fIsRunning);

    StatusMonitor oStatusMonitor("void __thiscall RootOfTrustCore::AuditEventDispatcher(void)");
    bool fIsShuttingDown = false;
    bool fIsDone = false;
    uint64_t un64StartTimestampInMilliseconds = ::GetEpochTimeInMilliseconds();

    // Keep on looping until all of the event queues are empty and fIsShutdown = true
    while (false == fIsDone)
    {
        // We need to  put the try..catch block INSIDE of the while loop in case something happens. This prevents
        // exceptions from causing this thread to stop running (which is really bad).
        try
        {
            // Track two different elapsed times, used to trigger audit event uploads every 30 seconds and used to trigger
            // heartbeasts every 20 seconds
            uint64_t un64ElapsedTimeInMilliseconds = ::GetEpochTimeInMilliseconds() - un64StartTimestampInMilliseconds;

            if ((true == fIsShuttingDown)||(30000 < un64ElapsedTimeInMilliseconds))
            {
                bool fHeartbeatHasBeenSent = false;
                std::string strEosb = m_oRootOfTrustCoreProperties.GetProperty("ResearcherEosb");
                std::queue<std::string> strAuditEventQueue = m_oAuditEventManagedQueues.GetQueuedAuditEvents(0x0010);
                // Process audit events generated within the researcher organization
                if ((0 < strEosb.size())&&(0 < strAuditEventQueue.size()))
                {
                    __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("ResearchOrganizationAuditEventParentBranchNodeIdentifier").size());

                    if (0 < strAuditEventQueue.size())
                    {
                        StructuredBuffer oAuditEventsToTransmit;
                        unsigned int unElementIndex = 0;

                        while (0 < strAuditEventQueue.size())
                        {
                            oAuditEventsToTransmit.PutString(std::to_string(unElementIndex++).c_str(), strAuditEventQueue.front());
                            strAuditEventQueue.pop();
                        }

                        // Send the audit events
                        oAuditEventsToTransmit.PutBoolean("__IsArray__", true);
                        ::TransmitAuditEventsToSailWebApiPortal(strEosb, m_oRootOfTrustCoreProperties.GetProperty("ResearcherOrganizationAuditEventParentBranchNodeIdentifier"), oAuditEventsToTransmit);
                    }

                    // Now send the heartbeat. This will cause the virtual machine to show a status of "In Use"
                    __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineIdentifier").size());
                    __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("ResearchUserIdentifier").size());
                    fHeartbeatHasBeenSent = ::VirtualMachineStatusUpdate(strEosb, m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineIdentifier"), 0x00000006, m_oRootOfTrustCoreProperties.GetProperty("ResearchUserIdentifier"));
                }

                strEosb = m_oRootOfTrustCoreProperties.GetProperty("DataOwnerEosb");
                strAuditEventQueue = m_oAuditEventManagedQueues.GetQueuedAuditEvents(0x0100);
                // Process audit events generated by within the data owner organization
                if ((0 < strEosb.size())&&(0 < strAuditEventQueue.size()))
                {
                    __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("DataOrganizationAuditEventParentBranchNodeIdentifier").size());

                    if (0 < strAuditEventQueue.size())
                    {
                        StructuredBuffer oAuditEventsToTransmit;
                        unsigned int unElementIndex = 0;

                        while (0 < strAuditEventQueue.size())
                        {
                            oAuditEventsToTransmit.PutString(std::to_string(unElementIndex++).c_str(), strAuditEventQueue.front());
                            strAuditEventQueue.pop();
                        }

                        // Send the audit events
                        oAuditEventsToTransmit.PutBoolean("__IsArray__", true);
                        ::TransmitAuditEventsToSailWebApiPortal(strEosb, m_oRootOfTrustCoreProperties.GetProperty("DataOrganizationAuditEventParentBranchNodeIdentifier"), oAuditEventsToTransmit);
                    }

                    if (false == fHeartbeatHasBeenSent)
                    {
                        // Now send the heartbeat. This will cause the virtual machine to show a status of "Ready to Use"
                        __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineIdentifier").size());
                        __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("DataOwnerUserIdentifier").size());
                        fHeartbeatHasBeenSent = ::VirtualMachineStatusUpdate(strEosb, m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineIdentifier"), 0x00000005, m_oRootOfTrustCoreProperties.GetProperty("DataOwnerUserIdentifier"));
                    }
                }

                strEosb = m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineEosb");
                strAuditEventQueue = m_oAuditEventManagedQueues.GetQueuedAuditEvents(0x0001);
                // Process audit events generated by within the data owner organization
                if ((0 < strEosb.size())&&(0 < strAuditEventQueue.size()))
                {
                    __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineAuditEventParentBranchNodeIdentifier").size());

                    if (0 < strAuditEventQueue.size())
                    {
                        StructuredBuffer oAuditEventsToTransmit;
                        unsigned int unElementIndex = 0;

                        while (0 < strAuditEventQueue.size())
                        {
                            oAuditEventsToTransmit.PutString(std::to_string(unElementIndex++).c_str(), strAuditEventQueue.front());
                            strAuditEventQueue.pop();
                        }

                        // Send the audit events
                        oAuditEventsToTransmit.PutBoolean("__IsArray__", true);
                        ::TransmitAuditEventsToSailWebApiPortal(strEosb, m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineAuditEventParentBranchNodeIdentifier"), oAuditEventsToTransmit);
                    }

                    // If neither the researcher or data owner EOSB's are registered, then we need to sent this
                    if (false == fHeartbeatHasBeenSent)
                    {
                        // Now send the heartbeat. This will cause the virtual machine to show a status of "Waiting for Data"
                        __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineEosb").size());
                        __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineIdentifier").size());
                        __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineUserIdentifier").size());
                        fHeartbeatHasBeenSent = ::VirtualMachineStatusUpdate(m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineEosb"), m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineIdentifier"), 0x00000005, m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineUserIdentifier"));
                    }
                }

                // Reset the start timestamp back to the latest.
                un64StartTimestampInMilliseconds = ::GetEpochTimeInMilliseconds();

                // Reality check around the heartbeat
                _ThrowBaseExceptionIf((false == fHeartbeatHasBeenSent), "ERROR: Virtual Machine Heartbeat was not sent", nullptr);
            }

            // Are we shutting down?
            fIsShuttingDown = oStatusMonitor.IsTerminating();
            // Are we done?
            if ((true == fIsShuttingDown)&&(0 == m_oAuditEventManagedQueues.GetQueuedAuditEventsCount(0x1111)))
            {
                fIsDone = true;
            }
        }

        catch (const BaseException & c_oBaseException)
        {
            ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
        }

        catch(...)
        {
            ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        }

        // Put this thread to sleep for 1/10th of a second
        ::usleep(100);
    }
}

/********************************************************************************************/

void * __stdcall RootOfTrustCore::RootOfTrustIpcListenerThread(
    _in void * pParameter
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != pParameter);

    RootOfTrustCore * poRootOfTrustCore = RootOfTrustCore::GetInstance();
    poRootOfTrustCore->RunIpcListener();

    return nullptr;
}

/********************************************************************************************/

void * __stdcall RootOfTrustCore::RootOfTrustTransactionHandlerThread(
    _in void * pParameter
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != pParameter);

    RootOfTrustCore * poRootOfTrustCore = RootOfTrustCore::GetInstance();
    poRootOfTrustCore->HandleIncomingTransaction((Socket *) pParameter);

    return nullptr;
}

/********************************************************************************************/

void * __stdcall RootOfTrustCore::RootOfTrustAuditEventDispatcherThread(
    _in void * pParameter
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != pParameter);

    RootOfTrustCore * poRootOfTrustCore = RootOfTrustCore::GetInstance();
    poRootOfTrustCore->AuditEventDispatcher();

    return nullptr;
}

/********************************************************************************************/

void __thiscall RootOfTrustCore::RunIpcListener(void)
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);
    __DebugAssert(true == m_fIsRunning);

    try
    {
        StatusMonitor oStatusMonitor("void __thiscall RootOfTrustCore::RunIpcListener(void)");
        SocketServer * poIpcServer = new SocketServer(m_oRootOfTrustCoreProperties.GetProperty("RootOfTrustIpcPath").c_str());
        _ThrowOutOfMemoryExceptionIfNull(poIpcServer);
        ThreadManager * poThreadManager = ThreadManager::GetInstance();
        unsigned int unNumberOfLoops = 0;
        unsigned int unNumberOfSuccessfulTransactions = 0;
        unsigned int unNumberOfFailedTransactions = 0;
        // Loop until the status monitor signals that things are terminating
        while (false == oStatusMonitor.IsTerminating())
        {
            // We wait for a connection
            if (true == poIpcServer->WaitForConnection(1000))
            {
                Socket * poSocket = poIpcServer->Accept();
                if (nullptr != poSocket)
                {
                    if (0xFFFFFFFFFFFFFFFF == poThreadManager->CreateThread("RootOfTrustCodeGroup", RootOfTrustTransactionHandlerThread, (void *) poSocket))
                    {
                        unNumberOfFailedTransactions++;
                    }
                    else
                    {
                        unNumberOfSuccessfulTransactions++;
                    }
                }
            }
            unNumberOfLoops++;
            //oStatusMonitor.UpdateStatus("unNumberOfLoops = %d, unNumberOfSuccessfulTransactions = %d, unNumberOfFailedTransactions = %d", unNumberOfLoops, unNumberOfSuccessfulTransactions, unNumberOfFailedTransactions);
        }
        // Close out the IPC server for the RootOfTrust
        poIpcServer->Release();
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
}


/********************************************************************************************/

void __thiscall RootOfTrustCore::HandleIncomingTransaction(
    _in Socket * poSocket
    )
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);
    __DebugAssert(true == m_fIsRunning);

    StructuredBuffer oTransactionParameters(::GetIpcTransaction(poSocket, false));
    Guid oOriginatingDomainIdentifier = oTransactionParameters.GetGuid("DomainIdentifier");
    Dword dwTransaction = oTransactionParameters.GetDword("Transaction");
    std::vector<Byte> stlSerializedResponse;
    switch(dwTransaction)
    {
        case 0x00000004 //  "RegisterResearcher"
        :   stlSerializedResponse = this->HandleRegisterResearcherTransaction(oTransactionParameters);
            break;
        case 0x00000005 //  "RegisterDataset"
        :   stlSerializedResponse = this->HandlePutDatasetTransaction(oTransactionParameters);
            break;
        case 0x00000006 //  "GetDataSet"
        :   stlSerializedResponse = this->HandleGetDatasetTransaction(oTransactionParameters);
            break;
        case 0x00000009 // "RecordAuditEvent"
        :   // Audit event don't wait for a response because of performance purposes
            (void) this->HandleAuditEventTransaction(oTransactionParameters);
            break;

    }

    // Send out the response to the transaction if there is a response available only
    if (0 < stlSerializedResponse.size())
    {
        ::PutIpcTransaction(poSocket, stlSerializedResponse);
    }
}

/********************************************************************************************/

std::vector<Byte> __thiscall RootOfTrustCore::HandleRegisterResearcherTransaction(
    _in const StructuredBuffer & c_oTransactionParameters
    ) throw()
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);
    __DebugAssert(true == m_fIsRunning);

    StructuredBuffer oResponseBuffer;

    try
    {
        oResponseBuffer.PutBoolean("Success", false);
        if (c_oTransactionParameters.GetGuid("DomainIdentifier") == Guid(m_oRootOfTrustCoreProperties.GetProperty("ComputationalDomainIdentifier")))
        {
            m_oRootOfTrustCoreProperties.SetProperty("ResearcherEosb", c_oTransactionParameters.GetString("ResearcherEosb"));
            __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("ResearchUserIdentifier").size());
            __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("ResearchOrganizationAuditEventParentBranchNodeIdentifier").size());
            oResponseBuffer.PutBoolean("Success", this->RegisterResearcherEosb());
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return oResponseBuffer.GetSerializedBuffer();
}

/********************************************************************************************/

std::vector<Byte> __thiscall RootOfTrustCore::HandlePutDatasetTransaction(
    _in const StructuredBuffer & c_oTransactionParameters
    ) throw()
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);
    __DebugAssert(true == m_fIsRunning);

    StructuredBuffer oResponseBuffer;

    try
    {
        oResponseBuffer.PutBoolean("Success", false);
        m_oRootOfTrustCoreProperties.SetProperty("DataOwnerEosb", c_oTransactionParameters.GetString("DataOwnerEosb"));
        m_oRootOfTrustCoreProperties.SetProperty("DatasetFilename", c_oTransactionParameters.GetString("DatasetFilename"));
        this->RegisterDataOwnerEosb();
        __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("DataOwnerUserIdentifier").size());
        __DebugAssert(0 < m_oRootOfTrustCoreProperties.GetProperty("DataOrganizationAuditEventParentBranchNodeIdentifier").size());
        oResponseBuffer.PutBoolean("Success", this->RegisterResearcherEosb());
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return oResponseBuffer.GetSerializedBuffer();
}

/********************************************************************************************/

std::vector<Byte> __thiscall RootOfTrustCore::HandleGetDatasetTransaction(
    _in const StructuredBuffer & c_oTransactionParameters
    ) throw()
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);
    __DebugAssert(true == m_fIsRunning);

    StructuredBuffer oResponseBuffer;

    try
    {
        oResponseBuffer.PutBoolean("Success", false);
        if (c_oTransactionParameters.GetGuid("DomainIdentifier") == Guid(m_oRootOfTrustCoreProperties.GetProperty("DataDomainIdentifier")))
        {
            oResponseBuffer.PutString("DatasetFilename", m_oRootOfTrustCoreProperties.GetProperty("DatasetFilename"));
            oResponseBuffer.PutBoolean("Success", true);
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return oResponseBuffer.GetSerializedBuffer();
}

/********************************************************************************************/

std::vector<Byte> __thiscall RootOfTrustCore::HandleAuditEventTransaction(
    _in const StructuredBuffer & c_oTransactionParameters
    ) throw()
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);
    __DebugAssert(true == m_fIsRunning);

    StructuredBuffer oResponseBuffer;

    try
    {
        // By default
        oResponseBuffer.PutBoolean("Success", false);
        // Make a local copy of the transaction parameters since we are going to be making
        // modifications to the parameters
        // Make a copy of the target channels
        std::string strEventName = c_oTransactionParameters.GetString("EventName");
        Word wTargetChannelsBitMask = c_oTransactionParameters.GetWord("TargetChannelsBitMask");
        Dword dwEventType = c_oTransactionParameters.GetDword("EventType");
        StructuredBuffer oEventData = c_oTransactionParameters.GetStructuredBuffer("EventData");
        // Register the event
        m_oAuditEventManagedQueues.AddAuditEvent(strEventName, wTargetChannelsBitMask, dwEventType, oEventData);
        // If we get here, the audit event was recorded
        oResponseBuffer.PutBoolean("Success", true);
    }

    catch (BaseException c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return oResponseBuffer.GetSerializedBuffer();
}

/********************************************************************************************/

bool __thiscall RootOfTrustCore::RegisterVirtualMachine(void)
{
    __DebugFunction();
    __DebugAssert(this == ms_RootOfTrustCoreSingletonInstance);
    __DebugAssert(true == m_fIsInitialized);
    __DebugAssert(false == m_fIsRunning);   // We should NOT be running yet

    bool fSuccess = false;

    try
    {
        StructuredBuffer oResponse(::RegisterVirtualMachineAfterInitialization(m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineEosb"), m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineIdentifier"), m_oRootOfTrustCoreProperties.GetProperty("DigitalContractIdentifier"), m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineIpAddress")));
        m_oRootOfTrustCoreProperties.SetProperty("VirtualMachineAuditEventParentBranchNodeIdentifier", oResponse.GetString("VirtualMachineAuditEventParentBranchNodeIdentifier"));
        fSuccess = true;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return fSuccess;
}

/********************************************************************************************/

bool __thiscall RootOfTrustCore::RegisterDataOwnerEosb(void)
{
    __DebugFunction();

    bool fSuccess = false;

    try
    {
        StructuredBuffer oResponse(::RegisterVirtualMachineDataOwner(m_oRootOfTrustCoreProperties.GetProperty("DataOwnerEosb"), m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineIdentifier")));
        m_oRootOfTrustCoreProperties.SetProperty("DataOwnerUserIdentifier", oResponse.GetString("DataOwnerUserIdentifier"));
        m_oRootOfTrustCoreProperties.SetProperty("DataOrganizationAuditEventParentBranchNodeIdentifier", oResponse.GetString("DataOrganizationAuditEventParentBranchNodeIdentifier"));
        fSuccess = true;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return fSuccess;
}

/********************************************************************************************/

bool __thiscall RootOfTrustCore::RegisterResearcherEosb(void)
{
    __DebugFunction();

    bool fSuccess = false;

    try
    {
        StructuredBuffer oResponse(::RegisterVirtualMachineResearchUser(m_oRootOfTrustCoreProperties.GetProperty("ResearchUserEosb"), m_oRootOfTrustCoreProperties.GetProperty("VirtualMachineIdentifier")));
        m_oRootOfTrustCoreProperties.SetProperty("ResearchUserIdentifier", oResponse.GetString("ResearchUserIdentifier"));
        m_oRootOfTrustCoreProperties.SetProperty("ResearchOrganizationAuditEventParentBranchNodeIdentifier", oResponse.GetString("ResearchOrganizationAuditEventParentBranchNodeIdentifier"));
        fSuccess = true;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return fSuccess;
}

/********************************************************************************************/

void __thiscall RootOfTrustCore::RecordInternalAuditEvent(
    _in const char * c_szEventName,
    _in Word wTargetChannelsBitMask,
    _in Dword dwEventType,
    _in const StructuredBuffer & c_oEventData
    )
{
    __DebugFunction();

    try
    {
        Guid oEventGuid;
        StructuredBuffer oTransactionData;
        // Internal elements only. These will be deleted before to transmitting the audit event
        oTransactionData.PutGuid("DomainIdentifier", m_oRootOfTrustCoreProperties.GetProperty("RootOfTrustDomainIdentifier"));
        oTransactionData.PutDword("Transaction", 0x00000009);
        // Make sure that the encrypted data contains the EventName property
        oTransactionData.PutWord("TargetChannelsBitMask", wTargetChannelsBitMask);
        oTransactionData.PutQword("EventType", dwEventType);
        // Add the encrypted event data to the audit event
        oTransactionData.PutString("EventData", c_oEventData.GetBase64SerializedBuffer());
        // Send the transaction
        this->HandleAuditEventTransaction(oTransactionData);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
}