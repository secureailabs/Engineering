/*********************************************************************************************
 *
 * @file DemoDatabase.cpp
 * @author Prawal Gangwar
 * @date 24 Feburary 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "DemoDatabase.h"
#include "Base64Encoder.h"
#include "InitializationVector.h"

/********************************************************************************************/

DemoDatabase::DemoDatabase(
    _in const char * c_szIpAddress,
    _in unsigned int unPortNumber
    )
{
    __DebugFunction();

    // initialize web portal ip address and port number
    ::AddWebPortalConfiguration(c_szIpAddress, unPortNumber);
    // initialize accounts
    this->InitializeMembers();
}

/********************************************************************************************/

DemoDatabase::~DemoDatabase(void)
{
    __DebugFunction();

}

/********************************************************************************************/

void __thiscall DemoDatabase::InitializeMembers(void)
{
    __DebugFunction();

    // Add Organizations information
    m_stlOrganizations.push_back(OrganizationInformation{"International Genetics Research Facility", "New York City", "Lily Bart", "System Administrator", "lbart@igr.com", "000-000-0000", "Philip Carey", "Network Engineer", "pcarey@igr.com", "000-000-0000"});
    m_stlOrganizations.push_back(OrganizationInformation{"Mercy General Hospital", "Los Angeles", "Nick Adams", "System Administrator", "nadams@mghl.com", "000-000-0000", "Nora Helmer", "Network Engineer", "nhelmer@mghl.com", "000-000-0000"});
    m_stlOrganizations.push_back(OrganizationInformation{"Kidney Cancer Association", "San Francisco", "Isabel Archer", "System Administrator", "iarcher@kca.com", "000-000-0000", "Sally Bowles", "Network Engineer", "sbowles@kca.com", "000-000-0000"});
    m_stlOrganizations.push_back(OrganizationInformation{"Cancer Research Hospital", "Seattle", "Anna Christie", "System Administrator", "achristie@crh.com", "000-000-0000", "Nick Carter", "Network Engineer", "ncarter@crh.com", "000-000-0000"});

    // Add super admins information
    m_stlAdmins.push_back(UserInformation{"lbart@igr.com", "Lily Bart", "System Administrator", "000-000-0000", eAdmin});
    m_stlAdmins.push_back(UserInformation{"nadams@mghl.com", "Nick Adams", "System Administrator", "000-000-0000", eAdmin});
    m_stlAdmins.push_back(UserInformation{"iarcher@kca.com", "Isabel Archer", "System Administrator", "000-000-0000", eAdmin});
    m_stlAdmins.push_back(UserInformation{"achristie@crh.com", "Anna Christie", "System Administrator", "000-000-0000", eAdmin});

    // Add datasets information
    m_stlDatasets.push_back(DatasetInformation(Guid(eDataset).ToString(eHyphensAndCurlyBraces), "0x00000001", "KCA Consortium Data - MGH", "Patient data derived from internal kidney cancer patient registry.  Covers patients admitted 1995 to present. Conforms to KCA Consortium Data Model ver 1.0", "kidney renal cancer KCAC_v1.0", GetEpochTimeInSeconds(), 1, "N/A"));
    m_stlDatasets.push_back(DatasetInformation(Guid(eDataset).ToString(eHyphensAndCurlyBraces), "0x00000001", "KCA Consortium Data - KCA", "Patient data from the KCA patient arm.  Covers patients registered from May, 2021 to present. Historical longitudinal data may go back several years. Conforms to KCA Consortium Data Model ver 1.0", "kidney renal cancer KCAC_v1.0", GetEpochTimeInSeconds(), 1, "N/A"));
    m_stlDatasets.push_back(DatasetInformation(Guid(eDataset).ToString(eHyphensAndCurlyBraces), "0x00000001", "KCA Consortium Data - CRH", "Patient data derived from internal kidney cancer patient registry.  Covers patient data collected from 1980 to present. Conforms to KCA Consortium Data Model ver 1.0", "kidney renal cancer KCAC_v1.0", GetEpochTimeInSeconds(), 1, "N/A"));

    // Add digital contracts information
    std::string strLegalAgreement = "The Parties acknowledge and agree that this Agreement represents the entire agreement between the Parties. "
                                    "In the event that the Parties desire to change, add, or otherwise modify any terms, they shall do so in writing to be signed by both parties.";
    std::string strDescription = "The dataset will be used to train models for academic research purposes.";
    m_stlDigitalContracts.push_back(DigitalContractInformation{"KCA Consortium - MGH", 90, strLegalAgreement, 16186603, strDescription, "SAIL", 1, "East US"});
    m_stlDigitalContracts.push_back(DigitalContractInformation{"KCA Consortium - KCA", 90, strLegalAgreement, 24117352, strDescription, "SAIL", 1, "East US"});
    m_stlDigitalContracts.push_back(DigitalContractInformation{"KCA Consortium - CRH", 90, strLegalAgreement, 60768913, strDescription, "SAIL", 1, "East US"});
}

