/*********************************************************************************************
 *
 * @file Organization.cpp
 * @author Luis Miguel Huapaya
 * @date 23 March 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "64BitHashes.h"
#include "Dataset.h"
#include "DatasetReInitializer.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "Organization.h"

#include <filesystem>
#include <iostream>

static const std::string gsc_strDefaultPassword{"SailPassword@123"};

/********************************************************************************************/

Organization::Organization(
    _in const std::string & c_strOrganizationName,
    _in const StructuredBuffer & c_oOrganizationalData
    )
{
    __DebugFunction();
    
    // Register the basic information
    m_fRegistered = false;
    m_strSailPlatformServicesIpAddress = "";
    m_wSailPlatformServicesPortNumber = 0;
    m_strOrganizationalName = c_strOrganizationName;
    m_strOrganizationalAddress = c_oOrganizationalData.GetString("Address");
    // Extract the contacts
    StructuredBuffer oContacts{c_oOrganizationalData.GetStructuredBuffer("Contacts")};
    oContacts.RemoveElement("__IsArray__");
    for (const std::string & c_strElementName: oContacts.GetNamesOfElements())
    {
        StructuredBuffer oContact{oContacts.GetStructuredBuffer(c_strElementName.c_str())};
        // Make sure the incoming contact is properly formatted
        if ((true == oContact.IsElementPresent("Email", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oContact.IsElementPresent("Name", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oContact.IsElementPresent("Phone Number", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oContact.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE)))
        {
            // Insert the contact m_stlContacts
            m_stlContacts.insert(oContact.GetBase64SerializedBuffer());
        }
        else
        {
            std::cout << "ERROR: Invalid contact entry encountered" << std::endl;
        }
    }
    _ThrowBaseExceptionIf((2 != m_stlContacts.size()), "INVALID ORGANIZATIONAL SPECIFICATION. You need at to specify exactly 2 contacts", nullptr);
    // Extract the administrators
    StructuredBuffer oAdministrators{c_oOrganizationalData.GetStructuredBuffer("Admins")};
    oAdministrators.RemoveElement("__IsArray__");
    for (const std::string & c_strElementName: oAdministrators.GetNamesOfElements())
    {
        StructuredBuffer oAdministrator{oAdministrators.GetStructuredBuffer(c_strElementName.c_str())};
        // Make sure the incoming contact is properly formatted
        if ((true == oAdministrator.IsElementPresent("Email", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oAdministrator.IsElementPresent("Name", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oAdministrator.IsElementPresent("Phone Number", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oAdministrator.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE)))
        {
            // Insert the contact m_stlContacts
            m_stlAdministrators.insert(oAdministrator.GetBase64SerializedBuffer());
        }
        else
        {
            std::cout << "ERROR: Invalid administrator entry encountered" << std::endl;
        }
        
    }
    _ThrowBaseExceptionIf((0 == m_stlAdministrators.size()), "INVALID ORGANIZATIONAL SPECIFICATION. You need at to specify at least one administrator", nullptr);
    // Extract the users
    if (true == c_oOrganizationalData.IsElementPresent("Users", INDEXED_BUFFER_VALUE_TYPE))
    {
        StructuredBuffer oUsers{c_oOrganizationalData.GetStructuredBuffer("Users")};
        oUsers.RemoveElement("__IsArray__");
        for (const std::string & c_strElementName: oUsers.GetNamesOfElements())
        {
            StructuredBuffer oUser{oUsers.GetStructuredBuffer(c_strElementName.c_str())};
            // Make sure the incoming contact is properly formatted
            if ((true == oUser.IsElementPresent("Email", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oUser.IsElementPresent("Name", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oUser.IsElementPresent("Phone Number", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oUser.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oUser.IsElementPresent("Access Rights", ANSI_CHARACTER_STRING_VALUE_TYPE)))
            {
                // Insert the contact m_stlContacts
                m_stlUsers.insert(oUser.GetBase64SerializedBuffer());
            }
            else
            {
                std::cout << "ERROR: Invalid user entry encountered" << std::endl;
            }
        }
    }
    // Extract the datasets
    if (true == c_oOrganizationalData.IsElementPresent("Datasets", INDEXED_BUFFER_VALUE_TYPE))
    {
        StructuredBuffer oDatasets{c_oOrganizationalData.GetStructuredBuffer("Datasets")};
        oDatasets.RemoveElement("__IsArray__");
        for (const std::string & c_strElementName: oDatasets.GetNamesOfElements())
        {
            StructuredBuffer oDatasetInformation{oDatasets.GetStructuredBuffer(c_strElementName.c_str())};
            std::string strDatasetFilename = oDatasetInformation.GetString("File");
            if (true == std::filesystem::exists(strDatasetFilename))
            {
                // Just a reality check to make sure the target file is in fact a properly formatted dataset
                Dataset oDataset(strDatasetFilename.c_str());
                // Now we persist the dataset information
                Qword qwHashOfDatasetName = ::Get64BitHashOfNullTerminatedString(oDatasetInformation.GetString("DatasetName").c_str(), false);
                m_strDatasetInformationByFilename[qwHashOfDatasetName] = oDatasetInformation.GetBase64SerializedBuffer();
            }
        }
    }
    // Extract the dataset families
    if (true == c_oOrganizationalData.IsElementPresent("DatasetFamilies", INDEXED_BUFFER_VALUE_TYPE))
    {
        StructuredBuffer oDatasetFamilies{c_oOrganizationalData.GetStructuredBuffer("DatasetFamilies")};
        oDatasetFamilies.RemoveElement("__IsArray__");
        for (const std::string & c_strElementName: oDatasetFamilies.GetNamesOfElements())
        {
            StructuredBuffer oDatasetFamily{oDatasetFamilies.GetStructuredBuffer(c_strElementName.c_str())};
            if ((true == oDatasetFamily.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oDatasetFamily.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oDatasetFamily.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE)))
            {
                // Insert the contact m_stlContacts
                m_stlDatasetFamilies.insert(oDatasetFamily.GetBase64SerializedBuffer());
            }
            else
            {
                std::cout << "ERROR: Invalid dataset family entry encountered" << std::endl;
            }
        }
    }
}

/********************************************************************************************/

Organization::~Organization(void)
{
    __DebugFunction();
}

/********************************************************************************************/

bool __thiscall Organization::Register(
    _in const std::string & c_strSailPlatformServicesIpAddress,
    _in Word wSailPlatformServicesPortNumber,
    _in unsigned int unStepIdentifier
    ) throw()
{
    __DebugFunction();
    
    try
    {
        m_strSailPlatformServicesIpAddress = c_strSailPlatformServicesIpAddress;
        m_wSailPlatformServicesPortNumber = wSailPlatformServicesPortNumber;
        
        // Step 1 --> Register organization, admins, users, dataset families and data federations
        // Step 2 --> Register datasets
        // Step 3 --> Do nothing, we are only registering Digital Contracts
        // Step 4 --> Register everything
        if (1 == unStepIdentifier)
        {
            this->RegisterOrganization();
            this->RegisterAdministrators();
            this->RegisterContacts();
            this->RegisterUsers();
            this->RegisterDataFederations();
            this->RegisterDatasetFamilies();
            m_fRegistered = true;
        }
        else if (2 == unStepIdentifier)
        {
            m_fRegistered = true;
            this->RegisterDatasets();
        }
        else if (4 == unStepIdentifier)
        {
            this->RegisterOrganization();
            this->RegisterAdministrators();
            this->RegisterContacts();
            this->RegisterUsers();
            this->RegisterDataFederations();
            this->RegisterDatasetFamilies();
            m_fRegistered = true;
            this->RegisterDatasets();
        }
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    return m_fRegistered;
}

/********************************************************************************************/

std::string __thiscall Organization::GetOrganizationalName(void) const throw()
{
    __DebugFunction();
    
    return m_strOrganizationalName;
}

/********************************************************************************************/

std::string __thiscall Organization::GetOrganizationalIdentifier(void) const throw()
{
    __DebugFunction();
    __DebugAssert(0 < m_strSailPlatformServicesIpAddress.size());
    __DebugAssert(0 < m_wSailPlatformServicesPortNumber);
    
    SailPlatformServicesSession oSailPlatformServicesSession(m_strSailPlatformServicesIpAddress, m_wSailPlatformServicesPortNumber);
    this->Login(oSailPlatformServicesSession);
    
    StructuredBuffer oBasicUserInformation(oSailPlatformServicesSession.GetBasicUserInformation());
    
    return oBasicUserInformation.GetString("OrganizationGuid");
}

/********************************************************************************************/

std::string __thiscall Organization::GetAdminUsername(void) const throw()
{
    __DebugFunction();
    
    std::string strAdminUserName{};
    
    try
    {
        StructuredBuffer oAdministrator(m_stlAdministrators.begin()->c_str());
        strAdminUserName = oAdministrator.GetString("Email");
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    return strAdminUserName;
}

/********************************************************************************************/

std::string __thiscall Organization::GetDatasetIdentifier(
    _in const std::string & c_strDatasetName
    ) const throw()
{
    __DebugFunction();
    
    std::string strDatasetIdentifier{};
    
    try
    {
        Qword qwHashOfDatasetName = ::Get64BitHashOfNullTerminatedString(c_strDatasetName.c_str(), false);
        if (m_strDatasetInformationByFilename.end() != m_strDatasetInformationByFilename.find(qwHashOfDatasetName))
        {
            StructuredBuffer oDatasetInformation(m_strDatasetInformationByFilename.at(qwHashOfDatasetName).c_str());
            std::string strDatasetFilename = oDatasetInformation.GetString("File");
            if (true == std::filesystem::exists(strDatasetFilename))
            {
                Dataset oDataset(strDatasetFilename.c_str());
                strDatasetIdentifier = oDataset.GetDatasetIdentifier();
            }
        }
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    return strDatasetIdentifier;
}

/********************************************************************************************/

std::string __thiscall Organization::GetDatasetFamilyIdentifier(
    _in const std::string & c_strDatasetFamilyName
    ) const throw()
{
    __DebugFunction();
    
    std::string strDatasetFamilyIdentifier{};
    
    try
    {
        _ThrowBaseExceptionIf((false == m_fRegistered), "ERROR: Cannot get the dataset family identifier before the organization has been registered fully", nullptr);
        
        Qword qwHashOfDatasetFamilyName = ::Get64BitHashOfNullTerminatedString(c_strDatasetFamilyName.c_str(), false);
        if (m_strDatasetFamilyIdentifiers.end() != m_strDatasetFamilyIdentifiers.find(qwHashOfDatasetFamilyName))
        {
            strDatasetFamilyIdentifier = m_strDatasetFamilyIdentifiers.at(qwHashOfDatasetFamilyName);
        }
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    return strDatasetFamilyIdentifier;
}

/********************************************************************************************/

std::string __thiscall Organization::GetDataFederationIdentifier(
    _in const std::string & c_strDataFederationName
    ) const throw()
{
    __DebugFunction();
    
    std::string strDataFederationIdentifier{};
    
    try
    {
        _ThrowBaseExceptionIf((false == m_fRegistered), "ERROR: Cannot get the data federation identifier before the organization has been registered fully", nullptr);
        
        Qword qwHashOfDataFederationName = ::Get64BitHashOfNullTerminatedString(c_strDataFederationName.c_str(), false);
        if (m_strDataFederationIdentifiers.end() != m_strDataFederationIdentifiers.find(qwHashOfDataFederationName))
        {
            strDataFederationIdentifier = m_strDataFederationIdentifiers.at(qwHashOfDataFederationName);
        }
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    return strDataFederationIdentifier;
}

/********************************************************************************************/

void __thiscall Organization::Login(
    _inout SailPlatformServicesSession & oSailPlatformServicesSession
    ) const
{
    __DebugFunction();
    
    // If there were more than one administrator specified, register the additional administrators
    std::unordered_set<std::string>::const_iterator c_stlIterator = m_stlAdministrators.begin();
    _ThrowBaseExceptionIf((m_stlAdministrators.end() == c_stlIterator), "ERROR: No administrator entry provided. Cannot login.", nullptr);
    StructuredBuffer oAdministrator(c_stlIterator->c_str());
    // Do the login
    oSailPlatformServicesSession.Login(oAdministrator.GetString("Email"), gsc_strDefaultPassword);
}
            
/********************************************************************************************/

void __thiscall Organization::RegisterOrganization(void)
{
    __DebugFunction();
    __DebugAssert(0 < m_strSailPlatformServicesIpAddress.size());
    __DebugAssert(0 < m_wSailPlatformServicesPortNumber);
    
    StructuredBuffer oRegistrationParameters;
    // Record the basic information
    oRegistrationParameters.PutString("OrganizationName", m_strOrganizationalName);
    oRegistrationParameters.PutString("OrganizationAddress", m_strOrganizationalAddress);
    // First we need to extract information about the primary contact
    std::unordered_set<std::string>::const_iterator c_stlIterator = m_stlContacts.begin();
    if (m_stlContacts.end() != c_stlIterator)
    {
        StructuredBuffer oContact(c_stlIterator->c_str());
        
        oRegistrationParameters.PutString("PrimaryContactName", oContact.GetString("Name"));
        oRegistrationParameters.PutString("PrimaryContactTitle", oContact.GetString("Title"));
        oRegistrationParameters.PutString("PrimaryContactEmail", oContact.GetString("Email"));
        oRegistrationParameters.PutString("PrimaryContactPhoneNumber", oContact.GetString("Phone Number"));
        c_stlIterator++;
    }
    // Now let's try to get the secondary contact
    if (m_stlContacts.end() != c_stlIterator)
    {
        StructuredBuffer oContact(c_stlIterator->c_str());
        
        oRegistrationParameters.PutString("SecondaryContactName", oContact.GetString("Name"));
        oRegistrationParameters.PutString("SecondaryContactTitle", oContact.GetString("Title"));
        oRegistrationParameters.PutString("SecondaryContactEmail", oContact.GetString("Email"));
        oRegistrationParameters.PutString("SecondaryContactPhoneNumber", oContact.GetString("Phone Number"));
    }
    // Now we need to know who the default administrator (i.e. initial user) is going to begin
    c_stlIterator = m_stlAdministrators.begin();
    if (m_stlAdministrators.end() != c_stlIterator)
    {
        StructuredBuffer oAdministrator(c_stlIterator->c_str());
        
        oRegistrationParameters.PutString("Name", oAdministrator.GetString("Name"));
        oRegistrationParameters.PutString("Title", oAdministrator.GetString("Title"));
        oRegistrationParameters.PutString("Email", oAdministrator.GetString("Email"));
        oRegistrationParameters.PutString("PhoneNumber", oAdministrator.GetString("Phone Number"));
        oRegistrationParameters.PutString("Password", gsc_strDefaultPassword);
    }
    
    // RegisterOrganization doesn't need you to be logged in at first.
    SailPlatformServicesSession oSailPlatformServicesSession(m_strSailPlatformServicesIpAddress, m_wSailPlatformServicesPortNumber);
    oSailPlatformServicesSession.RegisterOrganization(oRegistrationParameters);
}

/********************************************************************************************/

void __thiscall Organization::RegisterAdministrators(void)
{
    __DebugFunction();
    __DebugAssert(0 < m_strSailPlatformServicesIpAddress.size());
    __DebugAssert(0 < m_wSailPlatformServicesPortNumber);
    
    // Start a new session with SAIL Platform Services using the default administrator
    SailPlatformServicesSession oSailPlatformServicesSession(m_strSailPlatformServicesIpAddress, m_wSailPlatformServicesPortNumber);
    this->Login(oSailPlatformServicesSession);
    // Now that we have skipped the first entry, let's process all of the additional entries
    // Basically, we are adding new users with admin access rights
    std::unordered_set<std::string>::const_iterator c_stlIterator = m_stlAdministrators.begin();
    // We need to skip the first administrator, since that user was registered when the
    // organization was registered
    c_stlIterator++;
    // Now let's parse through the remaining admins and register then
    while (m_stlAdministrators.end() != c_stlIterator)
    {
        StructuredBuffer oAdministrator(c_stlIterator->c_str());
        StructuredBuffer oRegistrationParameters;

        oRegistrationParameters.PutString("Email", oAdministrator.GetString("Email"));
        oRegistrationParameters.PutString("Password", gsc_strDefaultPassword);
        oRegistrationParameters.PutString("Name", oAdministrator.GetString("Name"));
        oRegistrationParameters.PutString("PhoneNumber", oAdministrator.GetString("Phone Number"));
        oRegistrationParameters.PutString("Title", oAdministrator.GetString("Title"));
        oRegistrationParameters.PutQword("AccessRights", 0x1111111111111111);
        
        oSailPlatformServicesSession.RegisterUser(oRegistrationParameters);
        c_stlIterator++;
    }
}

/********************************************************************************************/

void __thiscall Organization::RegisterContacts(void)
{
    __DebugFunction();
    __DebugAssert(0 < m_strSailPlatformServicesIpAddress.size());
    __DebugAssert(0 < m_wSailPlatformServicesPortNumber);
    
    // This isn't used right now since contacts are not currently registered separately
    // from the organization registration. This will happen in the future, and thus this
    // method is a placeholder
}

/********************************************************************************************/

void __thiscall Organization::RegisterUsers(void)
{
    __DebugFunction();
    __DebugAssert(0 < m_strSailPlatformServicesIpAddress.size());
    __DebugAssert(0 < m_wSailPlatformServicesPortNumber);
    
    // Start a new session with SAIL Platform Services using the default administrator
    SailPlatformServicesSession oSailPlatformServicesSession(m_strSailPlatformServicesIpAddress, m_wSailPlatformServicesPortNumber);
    this->Login(oSailPlatformServicesSession);
    // Now that we have skipped the first entry, let's process all of the additional entries
    // Basically, we are adding new users with admin access rights
    std::unordered_set<std::string>::const_iterator c_stlIterator = m_stlUsers.begin();
    while (m_stlUsers.end() != c_stlIterator)
    {
        StructuredBuffer oUser(c_stlIterator->c_str());
        StructuredBuffer oRegistrationParameters;

        oRegistrationParameters.PutString("Email", oUser.GetString("Email"));
        oRegistrationParameters.PutString("Password", gsc_strDefaultPassword);
        oRegistrationParameters.PutString("Name", oUser.GetString("Name"));
        oRegistrationParameters.PutString("PhoneNumber", oUser.GetString("Phone Number"));
        oRegistrationParameters.PutString("Title", oUser.GetString("Title"));
        oRegistrationParameters.PutQword("AccessRights", 0x1111111111111111);
        
        oSailPlatformServicesSession.RegisterUser(oRegistrationParameters);
        c_stlIterator++;
    }
}

/********************************************************************************************/

void __thiscall Organization::RegisterDataFederations(void)
{
    __DebugFunction();
    __DebugAssert(0 < m_strSailPlatformServicesIpAddress.size());
    __DebugAssert(0 < m_wSailPlatformServicesPortNumber);
    
    // This is a placeholder for now since data federations aren't implemented yet
}

/********************************************************************************************/

void __thiscall Organization::RegisterDatasetFamilies(void)
{
    __DebugFunction();
    __DebugAssert(0 < m_strSailPlatformServicesIpAddress.size());
    __DebugAssert(0 < m_wSailPlatformServicesPortNumber);
    
    // Start a new session with SAIL Platform Services using the default administrator
    SailPlatformServicesSession oSailPlatformServicesSession(m_strSailPlatformServicesIpAddress, m_wSailPlatformServicesPortNumber);
    this->Login(oSailPlatformServicesSession);
    // Now that we have skipped the first entry, let's process all of the additional entries
    // Basically, we are adding new users with admin access rights
    std::unordered_set<std::string>::const_iterator c_stlIterator = m_stlDatasetFamilies.begin();
    while (m_stlDatasetFamilies.end() != c_stlIterator)
    {
        StructuredBuffer oDatasetFamily(c_stlIterator->c_str());
        StructuredBuffer oRegistrationParameters;
        
        oRegistrationParameters.PutString("DatasetFamilyTitle", oDatasetFamily.GetString("Title"));
        oRegistrationParameters.PutString("DatasetFamilyDescription", oDatasetFamily.GetString("Description"));
        oRegistrationParameters.PutString("DatasetFamilyTags", oDatasetFamily.GetString("Tags"));
        oRegistrationParameters.PutString("VersionNumber", "0x00000001");
    
        std::string strDatasetFamilyIdentifier = oSailPlatformServicesSession.RegisterDatasetFamily(oRegistrationParameters);
        // Make sure the register the dataset family identifier that is returned
        Qword qwHashOfDatasetFamilyName = ::Get64BitHashOfNullTerminatedString(oDatasetFamily.GetString("Title").c_str(), false);
        m_strDatasetFamilyIdentifiers[qwHashOfDatasetFamilyName] = strDatasetFamilyIdentifier;
        // Move on to the next item
        c_stlIterator++;
    }
}

/********************************************************************************************/

void __thiscall Organization::RegisterDatasets(void)
{
    __DebugFunction();
    __DebugAssert(0 < m_strSailPlatformServicesIpAddress.size());
    __DebugAssert(0 < m_wSailPlatformServicesPortNumber);
    
    // Start a new session with SAIL Platform Services using the default administrator
    SailPlatformServicesSession oSailPlatformServicesSession(m_strSailPlatformServicesIpAddress, m_wSailPlatformServicesPortNumber);
    this->Login(oSailPlatformServicesSession);
    // Get some basic user information. We will need this in order to update the OrganizationalIdentifier
    // in the dataset
    StructuredBuffer oBasicUserInformation(oSailPlatformServicesSession.GetBasicUserInformation());
    // Now that we have skipped the first entry, let's process all of the additional entries
    // Basically, we are adding new users with admin access rights
    std::unordered_map<Qword, std::string>::const_iterator c_stlIterator = m_strDatasetInformationByFilename.begin();
    while (m_strDatasetInformationByFilename.end() != c_stlIterator)
    {        
        // Load the serialized dataset information into a StructuredBuffer in order to access it
        StructuredBuffer oDatasetInformation(c_stlIterator->second.c_str());
        // Load an existing dataset. This dataset will be modified during registration, hence
        // the reason why a DatassetReInitializer class was created, which wraps the
        // shared Dataset class that is designed as an accessor only
        DatasetReInitializer oDatasetReInitializer(oDatasetInformation.GetString("File"));
        // Now we start resetting some of the values in the dataset to reflect what is about to be
        // registered.
        // Create a new identifier
        oDatasetReInitializer.SetDatasetIdentifier(Guid(eDataset));
        // Make sure the corporate identifier is updated
        oDatasetReInitializer.SetCorporateIdentifier(Guid(oBasicUserInformation.GetString("OrganizationGuid")));
        // Reset the publish date
        oDatasetReInitializer.ResetUtcEpochPublishDate();
        // If a new Title is provided in the JSON, update the title of the dataset
        if (true == oDatasetInformation.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            oDatasetReInitializer.SetDatasetTitle(oDatasetInformation.GetString("Title"));
        }
        // If a new Description is provided in the JSON, update the description of the dataset
        if (true == oDatasetInformation.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            oDatasetReInitializer.SetDatasetDescription(oDatasetInformation.GetString("Description"));
        }
        // If a new Tags are provided in the JSON, update the tags of the dataset
        if (true == oDatasetInformation.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            oDatasetReInitializer.SetDatasetKeywords(oDatasetInformation.GetString("Tags"));
        }
        // If the new dataset has a dataset family assigned to it
        if (true == oDatasetInformation.IsElementPresent("DatasetFamily", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            oDatasetReInitializer.SetDatasetFamily(this->GetDatasetFamilyIdentifier(oDatasetInformation.GetString("DatasetFamily")));
        }
        else
        {
            // If it doesn't have a dataset family assigned, make sure the updated dataset
            // doesn't have one
            oDatasetReInitializer.RemoveDatasetFamily();
        }
        // Now we register the dataset using the updated information
        StructuredBuffer oDatasetMetadata(oDatasetReInitializer.GetSerializedDatasetMetadata());
        oSailPlatformServicesSession.RegisterDataset(oDatasetReInitializer.GetDatasetIdentifier(), oDatasetMetadata);
        
        // If we get here, the dataset was successfully registered. As such, let's persist
        // the dataset changes to file
        oDatasetReInitializer.SaveDatasetUpdates();
        
        // If we get here, then the registration process has worked. Let's
        c_stlIterator++;
    }
}
