/*********************************************************************************************
 *
 * @file OrchestratorTypes.cpp
 * @author David Gascon
 * @date 20 Jan 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Types related for the orchestrator talking to the job engine
 *
 ********************************************************************************************/

#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "OrchestratorTypes.h"


/********************************************************************************************
 *
 * @function IsJobOutputParameter
 * @brief Determine if a string holds a job output parameter in the form: JobGUID.OutputParameterGuid
 * @param[in] std::string - The ID for the parameter pull in form: "JobGUID.OutputParameterGuid"
 * @return True if this is a JobOutputParameter, false otherwise
 ********************************************************************************************/
bool IsJobOutputParameter(
    _in const std::string& c_strParameter
)
{
    bool fIsJobParameter{false};

    try
    {
        size_t unFirstPeriod = c_strParameter.find_first_of(".");
        size_t unLastPeriod = c_strParameter.find_last_of(".");
        if ( std::string::npos != unFirstPeriod && (std::string::npos != unLastPeriod) )
        {
            const std::string& c_strJobId = c_strParameter.substr(0, unFirstPeriod);
            const std::string& c_strParameterId = c_strParameter.substr(unFirstPeriod + 1, std::string::npos);

            // If these two values are no GUIDs, these calls with  throw
            Guid oJobGuid(c_strJobId);
            Guid oParameterGuid(c_strParameterId);

            fIsJobParameter = (eJobIdentifier == oJobGuid.GetObjectType()) && ( eOutputParameterIdentifier == oParameterGuid.GetObjectType());
        }
    }
    catch(const BaseException& oBaseException )
    {
        ::RegisterBaseException(oBaseException, __func__, __FILE__, __LINE__);
        fIsJobParameter = false;
    }
    catch( ... )
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        fIsJobParameter = false;
    }

    return fIsJobParameter;
}

