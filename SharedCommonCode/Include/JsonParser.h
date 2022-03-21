/*********************************************************************************************
 *
 * @file JsonParser.h
 * @author Luis Miguel Huapaya
 * @date 08 Dec 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "CoreTypes.h"
#include "StructuredBuffer.h"

#include <string>

/// <summary>
/// 
/// </summary>
/// <param name="c_szJsonString"></param>
/// <returns></returns>
extern StructuredBuffer __stdcall ConvertJsonStringToStructuredBuffer(
    _in const char * c_szJsonString
    );

/// <summary>
/// 
/// </summary>
/// <param name="c_oStructuredBuffer"></param>
/// <returns></returns>
extern std::string __stdcall ConvertStructuredBufferToJson(
    _in const StructuredBuffer & c_oStructuredBuffer
    );
