/*********************************************************************************************
 *
 * @file Dataset.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "64BitHashes.h"
#include "BinaryFileHandlers.h"
#include "Dataset.h"
#include "DebugLibrary.h"
#include "Exceptions.h"

#include <iostream>

/********************************************************************************************/

Dataset::Dataset(
    _in const char * c_szFullFilename
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szFullFilename);

    BinaryFileReader oBinaryFileReader(c_szFullFilename);
    Qword qwMarker;
    oBinaryFileReader.Read((void *) &qwMarker, sizeof(qwMarker));
    _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != qwMarker), "Invalid marker value of 0x%08X%08X found at the beginning of the file", HIDWORD(qwMarker), LODWORD(qwMarker));
    unsigned int unSizeInBytesOfDatasetMetadata = 0;
    oBinaryFileReader.Read((void *) &unSizeInBytesOfDatasetMetadata, sizeof(unSizeInBytesOfDatasetMetadata));
    std::vector<Byte> stlBuffer = oBinaryFileReader.Read(unSizeInBytesOfDatasetMetadata);
    StructuredBuffer oDatasetMetadata(stlBuffer);
    // Now let's do a quick reality check and make sure the header is in good order
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Version", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Version is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("DatasetIdentifier", GUID_VALUE_TYPE)), "INVALID METADATA: DatasetIdentifier is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("PublisherIdentifier", GUID_VALUE_TYPE)), "INVALID METADATA: PublisherIdentifier is missing", nullptr);
    //_ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("DataFamilyIdentifier", GUID_VALUE_TYPE)), "INVALID METADATA: DataFamilyIdentifier is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Title is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Description is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Tags is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("EpochCreationTimeInSeconds", UINT64_VALUE_TYPE)), "INVALID METADATA: EpochCreationTimeInSeconds is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("TableCount", UINT32_VALUE_TYPE)), "INVALID METADATA: TableCount is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Tables", INDEXED_BUFFER_VALUE_TYPE)), "INVALID METADATA: Tables are missing", nullptr);
    // Track the cursor offset into the file. At this point, the current position should point to
    // the marker for the first table
    uint64_t un64FilePosition = oBinaryFileReader.GetFilePointer();
    oBinaryFileReader.Read((void *) &qwMarker, sizeof(qwMarker));
    _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != qwMarker), "Invalid marker value of 0x%08X%08X found at the beginning of the file", HIDWORD(qwMarker), LODWORD(qwMarker));
    do
    {
        // Read the UUID of the table
        stlBuffer = oBinaryFileReader.Read(16);
        __DebugAssert(16 == stlBuffer.size());
        Guid oTableIdentifier((const Byte *) stlBuffer.data());
        std::string strTableIdentifier = oTableIdentifier.ToString(eHyphensOnly);
        // Read the compressed size in bytes of the table data
        uint64_t un64CompressedSizeInBytes = 0;
        oBinaryFileReader.Read((void *) &un64CompressedSizeInBytes, sizeof(un64CompressedSizeInBytes));
        // Move the file cursor forward from the current position (1)
        oBinaryFileReader.Seek(eFromCurrentPositionInFile, un64CompressedSizeInBytes);
        uint64_t un64NewFilePosition = oBinaryFileReader.GetFilePointer();
        oBinaryFileReader.Read((void *) &qwMarker, sizeof(qwMarker));
        _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != qwMarker), "Invalid marker value of 0x%08X%08X found at the beginning of the file", HIDWORD(qwMarker), LODWORD(qwMarker));
        // Check to make sure the table identifier actually exists within the metadata
        StructuredBuffer oAllTables(oDatasetMetadata.GetStructuredBuffer("Tables"));
        _ThrowBaseExceptionIf((false == oAllTables.IsElementPresent(strTableIdentifier.c_str(), INDEXED_BUFFER_VALUE_TYPE)), "ERROR: Table identifier %s was found in the file, but not in the metadata.", strTableIdentifier.c_str());
        // Save this information
        Qword qwHashOfTableIdentifier = ::Get64BitHashOfNullTerminatedString(strTableIdentifier.c_str(), false);
        m_stlListOfTableIdentifiers.push_back(strTableIdentifier);
        m_stlListOfTableMarkerOffsets[qwHashOfTableIdentifier] = un64FilePosition;
        // Update the un64FilePosition to the latest value
        un64FilePosition = un64NewFilePosition;
    }
    while (oBinaryFileReader.GetFilePointer() < oBinaryFileReader.GetSizeInBytes());
    // Since everything went well, let's persist the dataset metadata
    m_oDatasetMetadata = oDatasetMetadata;
    m_strFilename = c_szFullFilename;
    m_fIsMetadataOnly = false;
}

/********************************************************************************************/

