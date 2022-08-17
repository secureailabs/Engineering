/*********************************************************************************************
 *
 * @file DatasetVersion.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "64BitHashes.h"
#include "BinaryFileHandlers.h"
#include "DatasetVersion.h"
#include "DebugLibrary.h"
#include "Exceptions.h"

#include <filesystem>
#include <iostream>
#include <algorithm>

/********************************************************************************************/

DatasetVersion::DatasetVersion(
    _in const char * c_szFullFilename
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szFullFilename);
    
    BinaryFileReader oBinaryFileReader(c_szFullFilename);
    Qword qwMarker;
    oBinaryFileReader.Read((void *) &qwMarker, sizeof(qwMarker));
    _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != qwMarker), "Invalid marker value of 0x%08X%08X found at the beginning of the file", HIDWORD(qwMarker), LODWORD(qwMarker));
    unsigned int unSizeInBytesOfDatasetVersionMetadata = 0;
    oBinaryFileReader.Read((void *) &unSizeInBytesOfDatasetVersionMetadata, sizeof(unSizeInBytesOfDatasetVersionMetadata));
    std::vector<Byte> stlBuffer = oBinaryFileReader.Read(unSizeInBytesOfDatasetVersionMetadata);
    StructuredBuffer oDatasetVersionMetadata(stlBuffer);
    // Now let's do a quick reality check and make sure the header is in good order
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("version", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: version is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("id", GUID_VALUE_TYPE)), "INVALID METADATA: id is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("organization_id", GUID_VALUE_TYPE)), "INVALID METADATA: organization_id is missing", nullptr);
    // _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("dataset_id", GUID_VALUE_TYPE)), "INVALID METADATA: Dataset Identifier is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("name", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: name is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("description", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: description is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("keywords", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: keywords is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("publish_date", UINT64_VALUE_TYPE)), "INVALID METADATA: publish_date is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("number_of_tables", UINT32_VALUE_TYPE)), "INVALID METADATA: number_of_tables is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("tables", INDEXED_BUFFER_VALUE_TYPE)), "INVALID METADATA: tables are missing", nullptr);
    // Track the cursor offset into the file. At this point, the current position should point to
    // the marker for the first table
    uint64_t un64FilePosition = oBinaryFileReader.GetFilePointer();
    oBinaryFileReader.Read((void *) &qwMarker, sizeof(qwMarker));
    _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != qwMarker), "Invalid marker value of 0x%08X%08X found at the beginning of the file", HIDWORD(qwMarker), LODWORD(qwMarker));

    StructuredBuffer oAllTables(oDatasetVersionMetadata.GetStructuredBuffer("tables"));
    for (const auto & strTableIndex : oAllTables.GetNamesOfElements())
    {
        if ("__IsArray__" != strTableIndex)
        {
            StructuredBuffer oTableMetadata(oAllTables.GetStructuredBuffer(strTableIndex.c_str()));
            m_stlMapOfTableIdentifiers.insert(std::make_pair(oTableMetadata.GetGuid("id").ToString(eHyphensOnly), std::atoi(strTableIndex.c_str())));
        }
    }

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
        _ThrowBaseExceptionIf((m_stlMapOfTableIdentifiers.end() == m_stlMapOfTableIdentifiers.find(strTableIdentifier)), "ERROR: Table identifier %s was found in the file, but not in the metadata.", strTableIdentifier.c_str());
        // Save this information
        Qword qwHashOfTableIdentifier = ::Get64BitHashOfNullTerminatedString(strTableIdentifier.c_str(), false);
        m_stlListOfTableMarkerOffsets[qwHashOfTableIdentifier] = un64FilePosition;
        // Update the un64FilePosition to the latest value
        un64FilePosition = un64NewFilePosition;
    }
    while (oBinaryFileReader.GetFilePointer() < oBinaryFileReader.GetSizeInBytes());
    // Since everything went well, let's persist the dataset metadata
    m_oDatasetVersionMetadata = oDatasetVersionMetadata;
    m_strFilename = c_szFullFilename;
    m_fIsMetadataOnly = false;
}

/********************************************************************************************/

DatasetVersion::DatasetVersion(
    _in const std::vector<Byte> & c_stlSerializedMetadata
    )
{
    __DebugFunction();

    // De-serialized the incoming serialized data
    StructuredBuffer oDatasetVersionMetadata(c_stlSerializedMetadata);
    // Now let's do a quick reality check and make sure the header is in good order
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("version", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: version is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("id", GUID_VALUE_TYPE)), "INVALID METADATA: DatasetVersionGuid is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("organization_id", GUID_VALUE_TYPE)), "INVALID METADATA: OrganizationGuid is missing", nullptr);
    //_ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("DataFamilyIdentifier", GUID_VALUE_TYPE)), "INVALID METADATA: DataFamilyIdentifier is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("name", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Title is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("description", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Description is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("keywords", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: keywords is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("publish_date", UINT64_VALUE_TYPE)), "INVALID METADATA: publish_date is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("number_of_tables", UINT32_VALUE_TYPE)), "INVALID METADATA: number_of_tables is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionMetadata.IsElementPresent("tables", INDEXED_BUFFER_VALUE_TYPE)), "INVALID METADATA: Tables are missing", nullptr);
    // Let's extract the table identifiers from the metadata. This is different than the
    // constructor that loads from file, since in that case, we load from file and then
    // verify it exists in the metadata
    StructuredBuffer oAllTables(oDatasetVersionMetadata.GetStructuredBuffer("tables"));
    std::vector<std::string> stlListOfTables = oAllTables.GetNamesOfElements();

    // Erase the __IsArray__ from the list of columns
    stlListOfTables.erase(std::remove(stlListOfTables.begin(), stlListOfTables.end(), "__IsArray__"), stlListOfTables.end());

    for (std::string strTableIndex: stlListOfTables)
    {
        StructuredBuffer oTable = oAllTables.GetStructuredBuffer(strTableIndex.c_str());
        auto strTableIdentifier = oTable.GetGuid("id").ToString(eHyphensOnly);
        Qword qwHashOfTableIdentifier = ::Get64BitHashOfNullTerminatedString(strTableIdentifier.c_str(), false);
        m_stlMapOfTableIdentifiers.insert(std::make_pair(strTableIdentifier, std::stoi(strTableIndex)));
        m_stlListOfTableMarkerOffsets[qwHashOfTableIdentifier] = 0xFFFFFFFFFFFFFFFF;
    }
    // Since everything went well, let's persist the dataset metadata
    m_oDatasetVersionMetadata = oDatasetVersionMetadata;
    m_fIsMetadataOnly = true;
}

