/*********************************************************************************************
 *
 * @file DatasetTable.cpp
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
#include <algorithm>

/********************************************************************************************/

DatasetTable::DatasetTable(
    _in const std::string & c_strFilename,
    _in const std::vector<Byte> & c_stlSerializedTableMetadataBuffer,
    _in uint64_t un64OffsetInBytesToTableDataInFile
    )
{
    __DebugFunction();

    StructuredBuffer oDatasetMetadata(c_stlSerializedTableMetadataBuffer);
    // Make sure the metadata contains what is expected
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("id", GUID_VALUE_TYPE)), "INVALID METADATA: id is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("name", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: name is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("description", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: description is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("tags", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: tags is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("number_of_columns", UINT32_VALUE_TYPE)), "INVALID METADATA: number_of_columns is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("number_of_rows", UINT64_VALUE_TYPE)), "INVALID METADATA: number_of_rows is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("data_size_in_bytes", UINT64_VALUE_TYPE)), "INVALID METADATA: data_size_in_bytes is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("compressed_data_size_in_bytes", UINT64_VALUE_TYPE)), "INVALID METADATA: compressed_data_size_in_bytes is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("all_column_properties", INDEXED_BUFFER_VALUE_TYPE)), "INVALID METADATA: all_column_properties is missing", nullptr);
    
    // Is this instance of DatasetTable being initialized with metadata only or with a file?
    if ((0 < c_strFilename.size())&&(0xFFFFFFFFFFFFFFFF != un64OffsetInBytesToTableDataInFile))
    {
        // Quick reality check to make sure everything lines upper_bound
        BinaryFileReader oBinaryFileReader(c_strFilename);
        // Move to the target offset and read the marker
        Qword qwMarker;
        oBinaryFileReader.Seek(eFromBeginningOfFile, un64OffsetInBytesToTableDataInFile);
        oBinaryFileReader.Read((void *) &qwMarker, sizeof(qwMarker));
        _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != qwMarker), "Invalid marker value of 0x%08X%08X found at the beginning of the file", HIDWORD(qwMarker), LODWORD(qwMarker));
        // Read the table identifier
        std::vector<Byte> stlBuffer = oBinaryFileReader.Read(16);
        __DebugAssert(16 == stlBuffer.size());
        Guid oTableIdentifier((const Byte *) stlBuffer.data());
        _ThrowBaseExceptionIf((oTableIdentifier != oDatasetMetadata.GetGuid("id")), "UNEXPECTED ERROR: Incorrect table identifier %s", oTableIdentifier.ToString(eHyphensOnly).c_str());
        // Read the compressed size in bytes
        uint64_t un64CompressedSizeInBytes = 0;
        oBinaryFileReader.Read((void *) &un64CompressedSizeInBytes, sizeof(un64CompressedSizeInBytes));
        _ThrowBaseExceptionIf((un64CompressedSizeInBytes != oDatasetMetadata.GetUnsignedInt64("compressed_data_size_in_bytes")), "UNEXPECTED ERROR: Incorrect compressed size in bytes %ld (expecting %ld)", un64CompressedSizeInBytes, oDatasetMetadata.GetUnsignedInt64("compressed_data_size_in_bytes"));
        // Move the file cursor forward from the current position (1) to find the marker at the end of the compressed data stream
        oBinaryFileReader.Seek(eFromCurrentPositionInFile, un64CompressedSizeInBytes);
        // Read the market
        oBinaryFileReader.Read((void *) &qwMarker, sizeof(qwMarker));
        _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != qwMarker), "Invalid marker value of 0x%08X%08X found at the beginning of the file", HIDWORD(qwMarker), LODWORD(qwMarker));
        // The offset to table data + the size of the compressed data should not be greater than the size of the file
        uint64_t un64TotalSizeInBytesOfTable = sizeof(Qword) + 16 + sizeof(uint64_t) + oDatasetMetadata.GetUnsignedInt64("compressed_data_size_in_bytes");
        _ThrowBaseExceptionIf(((un64OffsetInBytesToTableDataInFile + un64TotalSizeInBytesOfTable) > oBinaryFileReader.GetSizeInBytes()), "ERROR: Invalid size in bytes for table data.", nullptr);
    }

    // Okay, up to now, everything seems to be doing well. Now let's parse through the columns in the metadata
    unsigned int unColumnCount = oDatasetMetadata.GetUnsignedInt32("number_of_columns");
    StructuredBuffer oAllColumnProperties = oDatasetMetadata.GetStructuredBuffer("all_column_properties");
    std::vector<std::string> stlListOfColumns = oAllColumnProperties.GetNamesOfElements();
    // Erase the __IsArray__ from the list of columns
    stlListOfColumns.erase(std::remove(stlListOfColumns.begin(), stlListOfColumns.end(), "__IsArray__"), stlListOfColumns.end());
    _ThrowBaseExceptionIf((unColumnCount != stlListOfColumns.size()), "ERROR: Unexpected number of columns %d (expecting %d)", stlListOfColumns.size(), unColumnCount);
    for (unsigned int unColumnIndex = 0; unColumnIndex < unColumnCount; ++unColumnIndex)
    {
        std::string columnIndexAsString = std::to_string(unColumnIndex);
        StructuredBuffer oColumnProperties(oAllColumnProperties.GetStructuredBuffer(columnIndexAsString.c_str()));
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("id", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: id is missing", nullptr);
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("name", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: name is missing", nullptr);
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("description", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: description is missing", nullptr);
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("tags", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: tags is missing", nullptr);
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("units", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: units is missing", nullptr);
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("type", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: type is missing", nullptr);
        std::string strColumnIdentifier = oColumnProperties.GetString("id");
        Qword qwHashOfColumnIdentifier = ::Get64BitHashOfNullTerminatedString(strColumnIdentifier.c_str(), false);
        m_stlColumnIdentifiers.push_back(strColumnIdentifier);
        m_stlColumnIndexByIdentifier[qwHashOfColumnIdentifier] = unColumnIndex;
    }
    // If everything went well, everything is proper, we can persist member variable
    m_oTableMetadata = oDatasetMetadata;
    m_strFilename = c_strFilename;
    m_un64OffsetInBytesToTableDataInFile = un64OffsetInBytesToTableDataInFile;
}

/********************************************************************************************/

DatasetTable::~DatasetTable(void)
{
    __DebugFunction();
}

/********************************************************************************************/

std::string __thiscall DatasetTable::GetTableIdentifier(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("id", GUID_VALUE_TYPE));

    return m_oTableMetadata.GetGuid("id").ToString(eHyphensOnly);
}

/********************************************************************************************/

std::string __thiscall DatasetTable::GetTitle(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("name", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oTableMetadata.GetString("name");
}

/********************************************************************************************/

std::string __thiscall DatasetTable::GetDescription(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("description", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oTableMetadata.GetString("description");
}

/********************************************************************************************/

std::string __thiscall DatasetTable::GetTags(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("tags", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oTableMetadata.GetString("tags");
}

/********************************************************************************************/

uint64_t __thiscall DatasetTable::GetRowCount(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("number_of_rows", UINT64_VALUE_TYPE));

    return m_oTableMetadata.GetUnsignedInt64("number_of_rows");
}

/********************************************************************************************/

unsigned int __thiscall DatasetTable::GetColumnCount(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("number_of_columns", UINT32_VALUE_TYPE));

    return m_oTableMetadata.GetUnsignedInt32("number_of_columns");
}

/********************************************************************************************/

std::vector<std::string> __thiscall DatasetTable::GetColumnIdentifiers(void) const throw()
{
    __DebugFunction();

    return m_stlColumnIdentifiers;
}

/********************************************************************************************/

DatasetTableColumn __thiscall DatasetTable::GetTableColumn(
    _in const char * c_szColumnIdentifier
    ) const
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szColumnIdentifier);
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("all_column_properties", INDEXED_BUFFER_VALUE_TYPE));

    Qword qwHashOfColumnIdentifier = ::Get64BitHashOfNullTerminatedString(c_szColumnIdentifier, false);
    _ThrowBaseExceptionIf((m_stlColumnIndexByIdentifier.end() == m_stlColumnIndexByIdentifier.find(qwHashOfColumnIdentifier)), "ERROR: Invalid column identifier %s. Column not found", c_szColumnIdentifier);
    unsigned int unColumnIndex = m_stlColumnIndexByIdentifier.at(qwHashOfColumnIdentifier);
    std::string strColumnIndexAsString = std::to_string(unColumnIndex);
    StructuredBuffer oColumnProperties = m_oTableMetadata.GetStructuredBuffer("all_column_properties").GetStructuredBuffer(strColumnIndexAsString.c_str());
    
    return DatasetTableColumn(oColumnProperties.GetSerializedBuffer());
}

/********************************************************************************************/

StructuredBuffer __thiscall DatasetTable::GetInformationForDataAccess(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("compressed_data_size_in_bytes", UINT64_VALUE_TYPE));
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("data_size_in_bytes", UINT64_VALUE_TYPE));
    
    StructuredBuffer oInformationForDataAccess;
    
    oInformationForDataAccess.PutString("DatasetFilename", m_strFilename);
    oInformationForDataAccess.PutUnsignedInt64("data_size_in_bytes", m_oTableMetadata.GetUnsignedInt64("data_size_in_bytes"));
    oInformationForDataAccess.PutUnsignedInt64("CompressedSizeInBytes", m_oTableMetadata.GetUnsignedInt64("compressed_data_size_in_bytes"));
    oInformationForDataAccess.PutUnsignedInt64("OffsetToFirstByteOfCompressedData", m_un64OffsetInBytesToTableDataInFile + sizeof(Qword) + 16 + sizeof(uint64_t));
    
    return oInformationForDataAccess;
}