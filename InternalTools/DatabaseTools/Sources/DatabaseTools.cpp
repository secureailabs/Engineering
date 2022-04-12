/*********************************************************************************************
 *
 * @file DatabaseTools.cpp
 * @author Shabana Akhtar Baig
 * @date 24 March 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "DatabaseTools.h"
#include "Base64Encoder.h"
#include "InitializationVector.h"

/********************************************************************************************/

DatabaseTools::DatabaseTools(
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

DatabaseTools::~DatabaseTools(void)
{
    __DebugFunction();

    m_stlOrganizations.clear();
    m_stlAdmins.clear();
    m_stlUsers.clear();
    m_stlDigitalContractGuids.clear();
    m_stlDigitalContracts.clear();
}

/********************************************************************************************/

void __thiscall DatabaseTools::InitializeMembers(void)
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
    // Add other users information
    m_stlUsers.push_back(UserInformation{"pcarey@igr.com", "Philip Carey", "Network Engineer", "000-000-0000", eAuditor});
    m_stlUsers.push_back(UserInformation{"abede@igr.com", "Adam Bede", "Supply Generator", "000-000-0000", eOrganizationUser});
    m_stlUsers.push_back(UserInformation{"nhelmer@mghl.com", "Nora Helmer", "Network Engineer", "000-000-0000", eAuditor});
    m_stlUsers.push_back(UserInformation{"rcory@mghl.com", "Richard Cory", "Data Scientist", "000-000-0000", eOrganizationUser});
    m_stlUsers.push_back(UserInformation{"sbowles@kca.com", "Sally Bowles", "Network Engineer", "000-000-0000", eAuditor});
    m_stlUsers.push_back(UserInformation{"pmason@kca.com", "Perry Mason", "Research Scientist", "000-000-0000", eOrganizationUser});
    m_stlUsers.push_back(UserInformation{"ncarter@crh.com", "Nick Carter", "Network Engineer", "000-000-0000", eAuditor});
    m_stlUsers.push_back(UserInformation("dquilp@crh.com", "Daniel Quilp", "Data Scientist", "000-000-0000", eOrganizationUser));
    // Initialize to the number of other users that will be added for each organization
    m_unNumberOfOtherUsers = 2;
    // Add datasets information
    m_stlDatasets.push_back(DatasetInformation("Datataset_001.csvp"));
    m_stlDatasets.push_back(DatasetInformation("Datataset_002.csvp"));
    m_stlDatasets.push_back(DatasetInformation("Datataset_003.csvp"));
    m_stlDatasets.push_back(DatasetInformation("Datataset_004.csvp"));
    m_stlDatasets.push_back(DatasetInformation("Datataset_005.csvp"));
    m_stlDatasets.push_back(DatasetInformation("Datataset_006.csvp"));
    m_stlDatasets.push_back(DatasetInformation("Datataset_007.csvp"));
    m_stlDatasets.push_back(DatasetInformation("Datataset_008.csvp"));
    // Add digital contracts information
    std::string strLegalAgreement = "The Parties acknowledge and agree that this Agreement represents the entire agreement between the Parties. "
                                    "In the event that the Parties desire to change, add, or otherwise modify any terms, they shall do so in writing to be signed by both parties.";
    std::string strDescription = "The dataset will be used to train models for academic research purposes.";
    m_stlDigitalContracts.push_back(DigitalContractInformation{"Kidney Cancer Research Consortium", 10, strLegalAgreement, 16186603, strDescription, "Researcher", 2, "East US"});
    m_stlDigitalContracts.push_back(DigitalContractInformation{"Diabetes Re-admission Model Phase 1", 28, strLegalAgreement, 24117352, strDescription, "Data Owner", 4, "East US"});
    m_stlDigitalContracts.push_back(DigitalContractInformation{"Churn Prediction Project", 35, strLegalAgreement, 60768913, strDescription, "Researcher", 5, "West Europe"});
    m_stlDigitalContracts.push_back(DigitalContractInformation{"Harvest Model", 90, strLegalAgreement, 8090084, strDescription, "SAIL", 2, "West Europe"});
    m_stlDigitalContracts.push_back(DigitalContractInformation{"Obesity Model", 120, strLegalAgreement, 18605667, strDescription, "SAIL", 1, "East US 2"});
}

/********************************************************************************************/

void __thiscall DatabaseTools::AddOrganizationsAndSuperAdmins(void)
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

