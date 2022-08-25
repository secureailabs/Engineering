/*********************************************************************************************
 *
 * @file DataFederation.cpp
 * @author David Gascon
 * @date 14 Mar 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/
#include <algorithm>
#include <iostream>
#include <DataFederation.h>
#include <StructuredBufferHelperFunctions.h>
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"

/********************************************************************************************
 *
 * @class DataFederation
 * @function DataFederation
 * @brief Constructor
 * @param[in] oIdentifier the identifier for the federation
 * @param[in] oOrganizationOwnerIdentifier the identifier for the organziation that owns this
 *            federation
 * @param[in] strName the name of the federation
 * @param[in] strDescription the description of the federation
 *
 ********************************************************************************************/
DataFederation::DataFederation(
    _in const Guid & oIdentifier,
    _in const Guid & oOrganizationOwnerIdentifier,
    _in const std::string & strName,
    _in const std::string & strDescription
    ) :
    m_fActive{true},
    m_oIdentifier{oIdentifier},
    m_oOrganizationOwnerIdentifier{oOrganizationOwnerIdentifier},
    m_strName{strName},
    m_strDescription{strDescription}
{
    __DebugFunction();

    _ThrowBaseExceptionIf(eDataFederation != m_oIdentifier.GetObjectType(), "Invalid Identifier type", nullptr);
    _ThrowBaseExceptionIf(eOrganization != m_oOrganizationOwnerIdentifier.GetObjectType(), "Invalid Organization Identifier type", nullptr);
}

/********************************************************************************************
 *
 * @class DataFederation
 * @function DataFederation
 * @brief Constructor from StructuredBuffer
 * @param[in] c_oSourceBuffer - The structured buffer to build the object from
 *
 ********************************************************************************************/
DataFederation::DataFederation(
    _in const StructuredBuffer & c_oSourceBuffer
    ):
    m_fActive{c_oSourceBuffer.GetBoolean("DataFederationActive")},
    m_oIdentifier{c_oSourceBuffer.GetGuid("DataFederationIdentifier")},
    m_oOrganizationOwnerIdentifier{c_oSourceBuffer.GetGuid("DataFederationOwnerOrganizationIdentifier")},
    m_strName{c_oSourceBuffer.GetString("DataFederationName")},
    m_strDescription{c_oSourceBuffer.GetString("DataFederationDescription")}
{
    __DebugFunction();

    // Fill in data submitter list
    std::for_each(c_oSourceBuffer.GetStructuredBuffer("DataFederationDataSubmitterList").GetNamesOfElements().begin(),
        c_oSourceBuffer.GetStructuredBuffer("DataFederationDataSubmitterList").GetNamesOfElements().begin(),
        [&](auto oEntry)
        {
            m_stlDataSubmitterOrganizations.push_back(c_oSourceBuffer.GetStructuredBuffer("DataFederationDataSubmitterList").GetGuid(oEntry.c_str()));
        }
    );
    // Fill in researcher list
    std::for_each(c_oSourceBuffer.GetStructuredBuffer("DataFederationResearcherList").GetNamesOfElements().begin(),
        c_oSourceBuffer.GetStructuredBuffer("DataFederationResearcherList").GetNamesOfElements().begin(),
        [&](auto oEntry)
        {
            m_stlResearchOrganizations.push_back(c_oSourceBuffer.GetStructuredBuffer("DataFederationResearcherList").GetGuid(oEntry.c_str()));
        }
    );
    // Fill in dataset families
    std::for_each(c_oSourceBuffer.GetStructuredBuffer("DataFederationDatasetList").GetNamesOfElements().begin(),
        c_oSourceBuffer.GetStructuredBuffer("DataFederationDatasetList").GetNamesOfElements().begin(),
        [&](auto oEntry)
        {
            m_stlDatasets.push_back(c_oSourceBuffer.GetStructuredBuffer("DataFederationDatasetList").GetGuid(oEntry.c_str()));
        }
    );

}

/********************************************************************************************
 *
 * @class DataFederation
 * @function ~DataFederation
 * @brief Destructor
 *
 ********************************************************************************************/
DataFederation::~DataFederation()
{
    __DebugFunction();
}

/********************************************************************************************
 *
 * @class DatasetManager
 * @function ToStructuredBuffer
 * @brief Convert this object to a StructuredBuffer
 * @return A StructuredBuffer representing this object
 *
 ********************************************************************************************/
StructuredBuffer __thiscall DataFederation::ToStructuredBuffer(void) const
{
    __DebugFunction();

    StructuredBuffer oDataFederationStructuredBuffer;

    oDataFederationStructuredBuffer.PutGuid("DataFederationIdentifier", this->m_oIdentifier);
    oDataFederationStructuredBuffer.PutGuid("DataFederationOwnerOrganizationIdentifier", this->m_oOrganizationOwnerIdentifier);
    oDataFederationStructuredBuffer.PutString("DataFederationName", this->m_strName);
    oDataFederationStructuredBuffer.PutString("DataFederationDescription", this->m_strDescription);
    oDataFederationStructuredBuffer.PutBoolean("DataFederationActive", this->m_fActive);


    StructuredBuffer oDataFederationDataSubmitterList = ::ConvertIdentifierListToStructuredBuffer(this->m_stlDataSubmitterOrganizations);
    StructuredBuffer oDataFederationResearcherList = ::ConvertIdentifierListToStructuredBuffer(this->m_stlResearchOrganizations);
    StructuredBuffer oDataFederationDatasets = ::ConvertIdentifierListToStructuredBuffer(this->m_stlDatasets);

    oDataFederationStructuredBuffer.PutStructuredBuffer("DataFederationDataSubmitterList", oDataFederationDataSubmitterList);
    oDataFederationStructuredBuffer.PutStructuredBuffer("DataFederationResearcherList", oDataFederationResearcherList);
    oDataFederationStructuredBuffer.PutStructuredBuffer("DataFederationDatasetList", oDataFederationDatasets);
    oDataFederationStructuredBuffer.PutString("VersionNumber", "0x00000001");

    return oDataFederationStructuredBuffer;
}

