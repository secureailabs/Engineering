/*********************************************************************************************
 *
 * @file InitializationVector.h
 * @author Prawal Gangwar
 * @date 12 January 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "DebugLibrary.h"
#include "Exceptions.h"
#include "StructuredBuffer.h"

#include <vector>
#include <string>

extern std::string __stdcall GetInitializationValue(
    _in const std::string & c_strParameter
);

extern StructuredBuffer __stdcall GetInitialziationStructuredBuffer(
    _in const std::string & c_strStructuredBufferName
    );

extern bool __stdcall IsInitializationValuePresent(
    _in const std::string & c_strStructuredBufferName
    );