void __thiscall DatabaseTools::AddOtherUsers(void)
{
    __DebugFunction();

    // Register users for organizations
    for (unsigned int unIndex = 0; unIndex < m_stlOrganizations.size(); ++unIndex)
    {
        // Login to the web services
        std::string strEncodedEosb = Login(m_stlAdmins.at(unIndex).m_strEmail, m_strPassword);
        _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);
        // Get organization guid from eosb
        StructuredBuffer oUserInformation(::GetBasicUserInformation(strEncodedEosb));
        std::string strOrganizationGuid = oUserInformation.GetString("OrganizationGuid");
        // Add organization guid to the organization structure
        m_stlOrganizations.at(unIndex).m_strOrganizationGuid = strOrganizationGuid;
        // Add m_unNumberOfOtherUsers for each organization
        // Calculate index based on the number of other users per organization
        unsigned int unUserIndex = unIndex * m_unNumberOfOtherUsers;
        for (; unUserIndex < (unIndex * m_unNumberOfOtherUsers + m_unNumberOfOtherUsers); ++unUserIndex)
        {
            StructuredBuffer oUserInformation;
            oUserInformation.PutString("Email", m_stlUsers.at(unUserIndex).m_strEmail);
            oUserInformation.PutString("Password", m_strPassword);
            oUserInformation.PutString("Name", m_stlUsers.at(unUserIndex).m_strName);
            oUserInformation.PutString("PhoneNumber", m_stlUsers.at(unUserIndex).m_strPhoneNumber);
            oUserInformation.PutString("Title", m_stlUsers.at(unUserIndex).m_strTitle);
            oUserInformation.PutQword("AccessRights", m_stlUsers.at(unUserIndex).m_qwAccessRights);
            ::RegisterUser(strEncodedEosb, strOrganizationGuid, oUserInformation);
        }
    }

    std::cout << "Users added to organizations successfully." << std::endl;
}

/********************************************************************************************/

void __thiscall DatabaseTools::AddDatasets(void)
{
    __DebugFunction();

    unsigned int unDooIndex = 1;
    // Login to the web services as one of the users from the data owner organization
    std::string strEncodedEosb = Login(m_stlAdmins.at(unDooIndex).m_strEmail, m_strPassword);
    _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);
    // Register five datasets for the data owner organizations
    // The dataset guids will later be used in the digital contracts
    for (unsigned int unIndex = 0; unIndex < m_stlDatasets.size(); ++unIndex)
    {
        ::RegisterDataset(strEncodedEosb, StructuredBuffer(m_stlDatasets.at(unIndex).m_oDataset.GetSerializedDatasetMetadata()));
    }

    std::cout << "Datasets added successfully." << std::endl;
}

/********************************************************************************************/

void __thiscall DatabaseTools::AddDigitalContracts(void)
{
    __DebugFunction();

    // First organization is the researcher organization and second organization is the data owner organization
    unsigned int unRoIndex = 0, unDooIndex = 1;
    // Login to the web services
    std::string strEncodedEosb = Login(m_stlAdmins.at(unRoIndex).m_strEmail, m_strPassword);
    _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);
    // Get organization guids for the organizations
    std::string strRoGuid = m_stlOrganizations.at(unRoIndex).m_strOrganizationGuid;
    // Add digital contract information
    std::string strDooGuid = m_stlOrganizations.at(unDooIndex).m_strOrganizationGuid;
    StructuredBuffer oDcInformation;
    oDcInformation.PutString("DOOGuid", strDooGuid);
    // Register five digital contracts for the organizations
    for (unsigned int unIndex = 0; unIndex < m_stlDigitalContracts.size(); ++unIndex)
    {
        oDcInformation.PutString("Title", m_stlDigitalContracts.at(unIndex).m_strTitle);
        oDcInformation.PutUnsignedInt64("SubscriptionDays", m_stlDigitalContracts.at(unIndex).m_unSubscriptionDays);
        oDcInformation.PutString("LegalAgreement", m_stlDigitalContracts.at(unIndex).m_strLegalAgreement);
        oDcInformation.PutString("Description", m_stlDigitalContracts.at(unIndex).m_strDescription);
        oDcInformation.PutString("DatasetGuid", m_stlDatasets.at(unIndex).m_oDataset.GetDatasetIdentifier());
        // Register digital contract
        ::RegisterDigitalContract(strEncodedEosb, oDcInformation);
    }

    std::cout << "Digital contracts added successfully." << std::endl;
}

/********************************************************************************************/

