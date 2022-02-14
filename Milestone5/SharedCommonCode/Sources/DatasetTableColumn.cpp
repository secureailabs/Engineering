/*********************************************************************************************
 *
 * @file DatasetTableColumn.cpp
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

/********************************************************************************************/

DatasetTableColumn::DatasetTableColumn(
    _in const std::vector<Byte> & c_stlSerializedColumnMetadataBuffer
    )
{
    __DebugFunction();
    
    // Deserialize the dataset table column
    StructuredBuffer oDatasetTableColumnMetadata(c_stlSerializedColumnMetadataBuffer);
    // Reality check to ensure all of the data is in place correctly
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("ColumnIdentifier", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: ColumnIdentifier is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Title is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Description is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Tags is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("Units", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Units is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("Type", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: Type is missing", nullptr);
    // Persist the metadata
    m_oDatasetTableColumnMetadata = oDatasetTableColumnMetadata;
}

/********************************************************************************************/

DatasetTableColumn::~DatasetTableColumn(void)
{
    __DebugFunction();
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetColumnIdentifier(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("ColumnIdentifier", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("ColumnIdentifier");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetTitle(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("Title");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetDescription(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("Description");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetTags(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("Tags");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetUnits(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("Units", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("Units");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetType(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("Type", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("Type");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetUnitCategories(void) const
{
    __DebugFunction();

    // It is possible for "UnitCategories" not to exits. This is why this method can throw if
    // someone tries to call it
    
    return m_oDatasetTableColumnMetadata.GetString("UnitCategories");
}