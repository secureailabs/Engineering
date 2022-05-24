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
    std::string strDatsetGuid{""};
    unsigned int unUsageCount{0};
};

struct SecureNodeInformation
{
    std::string strProvisionStatus{""};
    std::string strDigitalContractGUID{""};
    std::string strRemoteIpAddress{""};
    std::string strVMGUID{""};
    HostedDatasetInformation oHostedDataset{};
    std::string strProvisionMessage{""};
};
