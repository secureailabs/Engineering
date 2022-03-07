
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
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "JobOutputParameter.h"

/********************************************************************************************
 *
 * @function ToString
 * @class JobOutputParameter
 * @brief Produce a string representation of a JobOutputParameter
 * @return std::string - The ID for the parameter pull in form: "JobGUID.OutputParameterGuid"
 ********************************************************************************************/
std::string JobOutputParameter::ToString() const
{
    return m_strJobIdentifier.ToString(eRaw) + "." + m_strOutputIdentifier.ToString(eRaw);
}


/********************************************************************************************
 *
 * @function ParseStringToJobOutput
 * @brief Parse out an output parameter identifier to its two guids: JobGUID.OutputParamGuid
 *        Throws an exception on error
 * @param[in] std::string - The ID for the parameter pull in form: "JobGUID.OutputParameterGuid"
 * @return std::pair<Guid, Guid> - The Guids of the Job and Output Param
 ********************************************************************************************/
JobOutputParameter ParseStringToJobOutput(
    _in const std::string& c_strJobOutputId
)
{
    size_t unFirstPeriod = c_strJobOutputId.find_first_of(".");
    size_t unLastPeriod = c_strJobOutputId.find_last_of(".");
    JobOutputParameter oJobOutputParameter;
    _ThrowBaseExceptionIf( (std::string::npos == unFirstPeriod) || (unFirstPeriod != unLastPeriod),
        "Invalid parameter specifier", nullptr);
    oJobOutputParameter.m_strJobIdentifier = Guid(c_strJobOutputId.substr(0, unFirstPeriod));
    oJobOutputParameter.m_strOutputIdentifier = Guid(c_strJobOutputId.substr(unFirstPeriod + 1, std::string::npos));

    return oJobOutputParameter;
}
