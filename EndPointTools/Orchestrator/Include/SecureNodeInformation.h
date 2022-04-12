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

struct HostedDatasetInformation
{
    Guid oDatsetGuid{};
    unsigned int unUsageCount{0};
};

struct SecureNodeInformation
{
    VirtualMachineState eProvisionStatus{VirtualMachineState::eStarting};
    std::string strDigitalContractGUID{""};
    std::string strRemoteIpAddress{""};
    std::string strVMGUID{""};
    HostedDatasetInformation oHostedDataset{};
    std::string strProvisionMessage{""};
};
