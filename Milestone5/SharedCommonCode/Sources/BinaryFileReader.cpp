/*********************************************************************************************
 *
 * @file BinaryFileReader.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "BinaryFileHandlers.h"
#include "DebugLibrary.h"
#include "Exceptions.h"

#include <limits>

/********************************************************************************************/

BinaryFileReader::BinaryFileReader(
    _in const std::string & c_strTargetFilename
    )
{
    __DebugFunction();
    
    m_strFilename = c_strTargetFilename;
    this->Load();
}

/********************************************************************************************/

BinaryFileReader::BinaryFileReader(
    _in const char * c_szTargetFilename
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szTargetFilename);
    
    m_strFilename = c_szTargetFilename;
    this->Load();
}

/********************************************************************************************/

BinaryFileReader::~BinaryFileReader(void)
{
    __DebugFunction();
    
    m_stlFileStream.close();
}

/********************************************************************************************/

std::string __thiscall BinaryFileReader::GetFilename(void) const throw()
{
    __DebugFunction();
    
    return m_strFilename;
}

/********************************************************************************************/

uint64_t __thiscall BinaryFileReader::GetSizeInBytes(void) const throw()
{
    __DebugFunction();
    
    return m_un64SizeInBytes;
}

/********************************************************************************************/

uint64_t __thiscall BinaryFileReader::GetFilePointer(void) const throw()
{
    __DebugFunction();
    
    const auto stlCurrentPosition = m_stlFileStream.tellg();
    
    return (stlCurrentPosition - m_stlStartingPosition);
}

/********************************************************************************************/

void __thiscall BinaryFileReader::Seek(
    _in FileOffsetType eOffsetType,
    _in uint64_t un64OffsetInBytes
    )
{
    __DebugFunction();
    
    std::ios_base::seekdir stlSeekDirection;
    
    if (eFromBeginningOfFile == eOffsetType)
    {
        stlSeekDirection = std::ios_base::beg;
    }
    else if (eFromCurrentPositionInFile == eOffsetType)
    {
        stlSeekDirection = std::ios_base::cur;
    }
    else
    {
        stlSeekDirection = std::ios_base::end;
    }
    
    // Change the file pointer
    m_stlFileStream.seekg(un64OffsetInBytes, stlSeekDirection);
}

/********************************************************************************************/
    
void __thiscall BinaryFileReader::Read(
    _in void * pDestinationBuffer,
    _in uint64_t un64NumberOfBytesToRead
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != pDestinationBuffer);
    
    if (0 < un64NumberOfBytesToRead)
    {
        m_stlFileStream.read((char *) pDestinationBuffer, un64NumberOfBytesToRead);
    }
}

/********************************************************************************************/

std::vector<Byte> __thiscall BinaryFileReader::Read(
    _in uint64_t un64NumberOfBytesToRead
    )
{
    __DebugFunction();
    
    std::vector<Byte> stlDestinationBuffer;
    
    if (0 < un64NumberOfBytesToRead)
    {
        stlDestinationBuffer.resize(un64NumberOfBytesToRead);
        this->Read((void *) stlDestinationBuffer.data(), un64NumberOfBytesToRead);
    }
    
    return stlDestinationBuffer;
}

/********************************************************************************************/

void __thiscall BinaryFileReader::Load(void)
{
    __DebugFunction();
    __DebugAssert(0 < m_strFilename.size());
    
    m_stlFileStream.open(m_strFilename.c_str(), (std::ifstream::in | std::ifstream::binary));
    // Record the starting position.
    m_stlFileStream.seekg(0, std::ios::beg);
    m_stlStartingPosition = m_stlFileStream.tellg();
    // Determine the file size
    m_stlFileStream.seekg(0, std::ios::end);
    const auto stlEndingPosition = m_stlFileStream.tellg();
    m_un64SizeInBytes = (stlEndingPosition - m_stlStartingPosition);
    // Reset the file pointer at the starting
    m_stlFileStream.seekg(0, std::ios::beg);
}