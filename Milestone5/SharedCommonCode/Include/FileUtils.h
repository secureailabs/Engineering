/*********************************************************************************************
 *
 * @file FileUtils.h
 * @author Prawal Gangwar
 * @date 16 July 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "CoreTypes.h"

#include <vector>
#include <string>

extern std::vector<Byte> __stdcall ReadFileAsByteBuffer(
    _in const std::string & c_strFileName
    );

extern std::string __stdcall ReadFileAsString(
    _in const std::string & c_strFileName
    );

extern void __stdcall WriteBytesAsFile(
    _in const std::string & c_strFileName,
    _in const std::vector<Byte> & c_stlFileData
    );

extern void __stdcall WriteStringAsFile(
    _in const std::string & c_strFileName,
    _in const std::string & c_strFileData
    );
