/*********************************************************************************************
 *
 * @file EntityTypes.cpp
 * @author David Gascon
 * @date 17 Dec 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Helper functions for enum translations
 *
 ********************************************************************************************/

#include "DebugLibrary.h"
#include "EntityTypes.h"
#include "Exceptions.h"

/********************************************************************************************
 *
 * @function ProvisioningStatusFromFloat
 * @brief Helper function to translate from a float to an enum, or throw an exception if the
 *        given value can't be translated
 * @param [in] float64_t - The float value to convert
 * @return DigitalContractProvisiongStatus - The enum value
 *
 ********************************************************************************************/
__stdcall DigitalContractProvisiongStatus ProvisioningStatusFromFloat(
    _in float64_t fValue
    )
{
    __DebugFunction();

    DigitalContractProvisiongStatus eReturnValue;

    if ( 1.0 == fValue )
    {
        eReturnValue = DigitalContractProvisiongStatus::eProvisioning;
    }
    else if ( 2.0 == fValue )
    {
        eReturnValue = DigitalContractProvisiongStatus::eReady;
    }
    else if ( 3.0 == fValue )
    {
        eReturnValue = DigitalContractProvisiongStatus::eUnprovisioned;
    }
    else if (4.0 == fValue )
    {
        eReturnValue = DigitalContractProvisiongStatus::eProvisioningFailed;
    }
    else
    {
        _ThrowBaseException("Unknown provisioning value", nullptr);
    }
    return eReturnValue;
}

/********************************************************************************************
 *
 * @function ProvisionStatusToString
 * @brief Helper function to translate from an enum to string
 * @param [in] DigitalContractProvisiongStatus - The enum to convert
 * @return std::string - The string value for the enum, "" if it can't be found
 *
 ********************************************************************************************/
__stdcall std::string ProvisionStatusToString(
    _in DigitalContractProvisiongStatus eProvisionStatus
    )
{
    switch (eProvisionStatus)
    {
        case DigitalContractProvisiongStatus::eReady
        :
            return "Ready";
        case DigitalContractProvisiongStatus::eProvisioning
        :
            return "Provisioning";
        case DigitalContractProvisiongStatus::eProvisioningFailed
        :
            return "Failed";
        case DigitalContractProvisiongStatus::eUnprovisioned
        :
            return "Not Provisioned";
    }
    return "";
}
