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
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("id", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: id is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("name", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: name is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("description", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: description is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("tags", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: tags is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("units", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: units is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetTableColumnMetadata.IsElementPresent("type", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: type is missing", nullptr);
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
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("id", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("id");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetTitle(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("name", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("name");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetDescription(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("description", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("description");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetTags(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("tags", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("tags");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetUnits(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("units", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("units");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetType(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetTableColumnMetadata.IsElementPresent("type", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetTableColumnMetadata.GetString("type");
}

/********************************************************************************************/

std::string __thiscall DatasetTableColumn::GetUnitCategories(void) const
{
    __DebugFunction();

    // It is possible for "UnitCategories" not to exits. This is why this method can throw if
    // someone tries to call it
    
    return m_oDatasetTableColumnMetadata.GetString("UnitCategories");
}