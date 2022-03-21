/*********************************************************************************************
 *
 * @file AuditEventManagedQueues.h
 * @author Luis Miguel Huapaya
 * @date 22 March 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "AuditEventManagedQueues.h"
#include "CompressionHelperFunctions.h"
#include "CoreTypes.h"
#include "DateAndTime.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"

/*********************************************************************************************/

AuditEventManagedQueues::AuditEventManagedQueues(void)
{
    __DebugFunction();

    m_unResearcherAuditEventSequenceNumber = 0;
    m_unDataOwnerAuditEventSequenceNumber = 0;
    m_unThirdPartyAuditorAuditEventSequenceNumber = 0;
    m_unSailAuditEventSequenceNumber = 0;
}

/*********************************************************************************************/

AuditEventManagedQueues::~AuditEventManagedQueues(void)
{
    __DebugFunction();
}

/*********************************************************************************************/

void __thiscall AuditEventManagedQueues::AddAuditEvent(
    _in const std::string & c_strEventName,
    _in Word wTargetChannelsBitMask,
    _in Dword dwEventType,
    _in const StructuredBuffer & c_oEventData
    )
{
    __DebugFunction();
    __DebugAssert(0 < c_strEventName.size());

    // We need to add some mandatory fields to the c_oEventData
    StructuredBuffer oAuditEvent;
    oAuditEvent.PutGuid("EventGuid", Guid(eAuditEvent_EncryptedLeafNode));
    oAuditEvent.PutUnsignedInt64("Timestamp", ::GetEpochTimeInMilliseconds());
    oAuditEvent.PutDword("EventType", dwEventType);
    oAuditEvent.PutString("EventName", c_strEventName);
    oAuditEvent.PutStructuredBuffer("EncryptedEventData", c_oEventData);
    // Now let's commit the audit event to one or more audit event queues based on the channels bit mask
    const std::lock_guard<std::mutex> lock(m_stlMutex);
    if (0x1000 == (0x1000 & wTargetChannelsBitMask)) // Third Party Auditor Channel
    {
        unsigned int unSequenceNumber = ::__sync_fetch_and_add((int *) &m_unThirdPartyAuditorAuditEventSequenceNumber, 1);
        oAuditEvent.PutUnsignedInt32("SequenceNumber", unSequenceNumber);
        m_stlIndependentAuditorOrganizationAuditEventQueue.push(oAuditEvent.GetBase64SerializedBuffer());
    }
    if (0x0100 == (0x0100 & wTargetChannelsBitMask)) // Data Organization Channel
    {
        unsigned int unSequenceNumber = ::__sync_fetch_and_add((int *) &m_unDataOwnerAuditEventSequenceNumber, 1);
        oAuditEvent.PutUnsignedInt32("SequenceNumber", unSequenceNumber);
        m_stlDataOrganizationAuditEventQueue.push(oAuditEvent.GetBase64SerializedBuffer());
    }
    if (0x0010 == (0x0010 & wTargetChannelsBitMask)) // Research Organization Channel
    {
        unsigned int unSequenceNumber = ::__sync_fetch_and_add((int *) &m_unResearcherAuditEventSequenceNumber, 1);
        oAuditEvent.PutUnsignedInt32("SequenceNumber", unSequenceNumber);
        m_stlResearchOrganizationAuditEventQueue.push(oAuditEvent.GetBase64SerializedBuffer());
    }
    if (0x0001 == (0x0001 & wTargetChannelsBitMask)) // Sail Organization Channel
    {
        unsigned int unSequenceNumber = ::__sync_fetch_and_add((int *) &m_unSailAuditEventSequenceNumber, 1);
        oAuditEvent.PutUnsignedInt32("SequenceNumber", unSequenceNumber);
        m_stlSailOrganizationAuditEventQueue.push(oAuditEvent.GetBase64SerializedBuffer());
    }
}

/*********************************************************************************************/

unsigned int AuditEventManagedQueues::GetQueuedAuditEventsCount(
    _in Word wTargetChannelsBitMask
    ) const throw()
{
    __DebugFunction();

    unsigned unAuditEventsCount = 0;

    try
    {
        const std::lock_guard<std::mutex> lock(m_stlMutex);
        if (0x1000 == (0x1000 & wTargetChannelsBitMask)) // Third Party Auditor Channel
        {
            unAuditEventsCount += m_stlIndependentAuditorOrganizationAuditEventQueue.size();
        }
        if (0x0100 == (0x0100 & wTargetChannelsBitMask)) // Data Organization Channel
        {
            unAuditEventsCount += m_stlDataOrganizationAuditEventQueue.size();
        }
        if (0x0010 == (0x0010 & wTargetChannelsBitMask)) // Research Organization Channel
        {
            unAuditEventsCount += m_stlResearchOrganizationAuditEventQueue.size();
        }
        if (0x0001 == (0x0001 & wTargetChannelsBitMask)) // Sail Organization Channel
        {
            unAuditEventsCount += m_stlSailOrganizationAuditEventQueue.size();
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return unAuditEventsCount;
}

/*********************************************************************************************/

std::queue<std::string> __thiscall AuditEventManagedQueues::GetQueuedAuditEvents(
    _in Word wTargetChannelBitMask
    ) throw()
{
    __DebugFunction();
    __DebugAssert((0x1000 == wTargetChannelBitMask)||(0x0100 == wTargetChannelBitMask)||(0x0010 == wTargetChannelBitMask)||(0x0001 == wTargetChannelBitMask));

    std::queue<std::string> strAuditEventQueue;

    try
    {
        const std::lock_guard<std::mutex> lock(m_stlMutex);
        if (0x1000 == wTargetChannelBitMask)  // Third Party Auditor Channel
        {
            std::swap(m_stlIndependentAuditorOrganizationAuditEventQueue, strAuditEventQueue);
            __DebugAssert(true == m_stlIndependentAuditorOrganizationAuditEventQueue.empty());
        }
        else if (0x1000 == wTargetChannelBitMask)    // Data Organization Channel
        {
            std::swap(m_stlDataOrganizationAuditEventQueue, strAuditEventQueue);
            __DebugAssert(true == m_stlDataOrganizationAuditEventQueue.empty());
        }
        else if (0x1000 == wTargetChannelBitMask)    // Research Organization Channel
        {
            std::swap(m_stlResearchOrganizationAuditEventQueue, strAuditEventQueue);
            __DebugAssert(true == m_stlResearchOrganizationAuditEventQueue.empty());
        }
        else if (0x1000 == wTargetChannelBitMask)    // Sail Organization Channel
        {
            std::swap(m_stlSailOrganizationAuditEventQueue, strAuditEventQueue);
            __DebugAssert(true == m_stlSailOrganizationAuditEventQueue.empty());
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return strAuditEventQueue;
}