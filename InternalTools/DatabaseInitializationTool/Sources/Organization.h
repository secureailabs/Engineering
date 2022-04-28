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
#include "SailPlatformServicesSession.h"
#include "StructuredBuffer.h"

#include <string>
#include <unordered_set>
#include <unordered_map>

class Organization : public Object
{
    public:
    
        Organization(
            _in const std::string & c_strOrganizationName,
            _in const StructuredBuffer & c_oOrganizationalData
            );
        virtual ~Organization(void);
        
        // Register() registers all aspects of an organization
        bool __thiscall Register(
            _in const std::string & c_strSailPlatformServicesIpAddress,
            _in Word wSailPlatformServicesPortNumber,
            _in unsigned int unStepIdentifier
            ) throw();

        // The following information is needed when trying to register
        // digital contracts. So once an organization is registered, these
        // methods can be used to keep track of data that will be
        // needed to register digital contracts related to organizations
        std::string __thiscall GetOrganizationalName(void) const throw();
        std::string __thiscall GetOrganizationalIdentifier(void) const throw();
        // Method which return the name of the first admin user associated with
        // this organization
        std::string __thiscall GetAdminUsername(void) const throw();
        // Method which returns the identifier of a dataset based on it'sb_type
        // name. This is required in order to help register digital contracts
        std::string __thiscall GetDatasetIdentifier(
            _in const std::string & c_strDatasetName
            ) const throw();
        // Method which returns the identifier of a dataset family based on it'sb_type
        // name. This is required in order to help register digital contracts
        std::string __thiscall GetDatasetFamilyIdentifier(
            _in const std::string & c_strDatasetFamilyName
            ) const throw();
        // Method which returns the identifier of a data federation based on it'sb_type
        // name. This is required in order to help register digital contracts
        std::string __thiscall GetDataFederationIdentifier(
            _in const std::string & c_strDataFederationName
            ) const throw();
        
        
    private:
    
        // Since all of the functions to register have the same login code in
        // common, we made a function for it
        void __thiscall Login(
            _inout SailPlatformServicesSession & oSailPlatformServicesSession
            ) const;
        // This registers both the organization and the original admin user.
        void __thiscall RegisterOrganization(void);
        // This registers any administrators above and beyond the 1st admin
        void __thiscall RegisterAdministrators(void);
        // Registers contacts associated with the organization. Contacts are not1
        // users (and don't need to be users). This is for SAIL purposes
        void __thiscall RegisterContacts(void);
        // Register non-admin users
        void __thiscall RegisterUsers(void);
        void __thiscall RegisterDataFederations(void);
        void __thiscall RegisterDatasetFamilies(void);
        void __thiscall RegisterDatasets(void);
        
        // Private data members
        std::string m_strSailPlatformServicesIpAddress;
        Word m_wSailPlatformServicesPortNumber;
        bool m_fRegistered;
        std::string m_strOrganizationalName;
        std::string m_strOrganizationalAddress;
        std::unordered_set<std::string> m_stlContacts;
        std::unordered_set<std::string> m_stlAdministrators;
        std::unordered_set<std::string> m_stlUsers;
        std::unordered_map<Qword, std::string> m_strDatasetFilenames;
        std::unordered_set<std::string> m_stlDatasetFamilies;
        std::unordered_map<Qword, std::string> m_strDatasetFamilyIdentifiers;
        std::unordered_set<std::string> m_stlDataFederations;
        std::unordered_map<Qword, std::string> m_strDataFederationIdentifiers;
};