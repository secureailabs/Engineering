/*********************************************************************************************
 *
 * @file DigitalContract.h
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

class DigitalContract : public Object
{
    public:
    
        DigitalContract(
            _in const StructuredBuffer & c_oOrganizationData
            );
        virtual ~DigitalContract(void);
        
        bool __thiscall Register(
            _in const std::string c_strSailPlatformServicesIpAddress
            ) const;
        
    private:
    
        std::string m_strSailPlatformServicesIpAddress
};