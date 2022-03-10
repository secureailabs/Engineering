/*********************************************************************************************
 *
 * @file StructuredBufferHelperFunctions.cpp
 * @author David Gascon
 * @date 14 Mar 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/


#include <StructuredBufferHelperFunctions.h>

/********************************************************************************************
 *
 * @function ConvertIdentifierListToStructuredBuffer
 * @brief Convert this identifier list to a StructuredBuffer
 * @return A StructuredBuffer representing this identifier list
 *
 ********************************************************************************************/
StructuredBuffer ConvertIdentifierListToStructuredBuffer(
    _in const std::list<Guid>& c_oIdentifierList
    )
{
    StructuredBuffer oGuidListStructuredBuffer;
    unsigned int unListIdx{0};
    for ( auto oIdentifier : c_oIdentifierList )
    {
        oGuidListStructuredBuffer.PutGuid(std::to_string(unListIdx).c_str(), oIdentifier);
        ++unListIdx;
    }
    return oGuidListStructuredBuffer;
}