/********************************************************************************************/

void __thiscall DemoDatabase::AddOrganizationsAndSuperAdmins(void)
{
    __DebugFunction();

    // Register organizations and super admins
    for (unsigned int unIndex = 0; unIndex < m_stlOrganizations.size(); ++unIndex)
    {
        StructuredBuffer oOrganizationInformation;
        oOrganizationInformation.PutString("Email", m_stlAdmins.at(unIndex).m_strEmail);
        oOrganizationInformation.PutString("Password", m_strPassword);
        oOrganizationInformation.PutString("Name", m_stlAdmins.at(unIndex).m_strName);
        oOrganizationInformation.PutString("PhoneNumber", m_stlAdmins.at(unIndex).m_strPhoneNumber);
        oOrganizationInformation.PutString("Title", m_stlAdmins.at(unIndex).m_strTitle);
        oOrganizationInformation.PutString("OrganizationName", m_stlOrganizations.at(unIndex).m_strOrganizationName);
        oOrganizationInformation.PutString("OrganizationAddress", m_stlOrganizations.at(unIndex).m_strOrganizationAddress);
        oOrganizationInformation.PutString("PrimaryContactName", m_stlOrganizations.at(unIndex).m_strPrimaryContactName);
        oOrganizationInformation.PutString("PrimaryContactTitle", m_stlOrganizations.at(unIndex).m_strPrimaryContactTitle);
        oOrganizationInformation.PutString("PrimaryContactEmail", m_stlOrganizations.at(unIndex).m_strPrimaryContactEmail);
        oOrganizationInformation.PutString("PrimaryContactPhoneNumber", m_stlOrganizations.at(unIndex).m_strPrimaryContactPhoneNumber);
        oOrganizationInformation.PutString("SecondaryContactName", m_stlOrganizations.at(unIndex).m_strSecondaryContactName);
        oOrganizationInformation.PutString("SecondaryContactTitle", m_stlOrganizations.at(unIndex).m_strSecondaryContactTitle);
        oOrganizationInformation.PutString("SecondaryContactEmail", m_stlOrganizations.at(unIndex).m_strSecondaryContactEmail);
        oOrganizationInformation.PutString("SecondaryContactPhoneNumber", m_stlOrganizations.at(unIndex).m_strSecondaryContactPhoneNumber);
        // Add organizations and their super admins to the database
        bool fSuccess = ::RegisterOrganizationAndSuperUser(oOrganizationInformation);
        _ThrowBaseExceptionIf((false == fSuccess), "Error registering organization and its super admin.", nullptr);
    }

    std::cout << "Organizations and their admins added successfully." << std::endl;
}

/********************************************************************************************/

