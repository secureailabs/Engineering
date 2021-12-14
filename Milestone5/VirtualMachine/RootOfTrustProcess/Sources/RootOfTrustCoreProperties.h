/*********************************************************************************************
 *
 * @file RootOfTrustCoreProperties.h
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "AuditEventManagedQueues.h"
#include "64BitHashes.h"
#include "CoreTypes.h"
#include "Object.h"
#include "RootOfTrustCoreProperties.h"
#include "Socket.h"
#include "SmartMemoryAllocator.h"
#include "StructuredBuffer.h"
#include "ThreadManager.h"

#include <string>
#include <map>
#include <mutex>

class RootOfTrustCoreProperties : public Object
{
    public:

        RootOfTrustCoreProperties(void);
        virtual ~RootOfTrustCoreProperties(void);

        std::string __thiscall GetProperty(
            _in const char * c_szPropertyName
            ) const throw();
        void __thiscall SetProperty(
            _in const char * c_szPropertyName,
            _in const std::string & c_szPropertyValue
            ) throw();

    private:

        mutable std::mutex m_stlMutex;
        std::map<Qword, std::string> m_stlProperties;
};