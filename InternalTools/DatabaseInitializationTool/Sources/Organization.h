/*********************************************************************************************
 *
 * @file Organization.h
 * @author Luis Miguel Huapaya
 * @date 23 March 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "Object.h"
#include "StructuredBuffer.h"

#include <unordered_set>

class Organization : public Object
{
    public:
    
        Organization(
            _in const StructuredBuffer & c_oOrganizationData
            );
        virtual ~Organization(void);
        
        bool __thiscall Register(
            _in const std::string c_strSailPlatformServicesIpAddress
            ) const;
        
    private:
    
        bool __thiscall RegisterOrganization(void) const;
        bool __thiscall RegisterUsers(void) const;
        bool __thiscall RegisterDatasets(void) const;
        
        std::string m_strSailPlatformServicesIpAddress
        std::string m_strName;
        std::string m_strAddress;
        std::unordered_set<StructuredBuffer> m_strAdministrators;
        std::unordered_set<StructuredBuffer> m_strContacts;
        std::unordered_set<StructuredBuffer> m_strUsers;
        std::unordered_set<std::string> m_strDatasets;
};