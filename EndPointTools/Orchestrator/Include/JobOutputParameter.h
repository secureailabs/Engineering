/*********************************************************************************************
 *
 * @file JobOutputParameter.cpp
 * @author David Gascon
 * @date 08 March 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Functions for dealing with job output parameters
 *
 ********************************************************************************************/
#include <string>
#include "Guid.h"

struct JobOutputParameter
{
    Guid m_strJobIdentifier;
    Guid m_strOutputIdentifier;

    std::string ToString() const;
};

bool IsJobOutputParameter(
    _in const std::string& c_strParameter
    );

JobOutputParameter ParseStringToJobOutput(
    _in const std::string& c_strJobOutputId
    );