void __thiscall DemoDatabase::AddDatasets(void)
{
    __DebugFunction();

    // Register five datasets for the data owner organizations
    // The dataset guids will later be used in the digital contracts
    for (unsigned int unIndex = 0; unIndex < m_stlDatasets.size(); ++unIndex)
    {
        // Login to the web services as one of the users from the data owner organization
        // unIndex + 1 because the first user is the resaercher
        std::string strEncodedEosb = Login(m_stlAdmins.at(unIndex+1).m_strEmail, m_strPassword);
        _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);

        // Get organization guid from eosb
        StructuredBuffer oUserInformation(::GetBasicUserInformation(strEncodedEosb));
        std::string strOrganizationGuid = oUserInformation.GetString("OrganizationGuid");
        // Add organization guid to the organization structure
        m_stlOrganizations.at(unIndex+1).m_strOrganizationGuid = strOrganizationGuid;

        StructuredBuffer oPacket;
        oPacket.PutString("DatasetGuid", m_stlDatasets.at(unIndex).m_strDatasetGuid);

        StructuredBuffer oDsetInformation;
        oDsetInformation.PutString("VersionNumber", m_stlDatasets.at(unIndex).m_strVersionNumber);
        oDsetInformation.PutString("DatasetName", m_stlDatasets.at(unIndex).m_strName);
        oDsetInformation.PutString("Description", m_stlDatasets.at(unIndex).m_strDescription);
        oDsetInformation.PutString("Keywords", m_stlDatasets.at(unIndex).m_strKeywords);
        oDsetInformation.PutUnsignedInt64("PublishDate", m_stlDatasets.at(unIndex).m_un64PublishTime);
        oDsetInformation.PutByte("PrivacyLevel", m_stlDatasets.at(unIndex).m_bPrivacyLevel);
        oDsetInformation.PutString("JurisdictionalLimitations", m_stlDatasets.at(unIndex).m_strLimitations);
        StructuredBuffer oTables;

        // TODO: Prawal Add correct data
        StructuredBuffer oSingleTable;
        oSingleTable.PutString("ColumnName", ",AGE,BMI,PD-L1 level before treatment,PD-L1 level after treatment,PD-L2 level before treatment,PD-L2 level after treatment,PD1 level before treatment,PD1 level after treatment,");
        oSingleTable.PutString("Description", "table 1_2");
        oSingleTable.PutString("Hashtags", "t1h2");
        oSingleTable.PutString("Name", "1_2.csv");
        oSingleTable.PutDword("NumberColumns", 9);
        oSingleTable.PutDword("NumberRows", 30);
        oTables.PutStructuredBuffer("52d7aa80-f18f-4932-af61-ecf6fd74c064", oSingleTable);
        oDsetInformation.PutStructuredBuffer("Tables", oTables);
        oPacket.PutStructuredBuffer("DatasetData", oDsetInformation);
        // Register dataset
        ::RegisterDataset(strEncodedEosb, oPacket);
    }

    std::cout << "Datasets added successfully." << std::endl;
}

/********************************************************************************************/

void __thiscall DemoDatabase::AddDigitalContracts(void)
{
    __DebugFunction();

    // First organization is the researcher organization and second organization is the data owner organization
    unsigned int unRoIndex = 0;

    // Login to the web services
    std::string strEncodedEosb = Login(m_stlAdmins.at(unRoIndex).m_strEmail, m_strPassword);
    _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);

    // Get organization guid from eosb
    StructuredBuffer oUserInformation(::GetBasicUserInformation(strEncodedEosb));
    std::string strOrganizationGuid = oUserInformation.GetString("OrganizationGuid");
    // Add organization guid to the organization structure
    m_stlOrganizations.at(unRoIndex).m_strOrganizationGuid = strOrganizationGuid;

    // Get organization guids for the organizations
    std::string strRoGuid = m_stlOrganizations.at(unRoIndex).m_strOrganizationGuid;

    // Register five digital contracts for the organizations
    for (unsigned int unIndex = 0; unIndex < m_stlDigitalContracts.size(); ++unIndex)
    {
        // Add digital contract information
        std::string strDooGuid = m_stlOrganizations.at(unIndex+1).m_strOrganizationGuid;
        StructuredBuffer oDcInformation;
        oDcInformation.PutString("DOOGuid", strDooGuid);

        oDcInformation.PutString("Title", m_stlDigitalContracts.at(unIndex).m_strTitle);
        oDcInformation.PutUnsignedInt64("SubscriptionDays", m_stlDigitalContracts.at(unIndex).m_unSubscriptionDays);
        oDcInformation.PutString("LegalAgreement", m_stlDigitalContracts.at(unIndex).m_strLegalAgreement);
        oDcInformation.PutString("Description", m_stlDigitalContracts.at(unIndex).m_strDescription);
        oDcInformation.PutString("DatasetGuid", m_stlDatasets.at(unIndex).m_strDatasetGuid);

        // Register digital contract
        ::RegisterDigitalContract(strEncodedEosb, oDcInformation);
    }

    std::cout << "Digital contracts added successfully." << std::endl;
}

