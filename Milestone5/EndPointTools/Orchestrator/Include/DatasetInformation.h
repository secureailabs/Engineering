/*********************************************************************************************
 *
 * @file DatasetInformation.h
 * @author David Gascon
 * @date 1 Feb 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once
#include "Guid.h"
#include "StructuredBuffer.h"
#include <list>
#include <string>

struct DatasetInformation
{
    Guid m_oDatsetGuid{};
    unsigned int m_unUsageCount{0};
    StructuredBuffer m_oMetadata{};
    std::list<Guid> m_stlSecureNodesHosting{};
};