Dataset::Dataset(
    _in const std::vector<Byte> & c_stlSerializedMetadata
    )
{
    __DebugFunction();

    // De-serialized the incoming serialized data
    StructuredBuffer oDatasetMetadata(c_stlSerializedMetadata);
    // Now let's do a quick reality check and make sure the header is in good order
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Version", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Version is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("DatasetIdentifier", GUID_VALUE_TYPE)), "INVALID METADATA: DatasetIdentifier is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("PublisherIdentifier", GUID_VALUE_TYPE)), "INVALID METADATA: PublisherIdentifier is missing", nullptr);
    //_ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("DataFamilyIdentifier", GUID_VALUE_TYPE)), "INVALID METADATA: DataFamilyIdentifier is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Title is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Description is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Tags is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("EpochCreationTimeInSeconds", UINT64_VALUE_TYPE)), "INVALID METADATA: EpochCreationTimeInSeconds is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("TableCount", UINT32_VALUE_TYPE)), "INVALID METADATA: TableCount is missing", nullptr);        
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Tables", INDEXED_BUFFER_VALUE_TYPE)), "INVALID METADATA: Tables are missing", nullptr);
    // Let's extract the table identifiers from the metadata. This is different than the
    // constructor that loads from file, since in that case, we load from file and then
    // verify it exists in the metadata
    StructuredBuffer oAllTables(oDatasetMetadata.GetStructuredBuffer("Tables"));
    std::vector<std::string> stlListOfTables = oAllTables.GetNamesOfElements();
    for (std::string strTableIdentifier: stlListOfTables)
    {
        Qword qwHashOfTableIdentifier = ::Get64BitHashOfNullTerminatedString(strTableIdentifier.c_str(), false);
        m_stlListOfTableIdentifiers.push_back(strTableIdentifier);
        m_stlListOfTableMarkerOffsets[qwHashOfTableIdentifier] = 0xFFFFFFFFFFFFFFFF;
    }
    // Since everything went well, let's persist the dataset metadata
    m_oDatasetMetadata = oDatasetMetadata;
    m_fIsMetadataOnly = true;
}

/********************************************************************************************/

Dataset::~Dataset(void) throw()
{
    __DebugFunction();
}

/********************************************************************************************/

std::string __thiscall Dataset::GetDatasetIdentifier(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetMetadata.IsElementPresent("DatasetIdentifier", GUID_VALUE_TYPE));

    return m_oDatasetMetadata.GetGuid("DatasetIdentifier").ToString(eHyphensOnly);
}

/********************************************************************************************/

std::string __thiscall Dataset::GetDatasetFamilyIdentifier(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetMetadata.IsElementPresent("DataFamilyIdentifier", GUID_VALUE_TYPE));

    return m_oDatasetMetadata.GetGuid("DataFamilyIdentifier").ToString(eHyphensOnly);
}

/********************************************************************************************/

std::string __thiscall Dataset::GetPublisherIdentifier(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetMetadata.IsElementPresent("PublisherIdentifier", GUID_VALUE_TYPE));

    return m_oDatasetMetadata.GetGuid("PublisherIdentifier").ToString(eHyphensOnly);
}

/********************************************************************************************/

std::string __thiscall Dataset::GetTitle(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetMetadata.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oDatasetMetadata.GetString("Title");
}

/********************************************************************************************/

std::string __thiscall Dataset::GetDescription(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetMetadata.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oDatasetMetadata.GetString("Description");
}

/********************************************************************************************/

std::string __thiscall Dataset::GetTags(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetMetadata.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oDatasetMetadata.GetString("Tags");
}

/********************************************************************************************/

uint64_t __thiscall Dataset::GetEpochCreationTimeInSeconds(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetMetadata.IsElementPresent("EpochCreationTimeInSeconds", UINT64_VALUE_TYPE));

    return m_oDatasetMetadata.GetUnsignedInt64("EpochCreationTimeInSeconds");
}

/********************************************************************************************/

unsigned int __thiscall Dataset::GetTableCount(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetMetadata.IsElementPresent("TableCount", UINT32_VALUE_TYPE));

    return m_oDatasetMetadata.GetUnsignedInt32("TableCount");
}

/********************************************************************************************/

std::vector<std::string> __thiscall Dataset::GetTableIdentifiers(void) const throw()
{
    __DebugFunction();

    return m_stlListOfTableIdentifiers;
}

/********************************************************************************************/

DatasetTable __thiscall Dataset::GetDatasetTable(
    _in const char * c_szTableIdentifier
    ) const
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetMetadata.IsElementPresent("Tables", INDEXED_BUFFER_VALUE_TYPE));

    Qword qwTableIdentifierHash = ::Get64BitHashOfNullTerminatedString(c_szTableIdentifier, false);
    _ThrowBaseExceptionIf((m_stlListOfTableMarkerOffsets.end() == m_stlListOfTableMarkerOffsets.find(qwTableIdentifierHash)), "ERROR: Invalid Dataset Identifier %s", c_szTableIdentifier);
    StructuredBuffer oTable(m_oDatasetMetadata.GetStructuredBuffer("Tables").GetStructuredBuffer(c_szTableIdentifier));
    uint64_t un64Offset = m_stlListOfTableMarkerOffsets.at(qwTableIdentifierHash);

    return DatasetTable(m_strFilename, oTable.GetSerializedBuffer(), un64Offset);
}

/********************************************************************************************/

std::vector<Byte> __thiscall Dataset::GetSerializedDatasetMetadata(void) const throw()
{
    __DebugFunction();
    
    return m_oDatasetMetadata.GetSerializedBuffer();
}