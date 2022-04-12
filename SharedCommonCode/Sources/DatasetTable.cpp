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
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("TableIdentifier", GUID_VALUE_TYPE)), "INVALID METADATA: TableIdentifier is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Title is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Description is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Tags is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("NumberOfColumns", UINT32_VALUE_TYPE)), "INVALID METADATA: NumberOfColumns is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("NumberOfRows", UINT64_VALUE_TYPE)), "INVALID METADATA: NumberOfRows is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("DataSizeInBytes", UINT64_VALUE_TYPE)), "INVALID METADATA: DataSizeInBytes is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("CompressedDataSizeInBytes", UINT64_VALUE_TYPE)), "INVALID METADATA: CompressedDataSizeInBytes is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetMetadata.IsElementPresent("AllColumnProperties", INDEXED_BUFFER_VALUE_TYPE)), "INVALID METADATA: AllColumnProperties is missing", nullptr);
    
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
        _ThrowBaseExceptionIf((oTableIdentifier != oDatasetMetadata.GetGuid("TableIdentifier")), "UNEXPECTED ERROR: Incorrect table identifier %s", oTableIdentifier.ToString(eHyphensOnly).c_str());
        // Read the compressed size in bytes
        uint64_t un64CompressedSizeInBytes = 0;
        oBinaryFileReader.Read((void *) &un64CompressedSizeInBytes, sizeof(un64CompressedSizeInBytes));
        _ThrowBaseExceptionIf((un64CompressedSizeInBytes != oDatasetMetadata.GetUnsignedInt64("CompressedDataSizeInBytes")), "UNEXPECTED ERROR: Incorrect compressed size in bytes %ld (expecting %ld)", un64CompressedSizeInBytes, oDatasetMetadata.GetUnsignedInt64("CompressedDataSizeInBytes"));
        // Move the file cursor forward from the current position (1) to find the marker at the end of the compressed data stream
        oBinaryFileReader.Seek(eFromCurrentPositionInFile, un64CompressedSizeInBytes);
        // Read the market
        oBinaryFileReader.Read((void *) &qwMarker, sizeof(qwMarker));
        _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != qwMarker), "Invalid marker value of 0x%08X%08X found at the beginning of the file", HIDWORD(qwMarker), LODWORD(qwMarker));
        // The offset to table data + the size of the compressed data should not be greater than the size of the file
        uint64_t un64TotalSizeInBytesOfTable = sizeof(Qword) + 16 + sizeof(uint64_t) + oDatasetMetadata.GetUnsignedInt64("CompressedDataSizeInBytes");
        _ThrowBaseExceptionIf(((un64OffsetInBytesToTableDataInFile + un64TotalSizeInBytesOfTable) > oBinaryFileReader.GetSizeInBytes()), "ERROR: Invalid size in bytes for table data.", nullptr);
    }
    
    // Okay, up to now, everything seems to be doing well. Now let's parse through the columns in the metadata
    unsigned int unColumnCount = oDatasetMetadata.GetUnsignedInt32("NumberOfColumns");
    StructuredBuffer oAllColumnProperties = oDatasetMetadata.GetStructuredBuffer("AllColumnProperties");
    std::vector<std::string> stlListOfColumns = oAllColumnProperties.GetNamesOfElements();
    _ThrowBaseExceptionIf((unColumnCount != stlListOfColumns.size()), "ERROR: Unexpected number of columns %d (expecting %d)", stlListOfColumns.size(), unColumnCount);
    for (unsigned int unColumnIndex = 0; unColumnIndex < unColumnCount; ++unColumnIndex)
    {
        std::string columnIndexAsString = std::to_string(unColumnIndex);
        StructuredBuffer oColumnProperties(oAllColumnProperties.GetStructuredBuffer(columnIndexAsString.c_str()));
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("ColumnIdentifier", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: ColumnIdentifier is missing", nullptr);
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Title is missing", nullptr);
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Description is missing", nullptr);
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Tags is missing", nullptr);
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("Units", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Units is missing", nullptr);
        _ThrowBaseExceptionIf((false == oColumnProperties.IsElementPresent("Type", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Type is missing", nullptr);
        std::string strColumnIdentifier = oColumnProperties.GetString("ColumnIdentifier");
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
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("TableIdentifier", GUID_VALUE_TYPE));

    return m_oTableMetadata.GetGuid("TableIdentifier").ToString(eHyphensOnly);
}

/********************************************************************************************/

std::string __thiscall DatasetTable::GetTitle(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oTableMetadata.GetString("Title");
}

/********************************************************************************************/

std::string __thiscall DatasetTable::GetDescription(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oTableMetadata.GetString("Description");
}

/********************************************************************************************/

std::string __thiscall DatasetTable::GetTags(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE));

    return m_oTableMetadata.GetString("Tags");
}

/********************************************************************************************/

uint64_t __thiscall DatasetTable::GetRowCount(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("NumberOfRows", UINT64_VALUE_TYPE));

    return m_oTableMetadata.GetUnsignedInt64("NumberOfRows");
}

/********************************************************************************************/

unsigned int __thiscall DatasetTable::GetColumnCount(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("NumberOfColumns", UINT32_VALUE_TYPE));

    return m_oTableMetadata.GetUnsignedInt32("NumberOfColumns");
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
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("AllColumnProperties", INDEXED_BUFFER_VALUE_TYPE));

    Qword qwHashOfColumnIdentifier = ::Get64BitHashOfNullTerminatedString(c_szColumnIdentifier, false);
    _ThrowBaseExceptionIf((m_stlColumnIndexByIdentifier.end() == m_stlColumnIndexByIdentifier.find(qwHashOfColumnIdentifier)), "ERROR: Invalid column identifier %s. Column not found", c_szColumnIdentifier);
    unsigned int unColumnIndex = m_stlColumnIndexByIdentifier.at(qwHashOfColumnIdentifier);
    std::string strColumnIndexAsString = std::to_string(unColumnIndex);
    StructuredBuffer oColumnProperties = m_oTableMetadata.GetStructuredBuffer("AllColumnProperties").GetStructuredBuffer(strColumnIndexAsString.c_str());
    
    return DatasetTableColumn(oColumnProperties.GetSerializedBuffer());
}

/********************************************************************************************/

StructuredBuffer __thiscall DatasetTable::GetInformationForDataAccess(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("CompressedDataSizeInBytes", UINT64_VALUE_TYPE));
    __DebugAssert(true == m_oTableMetadata.IsElementPresent("DataSizeInBytes", UINT64_VALUE_TYPE));
    
    StructuredBuffer oInformationForDataAccess;
    
    oInformationForDataAccess.PutString("DatasetFilename", m_strFilename);
    oInformationForDataAccess.PutUnsignedInt64("DataSizeInBytes", m_oTableMetadata.GetUnsignedInt64("DataSizeInBytes"));
    oInformationForDataAccess.PutUnsignedInt64("CompressedSizeInBytes", m_oTableMetadata.GetUnsignedInt64("CompressedDataSizeInBytes"));
    oInformationForDataAccess.PutUnsignedInt64("OffsetToFirstByteOfCompressedData", m_un64OffsetInBytesToTableDataInFile + sizeof(Qword) + 16 + sizeof(uint64_t));
    
    return oInformationForDataAccess;
}