void __thiscall DatabaseTools::AcceptDigitalContracts(void)
{
    __DebugFunction();

    // Login to the web services as the data owner's dataset admin
    // As the Rest API requires dataset admin privileges
    unsigned int unDatasetAdminIndex = 1;
    std::string strEncodedEosb = Login(m_stlAdmins.at(unDatasetAdminIndex).m_strEmail, m_strPassword);
    _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);
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
    // Accept all five digital contracts
    for (unsigned int unIndex = 0; unIndex < m_stlDigitalContracts.size(); ++unIndex)
    {
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

void __thiscall DatabaseTools::ActivateDigitalContracts(void)
{
    __DebugFunction();

    // Login to the web services as the researcher's digital contract admin
    // As the Rest API requires digital contract admin privileges
    unsigned int unDcAdminIndex = 0;
    std::string strEncodedEosb = Login(m_stlAdmins.at(unDcAdminIndex).m_strEmail, m_strPassword);
    _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);

    // Activate all five digital contracts
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

void __thiscall DatabaseTools::AddVirtualMachine(void)
{
    __DebugFunction();

    // Login to the web services with DOO admin credentials
    std::string strEncodedEosb = Login(m_stlAdmins.at(1).m_strEmail, m_strPassword);
    _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);
    // Get list of all digital contracts for the data owner organization
    for (std::string strGuid : StructuredBuffer(::ListDigitalContracts(strEncodedEosb)).GetNamesOfElements())
    {
        m_stlDigitalContractGuids.push_back(strGuid);
    }
    // Get imposter eosb
    std::string strIEosb = ::GetIEosb(strEncodedEosb);
    _ThrowBaseExceptionIf((0 == strIEosb.size()), "Exiting!", nullptr);
    // Add Vm information
    StructuredBuffer oVmInformation;
    oVmInformation.PutString("DigitalContractGuid", m_stlDigitalContractGuids.at(0));
    oVmInformation.PutString("IPAddress", "127.0.0.1");
    oVmInformation.PutString("HostRegion", "East US");
    // Register Vm
    std::string strVmGuid = Guid(eSecureComputationalVirtualMachine).ToString(eHyphensAndCurlyBraces);
    std::string strVmEosb = ::RegisterVirtualMachine(strIEosb, strVmGuid, oVmInformation);
    // Check if the virtual machine was registered successfully
    _ThrowBaseExceptionIf((0 == strVmEosb.size()), "Error occurred when registering a virtual machine.", nullptr);
    std::cout << "Virtual machine registered successfully." << std::endl;
    // Register VM for DOO and add leaf events
    this->RegisterVmAfterDataUpload(strVmGuid);
    // Register VM for RO and add leaf events
    this->RegisterVmForComputation(strVmGuid);
}

void __thiscall DatabaseTools::AddDatasetFamilies(void)
{
    __DebugFunction();

    std::string strEncodedEosb = Login(m_stlUsers.at(2).m_strEmail, m_strPassword);
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

void __thiscall DatabaseTools::RegisterVmAfterDataUpload(
    _in const std::string & c_strVmGuid
    )
{
    __DebugFunction();

    // Login to the web services with DOO admin credentials
    std::string strEncodedEosb = Login(m_stlAdmins.at(1).m_strEmail, m_strPassword);
    _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);
    // Add Vm information
    StructuredBuffer oVmInformation;
    oVmInformation.PutString("DigitalContractGuid", m_stlDigitalContractGuids.at(0));
    // Generate VM branch event for DOO
    std::string strVmEventGuid = ::RegisterVmAfterDataUpload(strEncodedEosb, c_strVmGuid);
    // Check if the virtual machine was registered successfully
    _ThrowBaseExceptionIf((0 == strVmEventGuid.size()), "Error occurred when adding VM branch event for data owner organization", nullptr);
    std::cout << "VM branch event added for DOO." << std::endl;
    // Create vector representing event names
    std::vector<std::string> stlEventNames = {"VM_STARTED", "VM_INITIALIZED", "VM_DATASET_UPLOADED", "VM_READY", "CONNECT_SUCCESS"};
    for (unsigned int unIndex = 0; unIndex < 4; ++unIndex)
    {
        stlEventNames.push_back("PUSH_DATA");
        stlEventNames.push_back("PUSH_FN");
        stlEventNames.push_back("RUN_FN");
        stlEventNames.push_back("CHECK_JOB");
        stlEventNames.push_back("PULL_DATA");
    }
    stlEventNames.push_back("INSPECT");
    stlEventNames.push_back("GET_TABLE");
    stlEventNames.push_back("DELETE_DATA");
    stlEventNames.push_back("LOGOFF");
    stlEventNames.push_back("VM_SHUTTING_DOWN");
    // Add leaf events information
    uint64_t un64EpochTimeInMilliseconds = ::GetEpochTimeInMilliseconds();
    StructuredBuffer oLeafEvents;
    for (unsigned int unIndex = 0; unIndex < 30; ++unIndex)
    {
        StructuredBuffer oEvent;
        oEvent.PutString("EventGuid", Guid(eAuditEvent_PlainTextLeafNode).ToString(eHyphensAndCurlyBraces));
        oEvent.PutQword("EventType", unIndex % 16);
        un64EpochTimeInMilliseconds += 1000;
        oEvent.PutUnsignedInt64("Timestamp", un64EpochTimeInMilliseconds);
        StructuredBuffer oEncryptedEventData;
        oEncryptedEventData.PutString("EventName", stlEventNames.at(unIndex));
        oEncryptedEventData.PutByte("EventType", unIndex + 1);
        StructuredBuffer oEventData;
        oEventData.PutUnsignedInt64("VersionNumber", 0x0000000100000001);
        oEventData.PutUnsignedInt64("Timestamp", ::GetEpochTimeInMilliseconds());
        oEncryptedEventData.PutStructuredBuffer("EventData", oEventData);
        oEvent.PutString("EncryptedEventData", ::Base64Encode(oEncryptedEventData.GetSerializedBufferRawDataPtr(), oEncryptedEventData.GetSerializedBufferRawDataSizeInBytes()));
        oLeafEvents.PutStructuredBuffer(std::to_string(unIndex).c_str(), oEvent);
    }
    // Register leaf events for DOO
    ::RegisterLeafEvents(strEncodedEosb, strVmEventGuid, oLeafEvents);
}

