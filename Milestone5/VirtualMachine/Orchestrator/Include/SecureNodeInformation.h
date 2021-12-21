/*********************************************************************************************
 *
 * @file SecureNodeInformation.h
 * @author David Gascon
 * @date 10 Jan 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once
#include <string>
#include "EntityTypes.h"

struct SecureNodeInformation
{
    DigitalContractProvisiongStatus eProvisionStatus{DigitalContractProvisiongStatus::eUnprovisioned};
    std::string strRemoteIpAddress{""};
    std::string strVMGUID{""};
    std::string strDatasetGUID{""};
};
