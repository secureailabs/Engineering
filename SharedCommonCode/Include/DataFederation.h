/*********************************************************************************************
 *
 * @file DataFederation.h
 * @author David Gascon
 * @date 14 Mar 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/
#pragma once

#include <list>
#include <string>
#include <Guid.h>
#include <StructuredBuffer.h>

class DataFederation
{
    public:
        explicit DataFederation(
            _in const Guid & oIdentifier,
            _in const Guid & oOrganizationOwnerIdentifier,
            _in const std::string & strName,
            _in const std::string & strDescription
            );

        explicit DataFederation(
            _in const StructuredBuffer & c_oSourceBuffer
            );

        // Don't allow default construction
        DataFederation() = delete;

        virtual ~DataFederation();

        // Convert this object to a structured buffer
        StructuredBuffer ToStructuredBuffer(void) const;

        // Determine if an organization is participating in this federation
        bool IsOrganizationInFederation(
            _in const Guid & 
            ) const throw();

        bool IsActive() const throw();

        std::string Name() const throw();
        std::string Description() const throw();

        Guid Identifier() const throw();
        Guid OrganizationOwnerIdentifier() const throw();

        std::list<Guid> DataSubmitterOrganizations() const throw();
        std::list<Guid> ResearchOrganizations() const throw();
        std::list<Guid> DatasetFamilies() const throw();
    private:
        // Data members
        bool m_fActive;

        Guid m_oIdentifier;
        Guid m_oOrganizationOwnerIdentifier;

        std::string m_strName;
        std::string m_strDescription;

        std::list<Guid> m_stlDataSubmitterOrganizations;
        std::list<Guid> m_stlResearchOrganizations;
        std::list<Guid> m_stlDataFamilies;
};