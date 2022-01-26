
/*********************************************************************************************
 *
 * @file TableInformation.h
 * @author David Gascon
 * @date 19 Jan, 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "StructuredBuffer.h"
#include <string>

struct TableInformation
{
    TableInformation(
        _in const std::string& strParentDataset,
        _in const StructuredBuffer& oInformation
        ) :
        m_strParentDataset{strParentDataset},
        m_oInformation{oInformation}
    {

    }

    TableInformation() = delete;

    std::string m_strParentDataset;
    StructuredBuffer m_oInformation;
};
