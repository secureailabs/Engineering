/*********************************************************************************************
 *
 * @file StructuredBufferHelperFunctions.h
 * @author David Gascon
 * @date 14 Mar 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/
#pragma once

#include <list>
#include <StructuredBuffer.h>

/********************************************************************************************/

StructuredBuffer ConvertIdentifierListToStructuredBuffer(
    _in const std::list<Guid>& c_oIdentifierList
    );
