/*********************************************************************************************
 *
 * @file DigitalContract.cpp
 * @author Luis Miguel Huapaya
 * @date 23 March 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "DatasetVersion.h"
#include "DebugLibrary.h"
#include "DigitalContract.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "SailPlatformServicesSession.h"

#include <filesystem>
#include <iostream>

static const std::string gsc_strDefaultPassword{"SailPassword@123"};

/********************************************************************************************/

DigitalContract::DigitalContract(
    _in const Organization * c_poDataOwnerOrganization,
    _in const Organization * c_poResearchOrganization,
    _in const StructuredBuffer & c_oDigitalContractParameters
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_poDataOwnerOrganization);
    __DebugAssert(nullptr != c_poResearchOrganization);

    // Extract all of the basic parameters
    m_strDataOwnerAdministratorUsername = c_poDataOwnerOrganization->GetAdminUsername();
    m_strResearchAdministratorUsername = c_poResearchOrganization->GetAdminUsername();
    m_strDataOwnerOrganizationIdentifier = c_poDataOwnerOrganization->GetOrganizationalIdentifier();
    m_strResearchOrganizationIdentifier = c_poResearchOrganization->GetOrganizationalIdentifier();
    m_strTitle = c_oDigitalContractParameters.GetString("Name");
    m_strDescription = c_oDigitalContractParameters.GetString("Description");
    m_strVersionNumber = "1.0.0";
    m_strLegalAgreement = c_oDigitalContractParameters.GetString("LegalAgreement");
    m_unSubscriptionDays = (unsigned int) c_oDigitalContractParameters.GetFloat64("SubscriptionDays");
    // Now we try and figure out whether we are dealing with a dataset or dataset family. What we need
    // is an identifier
    if (true == c_oDigitalContractParameters.IsElementPresent("Dataset", ANSI_CHARACTER_STRING_VALUE_TYPE))
    {
        // We are dealing with a dataset. In the JSON specification, this will be the name of a dataset file
        DatasetVersion oDatasetVersion(c_oDigitalContractParameters.GetString("Dataset").c_str());
        m_strAssociatedIdentifier = oDatasetVersion.GetDatasetVersionIdentifier();
    }
    else if (true == c_oDigitalContractParameters.IsElementPresent("DatasetFamily", ANSI_CHARACTER_STRING_VALUE_TYPE))
    {
        // We are dealing with a dataset family. We need to get the identifier of the dataset family from
        // the data owner organization
        m_strAssociatedIdentifier = c_poDataOwnerOrganization->GetDatasetFamilyIdentifier(c_oDigitalContractParameters.GetString("DatasetFamily"));
    }
    else
    {
        _ThrowBaseException("ERROR: Digital Contract specification invalid. Missing dataset or dataset family specification", nullptr);
    }
}

/********************************************************************************************/

DigitalContract::~DigitalContract(void)
{
    __DebugFunction();
}

/********************************************************************************************/

bool __thiscall DigitalContract::Register(
    _in const std::string & c_strSailPlatformServicesIpAddress,
    _in Word wSailPlatformServicesPortNumber
    ) throw()
{
    __DebugFunction();

    bool fSuccess = false;

    try
    {
        SailPlatformServicesSession oSailPlatformServicesSession(c_strSailPlatformServicesIpAddress, wSailPlatformServicesPortNumber);

        // Execute the registration. This is a three step process
        // 1. Application (done by researcher)
        // 2. Approval (done by data owner)
        // 3. Activation (done by researcher)

        // Setup the application parameters
        StructuredBuffer oApplicationParameters;
        oApplicationParameters.PutString("name", m_strTitle);
        oApplicationParameters.PutString("description", m_strDescription);
        oApplicationParameters.PutString("version", m_strVersionNumber);
        oApplicationParameters.PutUnsignedInt64("subscription_days", m_unSubscriptionDays);
        oApplicationParameters.PutString("dataset_id", m_strAssociatedIdentifier);
        oApplicationParameters.PutString("legal_agreement", m_strLegalAgreement);

        // Login as researcher and execute step 1 of the digital contract application
        oSailPlatformServicesSession.Login(m_strResearchAdministratorUsername, gsc_strDefaultPassword);
        std::string strDigitalContractIdentifier = oSailPlatformServicesSession.ApplyForDigitalContract(oApplicationParameters);
        // Setup the approval parameters
        // Login as data owner and execute step 2 of the digital contract approval
        oSailPlatformServicesSession.Login(m_strDataOwnerAdministratorUsername, gsc_strDefaultPassword);
        oSailPlatformServicesSession.ApproveDigitalContract(strDigitalContractIdentifier);

        // Setup the activation parameters
        // Login as researcher and execute step 3 of the digital contract activation
        oSailPlatformServicesSession.Login(m_strResearchAdministratorUsername, gsc_strDefaultPassword);
        oSailPlatformServicesSession.ActivateDigitalContract(strDigitalContractIdentifier);

        // If we get here, we were successful
        fSuccess = true;
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

    return fSuccess;
}

/********************************************************************************************/

std::string __thiscall DigitalContract::GetContractName(void) const throw()
{
    __DebugFunction();

    return m_strTitle;
}
