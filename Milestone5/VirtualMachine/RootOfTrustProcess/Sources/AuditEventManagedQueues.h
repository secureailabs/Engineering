/*********************************************************************************************
 *
 * @file AuditEventManagedQueues.h
 * @author Luis Miguel Huapaya
 * @date 22 March 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

 #pragma once

 #include "CoreTypes.h"
 #include "Object.h"
 #include "StructuredBuffer.h"

 #include <mutex>
 #include <queue>
 #include <string>

 class AuditEventManagedQueues : public Object
 {
    public:

        AuditEventManagedQueues(void);
        virtual ~AuditEventManagedQueues(void);

        void __thiscall AddAuditEvent(
            _in const std::string & c_strEventName,
            _in Word wTargetChannelsBitMask,
            _in Dword dwEventType,
            _in const StructuredBuffer & c_oEventData
            );
        unsigned int __thiscall GetQueuedAuditEventsCount(
            _in Word wTargetChannelBitMask
            ) const throw();
        std::queue<std::string> __thiscall GetQueuedAuditEvents(
            _in Word wTargetChannelBitMask
            ) throw();

    private:

        mutable std::mutex m_stlMutex;
        unsigned int m_unResearcherAuditEventSequenceNumber;
        unsigned int m_unDataOwnerAuditEventSequenceNumber;
        unsigned int m_unThirdPartyAuditorAuditEventSequenceNumber;
        unsigned int m_unSailAuditEventSequenceNumber;
        std::queue<std::string> m_stlResearchOrganizationAuditEventQueue;
        std::queue<std::string> m_stlDataOrganizationAuditEventQueue;
        std::queue<std::string> m_stlIndependentAuditorOrganizationAuditEventQueue;
        std::queue<std::string> m_stlSailOrganizationAuditEventQueue;
 };