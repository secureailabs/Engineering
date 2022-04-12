/*********************************************************************************************
 *
 * @file BinaryFileWriter.cpp
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

BinaryFileWriter::BinaryFileWriter(
    _in const std::string & c_strTargetFilename
    )
{
    __DebugFunction();

    m_strFilename = c_strTargetFilename;
    this->Load();
}

/********************************************************************************************/

BinaryFileWriter::BinaryFileWriter(
    _in const char * c_szTargetFilename
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szTargetFilename);

    m_strFilename = c_szTargetFilename;
    this->Load();
}

/********************************************************************************************/

BinaryFileWriter::~BinaryFileWriter(void)
{
    __DebugFunction();

    m_stlFileStream.close();
}

/********************************************************************************************/

std::string __thiscall BinaryFileWriter::GetFilename(void) const throw()
{
    __DebugFunction();

    return m_strFilename;
}

/********************************************************************************************/

uint64_t __thiscall BinaryFileWriter::GetSizeInBytes(void) const throw()
{
    __DebugFunction();

    return m_un64SizeInBytes;
}

/********************************************************************************************/

uint64_t __thiscall BinaryFileWriter::GetFilePointer(void) const throw()
{
    __DebugFunction();

    const auto stlCurrentPosition = m_stlFileStream.tellp();

    return (stlCurrentPosition - m_stlStartingPosition);
}

/********************************************************************************************/

void __thiscall BinaryFileWriter::Seek(
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
    m_stlFileStream.seekp(un64OffsetInBytes, stlSeekDirection);
}

/********************************************************************************************/
    
void __thiscall BinaryFileWriter::Write(
    _in const void * c_pSourceBuffer,
    _in uint64_t un64NumberOfBytesToWrite
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_pSourceBuffer);

    if (0 < un64NumberOfBytesToWrite)
    {
        m_stlFileStream.write((const char *) c_pSourceBuffer, un64NumberOfBytesToWrite);
    }
}

/********************************************************************************************/

void __thiscall BinaryFileWriter::Write(
    _in const std::vector<Byte> & c_stlSourceBuffer
    )
{
    __DebugFunction();

    if (0 < c_stlSourceBuffer.size())
    {
        m_stlFileStream.write((const char *) c_stlSourceBuffer.data(), c_stlSourceBuffer.size());
    }
}

/********************************************************************************************/

void __thiscall BinaryFileWriter::Load(void)
{
    __DebugFunction();
    __DebugAssert(0 < m_strFilename.size());

    m_stlFileStream.open(m_strFilename.c_str(), (std::ofstream::out | std::ofstream::binary));
    // Record the starting position.
    m_stlFileStream.seekp(0, std::ios::beg);
    m_stlStartingPosition = m_stlFileStream.tellp();
    // Determine the file size
    m_stlFileStream.seekp(0, std::ios::end);
    const auto stlEndingPosition = m_stlFileStream.tellp();
    m_un64SizeInBytes = (stlEndingPosition - m_stlStartingPosition);
    // Reset the file pointer at the starting
    m_stlFileStream.seekp(0, std::ios::beg);
}