/********************************************************************************************/

void __thiscall DemoDatabase::AcceptDigitalContracts(void)
{
    __DebugFunction();

    for (unsigned int unIndex = 0; unIndex < m_stlDigitalContracts.size(); ++unIndex)
    {
        // Login to the web services as the data owner's dataset admin
        // As the Rest API requires dataset admin privileges
        std::string strEncodedEosb = Login(m_stlAdmins.at(unIndex + 1).m_strEmail, m_strPassword);
        _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);

        // Get organization guid from eosb
        StructuredBuffer oUserInformation(::GetBasicUserInformation(strEncodedEosb));
        std::string strOrganizationGuid = oUserInformation.GetString("OrganizationGuid");
        // Add organization guid to the organization structure
        m_stlOrganizations.at(unIndex + 1).m_strOrganizationGuid = strOrganizationGuid;

        // Get list of all digital contracts for the data owner organization
        StructuredBuffer oDigitalContracts = ::ListDigitalContracts(strEncodedEosb);
        for (std::string strGuid : oDigitalContracts.GetNamesOfElements())
        {
            for (unsigned int unIndex = 0; unIndex < m_stlDigitalContracts.size(); ++unIndex)
            {
                if (0 == strcmp(m_stlDigitalContracts[unIndex].m_strTitle.c_str(), oDigitalContracts.GetStructuredBuffer(strGuid.c_str()).GetString("Title").c_str()))
                {
                    if (unIndex + 1 > m_stlDigitalContractGuids.size())
                    {
                        m_stlDigitalContractGuids.resize(unIndex + 1);
                    }
                    m_stlDigitalContractGuids[unIndex] = strGuid;
                    break;
                }
            }
        }

        StructuredBuffer oDcInformation;
        oDcInformation.PutUnsignedInt64("RetentionTime", m_stlDigitalContracts.at(unIndex).m_unRetentionTime);
        oDcInformation.PutString("LegalAgreement", m_stlDigitalContracts.at(unIndex).m_strLegalAgreement);
        oDcInformation.PutString("DigitalContractGuid", m_stlDigitalContractGuids[unIndex]);
        oDcInformation.PutString("HostForVirtualMachines", m_stlDigitalContracts.at(unIndex).m_strHostForVM);
        oDcInformation.PutUnsignedInt64("NumberOfVirtualMachines", m_stlDigitalContracts.at(unIndex).m_un64NoOfVM);
        oDcInformation.PutString("HostRegion", m_stlDigitalContracts.at(unIndex).m_strHostRegion);
        // Accept digital contract
        ::AcceptDigitalContract(strEncodedEosb, oDcInformation);
    }

    std::cout << "Digital contracts approved." << std::endl;
}

/********************************************************************************************/

