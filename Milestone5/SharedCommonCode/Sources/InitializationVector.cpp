/*********************************************************************************************
 *
 * @file InitializationVector.cpp
 * @author Prawal Gangwar
 * @date 12 January 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "DebugLibrary.h"
#include "Exceptions.h"
#include "InitializationVector.h"
#include "StructuredBuffer.h"
#include "JsonValue.h"
#include "FileUtils.h"

#include <vector>
#include <string>

/********************************************************************************************
 *
 * @function GetInitializationValue
 * @brief Get the initialization value for the given parameter
 * @param[in] c_strParameter Key of the value to be retrieved
 * @throw BaseException if element not found
 * @returns Valueof the required parameter
 *
 ********************************************************************************************/

std::string __stdcall GetInitializationValue(
    _in const std::string & c_strParameter
)
{
    __DebugFunction();
    _ThrowBaseExceptionIf((0 == c_strParameter.length()), "Parameter is empty", nullptr);

    std::string strParameterValue;

    // Declare it as a static memeber so that it is initialized only once.
    static StructuredBuffer oInitializationVector;

    // Initialize it only once if it is not already initialized.
    if (true == oInitializationVector.GetNamesOfElements().empty())
    {
        std::cout << "InitializationVector not loaded. Initializing it now." << std::endl;
        std::string strInitializationVectorJson = ::ReadFileAsString("InitializationVector.json");
        _ThrowBaseExceptionIf((0 == strInitializationVectorJson.length()), "InitializationVector.json is empty", nullptr);
        oInitializationVector = JsonValue::ParseDataToStructuredBuffer(strInitializationVectorJson.c_str());
    }

    // Get the value of the parameter from the initialization vector.
    strParameterValue = oInitializationVector.GetString(c_strParameter.c_str());

    return strParameterValue;
}
