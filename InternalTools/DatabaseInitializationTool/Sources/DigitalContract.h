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
#include "Organization.h"
#include "StructuredBuffer.h"

#include <string>
#include <unordered_map>

class DigitalContract : public Object
{
    public:
    
        DigitalContract(
            _in const Organization * c_poDataOwnerOrganization,
            _in const Organization * c_poResearchOrganization,
            _in const StructuredBuffer & c_oDigitalContractParameters
            );
        virtual ~DigitalContract(void);
        
        // Register() registers all digital contracts across all organizations
        bool __thiscall Register(
            _in const std::string & c_strSailPlatformServicesIpAddress,
            _in Word wSailPlatformServicesPortNumber
            ) throw();
        
        std::string __thiscall GetContractName(void) const throw();
        
    private:
    
        // Private data members
        std::string m_strDataOwnerAdministratorUsername;
        std::string m_strResearchAdministratorUsername;
        std::string m_strDataOwnerOrganizationIdentifier;
        std::string m_strResearchOrganizationIdentifier;
        std::string m_strTitle;
        std::string m_strDescription;
        std::string m_strAssociatedIdentifier;
        std::string m_strVersionNumber;
        std::string m_strLegalAgreement;
        unsigned int m_unSubscriptionDays;
        unsigned int m_unRetentionTime;
        std::string m_strHostForVirtualMachines;
        std::string m_strHostRegion;
        unsigned int m_unNumberOfVirtualMachines;
};