void __thiscall DemoDatabase::ActivateDigitalContracts(void)
{
    __DebugFunction();

    // Login to the web services as the researcher's digital contract admin
    // As the Rest API requires digital contract admin privileges
    unsigned int unDcAdminIndex = 0;
    std::string strEncodedEosb = Login(m_stlAdmins.at(unDcAdminIndex).m_strEmail, m_strPassword);
    _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);

    // Activate all digital contracts
    for (unsigned int unIndex = 0; unIndex < m_stlDigitalContractGuids.size(); ++unIndex)
    {
        StructuredBuffer oDcInformation;
        oDcInformation.PutString("DigitalContractGuid", m_stlDigitalContractGuids[unIndex]);
        // Activate digital contract
        ::ActivateDigitalContract(strEncodedEosb, oDcInformation);
    }

    std::cout << "Digital contracts activated." << std::endl;
}

/********************************************************************************************/

void __thiscall DemoDatabase::AddDatasetFamilies(void)
{
    __DebugFunction();

    std::string strEncodedEosb = Login(m_stlAdmins.at(1).m_strEmail, m_strPassword);
    _ThrowBaseExceptionIf(0 == strEncodedEosb.size(), "Failed to login, exiting!", nullptr);

    StructuredBuffer oFamilyInformation;
    oFamilyInformation.PutString("DatasetFamilyTitle", "Database Tools Dataset Family");
    oFamilyInformation.PutString("DatasetFamilyDescription", "This is a test dataset family generated from the database tools");
    oFamilyInformation.PutString("DatasetFamilyTags", "DBTools, CMDLINE, TDD");
    oFamilyInformation.PutString("VersionNumber", "0x00000001");
    oFamilyInformation.PutString("Eosb", strEncodedEosb);

    ::RegisterDatasetFamily(oFamilyInformation);
}

/********************************************************************************************/

void __thiscall DemoDatabase::DeleteDatabase(void)
{
    __DebugFunction();

    // Reset database
    try
    {
        bool fSuccess = false;
        TlsNode *poTlsNode = nullptr;
        poTlsNode = ::TlsConnectToNetworkSocket(g_szServerIpAddress, g_unPortNumber);
        _ThrowIfNull(poTlsNode, "TlsConnectToNetworkSocketWithTimeout failed.", nullptr);

        std::string strHttpLoginRequest = "DELETE /SAIL/AuthenticationManager/Admin/ResetDatabase HTTP/1.1\r\n"
                                          "Accept: */*\r\n"
                                          "Host: localhost:6200\r\n"
                                          "Connection: keep-alive\r\n"
                                          "Content-Length: 0\r\n"
                                          "\r\n";

        // Send request packet
        poTlsNode->Write((Byte *)strHttpLoginRequest.data(), (strHttpLoginRequest.size()));

        // Read Header of the Rest response one byte at a time
        bool fIsEndOfHeader = false;
        std::vector<Byte> stlHeaderData;
        while (false == fIsEndOfHeader)
        {
            std::vector<Byte> stlBuffer = poTlsNode->Read(1, 20000);
            // Check whether the read was successful or not
            if (0 < stlBuffer.size())
            {
                stlHeaderData.push_back(stlBuffer.at(0));
                if (4 <= stlHeaderData.size())
                {
                    if (("\r\n\r\n" == std::string(stlHeaderData.end() - 4, stlHeaderData.end())) || ("\n\r\n\r" == std::string(stlHeaderData.end() - 4, stlHeaderData.end())))
                    {
                        fIsEndOfHeader = true;
                    }
                }
            }
            else
            {
                fIsEndOfHeader = true;
            }
        }
        _ThrowBaseExceptionIf((0 == stlHeaderData.size()), "Dead Packet.", nullptr);

        std::string strRequestHeader = std::string(stlHeaderData.begin(), stlHeaderData.end());
        std::vector<Byte> stlSerializedResponse = ::GetResponseBody(strRequestHeader, poTlsNode);
        StructuredBuffer oResponse(stlSerializedResponse);
        _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "Error resetting the database.", nullptr);
    }
    catch (const BaseException & c_oBaseException)
    {
        ::ShowErrorMessage("Resetting the database failed!");
    }
}
