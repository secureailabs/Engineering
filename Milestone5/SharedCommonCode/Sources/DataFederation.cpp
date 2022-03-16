/*********************************************************************************************
 *
 * @file DataFederation.cpp
 * @author David Gascon
 * @date 14 Mar 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/
#include <DataFederation.h>
#include <StructuredBufferHelperFunctions.h>
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
    m_oIdentifier{oIdentifier},
    m_oOrganizationOwnerIdentifier{oOrganizationOwnerIdentifier},
    m_strName{strName},
    m_strDescription{strDescription},
    m_fActive{true}
{
    _ThrowBaseExceptionIf(eDataFederation != m_oIdentifier.GetObjectType(), "Invalid Identifier type", nullptr);
    _ThrowBaseExceptionIf(eOrganization != m_oOrganizationOwnerIdentifier.GetObjectType(), "Invalid Organization Identifier type", nullptr);
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

}

/********************************************************************************************
 *
 * @class DatasetFamilyManager
 * @function ToStructuredBuffer
 * @brief Convert this object to a StructuredBuffer
 * @return A StructuredBuffer representing this object
 *
 ********************************************************************************************/
StructuredBuffer __thiscall DataFederation::ToStructuredBuffer(void) const
{
    StructuredBuffer oDataFederationStructuredBuffer;

    oDataFederationStructuredBuffer.PutGuid("DataFederationIdentifier", this->m_oIdentifier);
    oDataFederationStructuredBuffer.PutGuid("DataFederationOwnerOrganizationIdentifier", this->m_oOrganizationOwnerIdentifier);
    oDataFederationStructuredBuffer.PutString("DataFederationName", this->m_strName);
    oDataFederationStructuredBuffer.PutString("DataFederationDescription", this->m_strDescription);
    oDataFederationStructuredBuffer.PutBoolean("DataFederationActive", this->m_fActive);


    StructuredBuffer oDataFederationDataSubmitterList = ConvertIdentifierListToStructuredBuffer(this->m_stlDataSubmitterOrganizations);
    StructuredBuffer oDataFederationResearcherList = ConvertIdentifierListToStructuredBuffer(this->m_stlResearchOrganizations);
    StructuredBuffer oDataFederationDatasetFamilies = ConvertIdentifierListToStructuredBuffer(this->m_stlDataFamilies);

    oDataFederationStructuredBuffer.PutStructuredBuffer("DataFederationDataSubmitterList", oDataFederationDataSubmitterList);
    oDataFederationStructuredBuffer.PutStructuredBuffer("DataFederationResearcherList", oDataFederationResearcherList);
    oDataFederationStructuredBuffer.PutStructuredBuffer("DataFederationDatasetFamilyList", oDataFederationDatasetFamilies);
    oDataFederationStructuredBuffer.PutString("VersionNumber", "0x00000001");

    return oDataFederationStructuredBuffer;
}