/********************************************************************************************/

DatasetVersion::~DatasetVersion(void) throw()
{
    __DebugFunction();
}

/********************************************************************************************/

std::string __thiscall DatasetVersion::GetDatasetVersionIdentifier(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionMetadata.IsElementPresent("id", GUID_VALUE_TYPE));

    return m_oDatasetVersionMetadata.GetGuid("id").ToString(eHyphensOnly);
}

/********************************************************************************************/

std::string __thiscall DatasetVersion::GetDatasetFamilyIdentifier(void) const throw()
{
    __DebugFunction();
    
    std::string strDatasetVersionFamilyIdentifier = "00000000-0000-0000-0000-000000000000";
    
    if (true == m_oDatasetVersionMetadata.IsElementPresent("dataset_id", GUID_VALUE_TYPE))
    {
        strDatasetVersionFamilyIdentifier = m_oDatasetVersionMetadata.GetGuid("dataset_id").ToString(eHyphensOnly);
    }

    return strDatasetVersionFamilyIdentifier;
}

/********************************************************************************************/

std::string __thiscall DatasetVersion::GetPublisherIdentifier(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionMetadata.IsElementPresent("organization_id", GUID_VALUE_TYPE));

    return m_oDatasetVersionMetadata.GetGuid("organization_id").ToString(eHyphensOnly);
}

/********************************************************************************************/

std::string __thiscall DatasetVersion::GetTitle(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionMetadata.IsElementPresent("name", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oDatasetVersionMetadata.GetString("name");
}

/********************************************************************************************/

std::string __thiscall DatasetVersion::GetDescription(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionMetadata.IsElementPresent("description", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oDatasetVersionMetadata.GetString("description");
}

/********************************************************************************************/

std::string __thiscall DatasetVersion::GetKeywords(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionMetadata.IsElementPresent("keywords", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oDatasetVersionMetadata.GetString("keywords");
}

/********************************************************************************************/

uint64_t __thiscall DatasetVersion::GetPublishDate(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionMetadata.IsElementPresent("publish_date", UINT64_VALUE_TYPE));

    return m_oDatasetVersionMetadata.GetUnsignedInt64("publish_date");
}

/********************************************************************************************/

unsigned int __thiscall DatasetVersion::GetNumberOfTables(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionMetadata.IsElementPresent("number_of_tables", UINT32_VALUE_TYPE));

    return m_oDatasetVersionMetadata.GetUnsignedInt32("number_of_tables");
}

/********************************************************************************************/

std::vector<std::string> __thiscall DatasetVersion::GetTableIdentifiers(void) const throw()
{
    __DebugFunction();

    std::vector<std::string> stlResponseListOfTableIdentifiers;
    for (const auto & strIdentifier : m_stlMapOfTableIdentifiers)
    {
        stlResponseListOfTableIdentifiers.push_back(strIdentifier.first);
    }

    return stlResponseListOfTableIdentifiers;
}

/********************************************************************************************/

DatasetVersionTable __thiscall DatasetVersion::GetDatasetVersionTable(
    _in const char * c_szTableIdentifier
    ) const
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionMetadata.IsElementPresent("tables", INDEXED_BUFFER_VALUE_TYPE));

    Qword qwTableIdentifierHash = ::Get64BitHashOfNullTerminatedString(c_szTableIdentifier, false);
    _ThrowBaseExceptionIf((m_stlListOfTableMarkerOffsets.end() == m_stlListOfTableMarkerOffsets.find(qwTableIdentifierHash)), "ERROR: Invalid DatasetVersion Identifier %s", c_szTableIdentifier);

    std::string strTableKey = std::to_string(m_stlMapOfTableIdentifiers.at(c_szTableIdentifier));
    StructuredBuffer oTable(m_oDatasetVersionMetadata.GetStructuredBuffer("tables").GetStructuredBuffer(strTableKey.c_str()));
    uint64_t un64Offset = m_stlListOfTableMarkerOffsets.at(qwTableIdentifierHash);

    return DatasetVersionTable(m_strFilename, oTable.GetSerializedBuffer(), un64Offset);
}

/********************************************************************************************/

std::vector<Byte> __thiscall DatasetVersion::GetSerializedDatasetVersionMetadata(void) const throw()
{
    __DebugFunction();

    return m_oDatasetVersionMetadata.GetSerializedBuffer();
}

