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
#include "DatasetVersion.h"
#include "DatasetVersionReInitializer.h"
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
    _in const StructuredBuffer & c_oOrganizationalData,
    _in unsigned int unStepIdentifier
    )
{
    __DebugFunction();

    // Register the basic information
    m_fRegistered = false;
    m_strSailPlatformServicesIpAddress = "";
    m_wSailPlatformServicesPortNumber = 0;
    m_strOrganizationalName = c_strOrganizationName;
    m_strOrganizationalDescription = c_oOrganizationalData.GetString("Description");

    // Extract the administrators
    StructuredBuffer oAdministrators{c_oOrganizationalData.GetStructuredBuffer("Admins")};
    if (true == oAdministrators.IsElementPresent("__IsArray__", BOOLEAN_VALUE_TYPE))
    {
        oAdministrators.RemoveElement("__IsArray__");
    }
    for (const std::string & c_strElementName: oAdministrators.GetNamesOfElements())
    {
        StructuredBuffer oAdministrator{oAdministrators.GetStructuredBuffer(c_strElementName.c_str())};
        // Make sure the incoming contact is properly formatted
        if ((true == oAdministrator.IsElementPresent("Email", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oAdministrator.IsElementPresent("Name", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oAdministrator.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE)))
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
        if (true == oUsers.IsElementPresent("__IsArray__", BOOLEAN_VALUE_TYPE))
        {
            oUsers.RemoveElement("__IsArray__");
        }
        for (const std::string & c_strElementName: oUsers.GetNamesOfElements())
        {
            StructuredBuffer oUser{oUsers.GetStructuredBuffer(c_strElementName.c_str())};
            // Make sure the incoming contact is properly formatted
            if ((true == oUser.IsElementPresent("Email", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oUser.IsElementPresent("Name", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oUser.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oUser.IsElementPresent("Role", ANSI_CHARACTER_STRING_VALUE_TYPE)))
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
    if (true == c_oOrganizationalData.IsElementPresent("DatasetVersions", INDEXED_BUFFER_VALUE_TYPE))
    {
        StructuredBuffer oDatasetVersions{c_oOrganizationalData.GetStructuredBuffer("DatasetVersions")};
        if (true == oDatasetVersions.IsElementPresent("__IsArray__", BOOLEAN_VALUE_TYPE))
        {
            oDatasetVersions.RemoveElement("__IsArray__");
        }
        for (const std::string & c_strElementName: oDatasetVersions.GetNamesOfElements())
        {
            StructuredBuffer oDatasetVersionInformation{oDatasetVersions.GetStructuredBuffer(c_strElementName.c_str())};
            std::string strDatasetVersionFilename = oDatasetVersionInformation.GetString("File");
            if (true == std::filesystem::exists(strDatasetVersionFilename))
            {
                // Just a reality check to make sure the target file is in fact a properly formatted dataset
                DatasetVersion oDatasetVersion(strDatasetVersionFilename.c_str());
                // Now we persist the dataset information
                Qword qwHashOfDatasetVersionName = ::Get64BitHashOfNullTerminatedString(oDatasetVersionInformation.GetString("Name").c_str(), false);
                m_strDatasetVersionInformationByFilename[qwHashOfDatasetVersionName] = oDatasetVersionInformation.GetBase64SerializedBuffer();
            }
        }
    }
    // Extract the datasets
    if (true == c_oOrganizationalData.IsElementPresent("Datasets", INDEXED_BUFFER_VALUE_TYPE))
    {
        StructuredBuffer oDatasets{c_oOrganizationalData.GetStructuredBuffer("Datasets")};
        if (true == oDatasets.IsElementPresent("__IsArray__", BOOLEAN_VALUE_TYPE))
        {
            oDatasets.RemoveElement("__IsArray__");
        }
        for (const std::string & c_strElementName: oDatasets.GetNamesOfElements())
        {
            StructuredBuffer oDataset{oDatasets.GetStructuredBuffer(c_strElementName.c_str())};
            if ((true == oDataset.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oDataset.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oDataset.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE)))
            {
                std::cout << oDataset.GetString("Title") << std::endl;
                // Insert the contact m_stlContacts
                m_stlDatasets.insert(oDataset.GetBase64SerializedBuffer());
            }
            else
            {
                std::cout << "ERROR: Invalid dataset entry encountered" << std::endl;
            }
        }
    }
    if ( true == c_oOrganizationalData.IsElementPresent("Data Federation", INDEXED_BUFFER_VALUE_TYPE))
    {
        StructuredBuffer oFederations{c_oOrganizationalData.GetStructuredBuffer("Data Federation")};
        if (true == oFederations.IsElementPresent("__IsArray__", BOOLEAN_VALUE_TYPE))
        {
            oFederations.RemoveElement("__IsArray__");
        }
        for (const std::string & c_strElementName: oFederations.GetNamesOfElements())
        {
            StructuredBuffer oFederation{oFederations.GetStructuredBuffer(c_strElementName.c_str())};
            if ((true == oFederation.IsElementPresent("DataFederationName", ANSI_CHARACTER_STRING_VALUE_TYPE))&&(true == oFederation.IsElementPresent("DataFederationDescription", ANSI_CHARACTER_STRING_VALUE_TYPE)))
            {
                m_stlDataFederations.insert(oFederation.GetBase64SerializedBuffer());
            }
            else
            {
                std::cout << "ERROR: Invalid federation entry encountered" << std::endl;
            }
        }
    }
    if (1 != unStepIdentifier)
    {
        // Extract the datasets
        if (true == c_oOrganizationalData.IsElementPresent("DatasetVersions", INDEXED_BUFFER_VALUE_TYPE))
        {
            StructuredBuffer oDatasetVersions{c_oOrganizationalData.GetStructuredBuffer("DatasetVersions")};
            if (true == oDatasetVersions.IsElementPresent("__IsArray__", BOOLEAN_VALUE_TYPE))
            {
                oDatasetVersions.RemoveElement("__IsArray__");
            }
            for (const std::string & c_strElementName: oDatasetVersions.GetNamesOfElements())
            {
                StructuredBuffer oDatasetVersionInformation{oDatasetVersions.GetStructuredBuffer(c_strElementName.c_str())};
                std::string strDatasetVersionFilename = oDatasetVersionInformation.GetString("File");
                if (true == std::filesystem::exists(strDatasetVersionFilename))
                {
                    // Just a reality check to make sure the target file is in fact a properly formatted dataset
                    DatasetVersion oDatasetVersion(strDatasetVersionFilename.c_str());
                    // Now we persist the dataset information
                    Qword qwHashOfDatasetVersionName = ::Get64BitHashOfNullTerminatedString(oDatasetVersionInformation.GetString("Name").c_str(), false);
                    m_strDatasetVersionInformationByFilename[qwHashOfDatasetVersionName] = oDatasetVersionInformation.GetBase64SerializedBuffer();
                }
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
    _in unsigned int unStepIdentifier,
    std::unordered_map<std::string, Guid>& registeredFederations
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
            std::cout << "001" << std::endl;
            this->RegisterOrganization();
            std::cout << "003" << std::endl;
            this->RegisterContacts();
            std::cout << "004" << std::endl;
            this->RegisterUsers();
            std::cout << "005" << std::endl;
            this->RegisterDataFederations(registeredFederations);
            std::cout << "006" << std::endl;
            this->RegisterDatasets();
            std::cout << "007" << std::endl;
            m_fRegistered = true;
        }
        else if (2 == unStepIdentifier)
        {
            m_fRegistered = true;
            this->RegisterDatasetVersions();
        }
        else if (4 == unStepIdentifier)
        {
            this->RegisterOrganization();
            this->RegisterContacts();
            this->RegisterUsers();
            this->RegisterDataFederations(registeredFederations);
            this->RegisterDatasets();
            m_fRegistered = true;
            this->RegisterDatasetVersions();
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

    StructuredBuffer oBasicUserInformation = oSailPlatformServicesSession.GetBasicUserInformation();
    return oBasicUserInformation.GetStructuredBuffer("organization").GetString("id");
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

std::string __thiscall Organization::GetDatasetVersionIdentifier(
    _in const std::string & c_strDatasetVersionName
    ) const throw()
{
    __DebugFunction();
    
    std::string strDatasetVersionIdentifier{};

    try
    {
        Qword qwHashOfDatasetVersionName = ::Get64BitHashOfNullTerminatedString(c_strDatasetVersionName.c_str(), false);
        if (m_strDatasetVersionInformationByFilename.end() != m_strDatasetVersionInformationByFilename.find(qwHashOfDatasetVersionName))
        {
            StructuredBuffer oDatasetVersionInformation(m_strDatasetVersionInformationByFilename.at(qwHashOfDatasetVersionName).c_str());
            std::string strDatasetVersionFilename = oDatasetVersionInformation.GetString("File");
            if (true == std::filesystem::exists(strDatasetVersionFilename))
            {
                DatasetVersion oDatasetVersion(strDatasetVersionFilename.c_str());
                strDatasetVersionIdentifier = oDatasetVersion.GetDatasetVersionIdentifier();
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
    
    return strDatasetVersionIdentifier;
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
        _ThrowBaseExceptionIf((false == m_fRegistered), "ERROR: Cannot get the dataset identifier before the organization has been registered fully", nullptr);

        if (m_strDatasetIdentifiers.end() != m_strDatasetIdentifiers.find(c_strDatasetName))
        {
            strDatasetIdentifier = m_strDatasetIdentifiers.at(c_strDatasetName);
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
    oSailPlatformServicesSession.Login(oAdministrator.GetString("Email"), m_adminUserPassword);
}

/********************************************************************************************/

void __thiscall Organization::RegisterOrganization(void)
{
    __DebugFunction();
    __DebugAssert(0 < m_strSailPlatformServicesIpAddress.size());
    __DebugAssert(0 < m_wSailPlatformServicesPortNumber);

    StructuredBuffer oRegistrationParameters;
    // Record the basic information
    oRegistrationParameters.PutString("name", m_strOrganizationalName);
    oRegistrationParameters.PutString("description", m_strOrganizationalDescription);
    // Now we need to know who the default administrator (i.e. initial user) is going to begin
    auto c_stlIterator = m_stlAdministrators.begin();
    if (m_stlAdministrators.end() != c_stlIterator)
    {
        StructuredBuffer oAdministrator(c_stlIterator->c_str());
        oRegistrationParameters.PutString("admin_name", oAdministrator.GetString("Name"));
        oRegistrationParameters.PutString("admin_job_title", oAdministrator.GetString("Title"));
        oRegistrationParameters.PutString("admin_email", oAdministrator.GetString("Email"));
        m_adminUserPassword = gsc_strDefaultPassword;
        if ( oAdministrator.IsElementPresent("Password", ANSI_CHARACTER_STRING_VALUE_TYPE) )
        {
            m_adminUserPassword = oAdministrator.GetString("Password");
        }
        oRegistrationParameters.PutString("admin_password", m_adminUserPassword);

    }
    // RegisterOrganization doesn't need you to be logged in at first.
    SailPlatformServicesSession oSailPlatformServicesSession(m_strSailPlatformServicesIpAddress, m_wSailPlatformServicesPortNumber);
    oSailPlatformServicesSession.RegisterOrganization(oRegistrationParameters);
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

        oRegistrationParameters.PutString("name", oUser.GetString("Name"));
        oRegistrationParameters.PutString("email", oUser.GetString("Email"));
        oRegistrationParameters.PutString("job_title", oUser.GetString("Title"));
        oRegistrationParameters.PutString("role", oUser.GetString("Role"));
        if ( oUser.IsElementPresent("Password", ANSI_CHARACTER_STRING_VALUE_TYPE) )
        {
            oRegistrationParameters.PutString("password", oUser.GetString("Password"));
        }
        else
        {
            oRegistrationParameters.PutString("password", gsc_strDefaultPassword);
        }
        oSailPlatformServicesSession.RegisterUser(oRegistrationParameters, this->GetOrganizationalIdentifier());
        c_stlIterator++;
    }
}

/********************************************************************************************/

void __thiscall Organization::RegisterDataFederations(
    std::unordered_map<std::string, Guid>& registeredFederations
)
{
    __DebugFunction();
    __DebugAssert(0 < m_strSailPlatformServicesIpAddress.size());
    __DebugAssert(0 < m_wSailPlatformServicesPortNumber);

    // Start a new session with SAIL Platform Services using the default administrator
    SailPlatformServicesSession oSailPlatformServicesSession(m_strSailPlatformServicesIpAddress, m_wSailPlatformServicesPortNumber);
    this->Login(oSailPlatformServicesSession);
    // Now that we have skipped the first entry, let's process all of the additional entries
    // Basically, we are adding new users with admin access rights
    std::unordered_set<std::string>::const_iterator c_stlIterator = m_stlDataFederations.begin();

    for ( auto federation : m_stlDataFederations )
    {
        StructuredBuffer oFederation(federation.c_str());

        StructuredBuffer oRegistrationParameters;

        oRegistrationParameters.PutString("name", oFederation.GetString("DataFederationName"));
        oRegistrationParameters.PutString("description", oFederation.GetString("DataFederationDescription"));

        std::string strFederationIdentifier = oSailPlatformServicesSession.RegisterDataFederation(oRegistrationParameters);
        if ( m_stlDataFederationIdentifiers.find(oFederation.GetString("DataFederationName")) == m_stlDataFederationIdentifiers.end())
        {
            m_stlDataFederationIdentifiers[oFederation.GetString("DataFederationName")] = strFederationIdentifier;
            std::cout << "Registered Federation \"" << oFederation.GetString("DataFederationName") << "\" which was given identifier " << strFederationIdentifier << std::endl;
            registeredFederations[oFederation.GetString("DataFederationName")] = strFederationIdentifier;
        }
        else
        {
            std::cout << "Federation " << oFederation.GetString("DataFederationName") << " already registered, not replacing identifier" << std::endl;
        }
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
    // Now that we have skipped the first entry, let's process all of the additional entries
    // Basically, we are adding new users with admin access rights
    std::unordered_set<std::string>::const_iterator c_stlIterator = m_stlDatasets.begin();
    while (m_stlDatasets.end() != c_stlIterator)
    {
        StructuredBuffer oDataset(c_stlIterator->c_str());
        StructuredBuffer oRegistrationParameters;

        oRegistrationParameters.PutString("name", oDataset.GetString("Title"));
        oRegistrationParameters.PutString("description", oDataset.GetString("Description"));
        oRegistrationParameters.PutString("tags", oDataset.GetString("Tags"));
        oRegistrationParameters.PutString("version", "0.0.1");

        std::string strDatasetIdentifier = oSailPlatformServicesSession.RegisterDataset(oRegistrationParameters);
        // Make sure the register the dataset identifier that is returned
        m_strDatasetIdentifiers[oDataset.GetString("Title")] = strDatasetIdentifier;
        // Move on to the next item
        c_stlIterator++;

        std::cout << "Registered dataset " << oDataset.GetString("Title") << " which was given identifier " << strDatasetIdentifier << std::endl;
    }
}

/********************************************************************************************/

void __thiscall Organization::RegisterDatasetVersions(void)
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
    std::unordered_map<Qword, std::string>::const_iterator c_stlIterator = m_strDatasetVersionInformationByFilename.begin();
    while (m_strDatasetVersionInformationByFilename.end() != c_stlIterator)
    {
        // Load the serialized dataset information into a StructuredBuffer in order to access it
        StructuredBuffer oDatasetVersionInformation(c_stlIterator->second.c_str());
        std::string strDatasetVersionFile = oDatasetVersionInformation.GetString("File");
        if (false == std::filesystem::exists(strDatasetVersionFile))
        {
            std::cout << "ERROR: DatasetVersion file not found (" << strDatasetVersionFile << ")" << std::endl;
        }
        else
        {
            // Load an existing dataset. This dataset will be modified during registration, hence
            // the reason why a DatassetReInitializer class was created, which wraps the
            // shared DatasetVersion class that is designed as an accessor only
            DatasetVersionReInitializer oDatasetVersionReInitializer(oDatasetVersionInformation.GetString("File"));
            // Now we start resetting some of the values in the dataset to reflect what is about to be
            // registered.
            // Create a new identifier
            // oDatasetVersionReInitializer.SetDatasetVersionIdentifier(Guid(eDatasetVersion));
            // Make sure the corporate identifier is updated
            oDatasetVersionReInitializer.SetCorporateIdentifier(Guid(oBasicUserInformation.GetStructuredBuffer("organization").GetString("id")));
            // Reset the publish date
            oDatasetVersionReInitializer.ResetUtcEpochPublishDate();
            // If a new Title is provided in the JSON, update the title of the dataset
            if (true == oDatasetVersionInformation.IsElementPresent("Name", ANSI_CHARACTER_STRING_VALUE_TYPE))
            {
                oDatasetVersionReInitializer.SetDatasetVersionName(oDatasetVersionInformation.GetString("Name"));
            }
            // If a new Description is provided in the JSON, update the description of the dataset
            if (true == oDatasetVersionInformation.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE))
            {
                oDatasetVersionReInitializer.SetDatasetVersionDescription(oDatasetVersionInformation.GetString("Description"));
            }
            // If a new Tags are provided in the JSON, update the tags of the dataset
            if (true == oDatasetVersionInformation.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE))
            {
                oDatasetVersionReInitializer.SetDatasetVersionKeywords(oDatasetVersionInformation.GetString("Tags"));
            }
            // If the new dataset has a dataset assigned to it
            if (true == oDatasetVersionInformation.IsElementPresent("Dataset", ANSI_CHARACTER_STRING_VALUE_TYPE))
            {
                oDatasetVersionReInitializer.SetDataset(this->GetDatasetIdentifier(oDatasetVersionInformation.GetString("Dataset")));
            }
            else
            {
                // If it doesn't have a dataset assigned, make sure the updated dataset
                // doesn't have one
                // oDatasetVersionReInitializer.RemoveDataset();
            }
            // Now we register the dataset using the updated information
            StructuredBuffer oDatasetVersionMetadata(oDatasetVersionReInitializer.GetSerializedDatasetVersionMetadata());
            oSailPlatformServicesSession.RegisterDatasetVersion(oDatasetVersionReInitializer.GetDatasetVersionIdentifier(), oDatasetVersionMetadata);

            // If we get here, the dataset was successfully registered. As such, let's persist
            // the dataset changes to file
            oDatasetVersionReInitializer.SaveDatasetVersionUpdates();
        }

        // If we get here, then the registration process has worked. Let's
        c_stlIterator++;
    }
}

/********************************************************************************************/

void __thiscall Organization::RegisterFederationDataSubmitters(
    _in const std::string & c_strSailPlatformServicesIpAddress,
    _in Word wSailPlatformServicesPortNumber,
    const std::unordered_map<std::string, Organization *>& organizationList
    ) throw()
{
    StructuredBuffer oRegistrationParameters;
    SailPlatformServicesSession oSailPlatformServicesSession(c_strSailPlatformServicesIpAddress, wSailPlatformServicesPortNumber);
    this->Login(oSailPlatformServicesSession);

    for ( auto federation : m_stlDataFederations )
    {
        StructuredBuffer oFederation(federation.c_str());
        if ( oFederation.IsElementPresent("DataSubmitters", INDEXED_BUFFER_VALUE_TYPE) )
        {
            StructuredBuffer oDataSubmitters{oFederation.GetStructuredBuffer("DataSubmitters")};
            if (true == oDataSubmitters.IsElementPresent("__IsArray__", BOOLEAN_VALUE_TYPE))
            {
                oDataSubmitters.RemoveElement("__IsArray__");
            }
            for ( const auto organizationIndex : oDataSubmitters.GetNamesOfElements())
            {
                auto organizationName = oDataSubmitters.GetString(organizationIndex.c_str());
                auto orgInformation = organizationList.find(organizationName);
                if ( organizationList.end() != orgInformation )
                {
                    std::cout << "Registering Data Submitter \"" << organizationName << "\" for Federation \"" << oFederation.GetString("DataFederationName") << "\"" << std::endl;
                    Guid federationIdentifier = m_stlDataFederationIdentifiers[oFederation.GetString("DataFederationName")];
                    Guid organizationIdentifier = orgInformation->second->GetOrganizationalIdentifier();

                    oSailPlatformServicesSession.RegisterDataFederationDataSubmitter(federationIdentifier, organizationIdentifier);
                }
                else
                {
                    std::cout << "Failed to find org identifier " <<  organizationName << std::endl;
                }
            }
        }
    };
}

/********************************************************************************************/

void __thiscall Organization::RegisterFederationResearchers(
    _in const std::string & c_strSailPlatformServicesIpAddress,
    _in Word wSailPlatformServicesPortNumber,
    const std::unordered_map<std::string, Organization *>& organizationList
    ) throw()
{
    StructuredBuffer oRegistrationParameters;
    SailPlatformServicesSession oSailPlatformServicesSession(c_strSailPlatformServicesIpAddress, wSailPlatformServicesPortNumber);
    this->Login(oSailPlatformServicesSession);

    for ( auto federation : m_stlDataFederations )
    {
        StructuredBuffer oFederation(federation.c_str());
        if ( oFederation.IsElementPresent("Researchers", INDEXED_BUFFER_VALUE_TYPE) )
        {
            StructuredBuffer oResearchers{oFederation.GetStructuredBuffer("Researchers")};
            if (true == oResearchers.IsElementPresent("__IsArray__", BOOLEAN_VALUE_TYPE))
            {
                oResearchers.RemoveElement("__IsArray__");
            }
            for ( const auto organizationIndex : oResearchers.GetNamesOfElements())
            {
                auto organizationName = oResearchers.GetString(organizationIndex.c_str());
                auto orgInformation = organizationList.find(organizationName);
                if ( organizationList.end() != orgInformation )
                {
                    std::cout << "Registering Researcher \"" << organizationName << "\" for Federation \"" << oFederation.GetString("DataFederationName") << "\"" << std::endl;
                    Guid federationIdentifier = m_stlDataFederationIdentifiers[oFederation.GetString("DataFederationName")];
                    Guid organizationIdentifier = orgInformation->second->GetOrganizationalIdentifier();

                    oSailPlatformServicesSession.RegisterDataFederationResearcher(federationIdentifier, organizationIdentifier);
                }
                else
                {
                    std::cout << "Failed to find org identifier " <<  organizationName << std::endl;
                }
            }
        }
    };
}

/********************************************************************************************/

void Organization::RegisterDatasetsToFederations(
    _in const std::string & c_strSailPlatformServicesIpAddress,
    _in Word wSailPlatformServicesPortNumber,
    const std::unordered_map<std::string, Guid>& federationList
    ) throw()
{

    StructuredBuffer oRegistrationParameters;
    SailPlatformServicesSession oSailPlatformServicesSession(c_strSailPlatformServicesIpAddress, wSailPlatformServicesPortNumber);
    this->Login(oSailPlatformServicesSession);

    for ( auto dataset : m_stlDatasets )
    {
        StructuredBuffer oDataset(dataset.c_str());
        if ( oDataset.IsElementPresent("Federation", ANSI_CHARACTER_STRING_VALUE_TYPE) )
        {
            std::string federationName = oDataset.GetString("Federation");
            auto federationItr = federationList.find(federationName);
            if ( federationList.end() != federationItr )
            {
                std::cout << "Registering Dataset \"" << oDataset.GetString("Title") << "\" for Federation \"" << federationName << "\"" << std::endl;
                Guid federationIdentifier = federationItr->second;
                Guid datasetIdentifier = m_strDatasetIdentifiers[oDataset.GetString("Title")];

                oSailPlatformServicesSession.RegisterDataFederationDataset(federationIdentifier, datasetIdentifier);
            }
            else
            {
                std::cout << "Failed to find dataset identifier " <<  oDataset.GetString("Title") << std::endl;
            }
        }
    };
}