/********************************************************************************************
 *
 * @class DataFederation
 * @function IsOrganizationInFederation
 * @brief Determine if the given organization identifer particpates in this federation
 * @param[in] c_oOrganizationIdentifier The identifier for the organization to check
 * @returns bool, true if the organization is in the federation, false otherwise
 *
 ********************************************************************************************/
bool DataFederation::IsOrganizationInFederation(
    _in const Guid & c_oOrganizationIdentifier
    ) const throw()
{
    __DebugFunction();

    bool fIsInFederation{ m_oOrganizationOwnerIdentifier == c_oOrganizationIdentifier};
    if ( false == fIsInFederation )
    {
        fIsInFederation = std::any_of(m_stlDataSubmitterOrganizations.begin(), m_stlDataSubmitterOrganizations.end(),[&c_oOrganizationIdentifier] (auto oSubmitterIdentifier) 
        {
            return (oSubmitterIdentifier == c_oOrganizationIdentifier);
        });
    }
    if ( false == fIsInFederation )
    {
        fIsInFederation = std::any_of(m_stlResearchOrganizations.begin(), m_stlResearchOrganizations.end(),[&c_oOrganizationIdentifier] (auto oResearcherIdentifier) 
        {
            return (oResearcherIdentifier == c_oOrganizationIdentifier);
        });
    }
    return fIsInFederation;
}

/********************************************************************************************
 *
 * @class DataFederation
 * @function IsActive
 * @brief Determine if this federation is active
 * @returns bool stating whether the federation is active
 *
 ********************************************************************************************/
bool DataFederation::IsActive() const throw()
{
    __DebugFunction();

    return m_fActive;
}

/********************************************************************************************
 *
 * @class DataFederation
 * @function Name
 * @brief Get the data federation name
 * @returns std::string of the data federation name
 *
 ********************************************************************************************/
std::string DataFederation::Name() const throw()
{
    __DebugFunction();

    return m_strName;
}

/********************************************************************************************
 *
 * @class DataFederation
 * @function Description
 * @brief Get the data federation Description
 * @returns std::string of the data federation Description
 *
 ********************************************************************************************/
std::string DataFederation::Description() const throw()
{
    __DebugFunction();

    return m_strDescription;
}

/********************************************************************************************
 *
 * @class DataFederation
 * @function Identifier
 * @brief Get the data federation Identifier
 * @returns Guid of the data federation Identifier
 *
 ********************************************************************************************/
Guid DataFederation::Identifier() const throw()
{
    __DebugFunction();

    return m_oIdentifier;
}

/********************************************************************************************
 *
 * @class DataFederation
 * @function OrganizationOwnerIdentifier
 * @brief Get the data federation Organization Owner Identifier
 * @returns Guid of the data federation Organization Owner Identifier
 *
 ********************************************************************************************/
Guid DataFederation::OrganizationOwnerIdentifier() const throw()
{
    __DebugFunction();

    return m_oOrganizationOwnerIdentifier;
}

/********************************************************************************************
 *
 * @class DataFederation
 * @function DataSubmitterOrganizations
 * @brief Get the list of organizations registered to submit data to this federation
 * @returns std::list<Guid> of organizations registered to submit data to this federation
 *
 ********************************************************************************************/
std::list<Guid> DataFederation::DataSubmitterOrganizations() const throw()
{
    __DebugFunction();

    return m_stlDataSubmitterOrganizations;
}

/********************************************************************************************
 *
 * @class DataFederation
 * @function ResearchOrganizations
 * @brief Get the list of organizations registered to research in this federation
 * @returns std::list<Guid> of organizations registered to research in this federation
 *
 ********************************************************************************************/
std::list<Guid> DataFederation::ResearchOrganizations() const throw()
{
    __DebugFunction();

    return m_stlResearchOrganizations;
}

/********************************************************************************************
 *
 * @class DataFederation
 * @function Datasets
 * @brief Get the list of datset families in this federation
 * @returns std::list<Guid> of dataset families in this federation
 *
 ********************************************************************************************/
std::list<Guid> DataFederation::Datasets() const throw()
{
    __DebugFunction();

    return m_stlDatasets;
}

/********************************************************************************************
 *
 * @class DataFederation
 * @function SetInactive
 * @brief Set this federation to be inactive
 *
 ********************************************************************************************/
void DataFederation::SetInactive() throw()
{
    __DebugFunction()

    m_fActive = false;
}
