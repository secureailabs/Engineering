/*********************************************************************************************
 *
 * @file TextFileReader.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "TextFileHandlers.h"

#include <filesystem>

/********************************************************************************************/

TextFileReader::TextFileReader(
    _in const std::string & c_strTargetFilename
    )
{
    __DebugFunction();
    
    m_strFilename = c_strTargetFilename;
    this->Load();
}

/********************************************************************************************/

TextFileReader::TextFileReader(
    _in const char * c_szTargetFilename
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szTargetFilename);
    
    m_strFilename = c_szTargetFilename;
    this->Load();
}

/********************************************************************************************/

TextFileReader::~TextFileReader(void)
{
    __DebugFunction();
    
    m_stlFileStream.close();
}

/********************************************************************************************/

std::string __thiscall TextFileReader::GetFilename(void) const throw()
{
    __DebugFunction();
    
    return m_strFilename;
}

/********************************************************************************************/

uint64_t __thiscall TextFileReader::GetSizeInBytes(void) const throw()
{
    __DebugFunction();
    
    return m_un64SizeInBytes;
}

/********************************************************************************************/

bool __thiscall TextFileReader::EndOfFileReached(void) const throw()
{
    __DebugFunction();
    
    return m_stlFileStream.eof();
}

/********************************************************************************************/

std::string __thiscall TextFileReader::Read(void)
{
    __DebugFunction();
    
    std::string strLineOfText;
    std::getline(m_stlFileStream, strLineOfText);
    
    return strLineOfText;
}

/********************************************************************************************/

void __thiscall TextFileReader::Load(void)
{
    __DebugFunction();
    __DebugAssert(0 < m_strFilename.size());
    
    // Check to make sure the file exists
    _ThrowBaseExceptionIf((false == std::filesystem::exists(m_strFilename)), "ERROR: File %s not found", m_strFilename.c_str());
    // Open the target file
    m_stlFileStream.open(m_strFilename.c_str(), std::ifstream::in);
    // Record the starting position.
    m_stlFileStream.seekg(0, std::ios::beg);
    const auto stlStartingPosition = m_stlFileStream.tellg();
    // Determine the file size
    m_stlFileStream.seekg(0, std::ios::end);
    const auto stlEndingPosition = m_stlFileStream.tellg();
    m_un64SizeInBytes = (stlEndingPosition - stlStartingPosition);
    // Reset the file pointer at the starting
    m_stlFileStream.seekg(0, std::ios::beg);    
}