/********************************************************************************************/

void __thiscall DatabaseTools::RegisterVmForComputation(
    _in const std::string & c_strVmGuid
    )
{
    __DebugFunction();

    // Login to the web services with RO admin credentials
    std::string strEncodedEosb = Login(m_stlAdmins.at(0).m_strEmail, m_strPassword);
    _ThrowBaseExceptionIf((0 == strEncodedEosb.size()), "Exiting!", nullptr);
    // Add Vm information
    StructuredBuffer oVmInformation;
    oVmInformation.PutString("DigitalContractGuid", m_stlDigitalContractGuids.at(0));
    // Generate VM branch event for DOO
    std::string strVmEventGuid = ::RegisterVmForComputation(strEncodedEosb, c_strVmGuid);
    // Check if the virtual machine was registered successfully
    _ThrowBaseExceptionIf((0 == strVmEventGuid.size()), "Error occurred when adding VM branch event for researcher organization", nullptr);
    std::cout << "VM branch event added for RO." << std::endl;
    // Create vector representing event names
    std::vector<std::string> stlEventNames = {"VM_STARTED", "VM_INITIALIZED", "VM_DATASET_UPLOADED", "VM_READY", "CONNECT_SUCCESS"};
    for (unsigned int unIndex = 0; unIndex < 4; ++unIndex)
    {
        stlEventNames.push_back("PUSH_DATA");
        stlEventNames.push_back("PUSH_FN");
        stlEventNames.push_back("RUN_FN");
        stlEventNames.push_back("CHECK_JOB");
        stlEventNames.push_back("PULL_DATA");
    }
    stlEventNames.push_back("INSPECT");
    stlEventNames.push_back("GET_TABLE");
    stlEventNames.push_back("DELETE_DATA");
    stlEventNames.push_back("LOGOFF");
    stlEventNames.push_back("VM_SHUTTING_DOWN");
    // Add leaf events information
    StructuredBuffer oLeafEvents;
    for (unsigned int unIndex = 0; unIndex < 30; ++unIndex)
    {
        StructuredBuffer oEvent;
        oEvent.PutString("EventGuid", Guid(eAuditEvent_PlainTextLeafNode).ToString(eHyphensAndCurlyBraces));
        oEvent.PutQword("EventType", unIndex % 16);
        oEvent.PutUnsignedInt64("Timestamp", ::GetEpochTimeInMilliseconds());
        StructuredBuffer oEncryptedEventData;
        oEncryptedEventData.PutString("EventName", stlEventNames.at(unIndex));
        oEncryptedEventData.PutByte("EventType", unIndex + 1);
        StructuredBuffer oEventData;
        oEventData.PutUnsignedInt64("VersionNumber", 0x0000000100000001);
        oEventData.PutUnsignedInt64("Timestamp", ::GetEpochTimeInMilliseconds());
        oEncryptedEventData.PutStructuredBuffer("EventData", oEventData);
        oEvent.PutString("EncryptedEventData", ::Base64Encode(oEncryptedEventData.GetSerializedBufferRawDataPtr(), oEncryptedEventData.GetSerializedBufferRawDataSizeInBytes()));
        oLeafEvents.PutStructuredBuffer(std::to_string(unIndex).c_str(), oEvent);
    }
    // Register leaf events for DOO
    ::RegisterLeafEvents(strEncodedEosb, strVmEventGuid, oLeafEvents);
}

/********************************************************************************************/

void __thiscall DatabaseTools::DeleteDatabase(void)
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
