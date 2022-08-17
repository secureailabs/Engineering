/*********************************************************************************************
 *
 * @file DatasetVersionTableColumn.cpp
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

/********************************************************************************************/

DatasetVersionTableColumn::DatasetVersionTableColumn(
    _in const std::vector<Byte> & c_stlSerializedColumnMetadataBuffer
    )
{
    __DebugFunction();
    
    // Deserialize the dataset table column
    StructuredBuffer oDatasetVersionTableColumnMetadata(c_stlSerializedColumnMetadataBuffer);
    // Reality check to ensure all of the data is in place correctly
    _ThrowBaseExceptionIf((false == oDatasetVersionTableColumnMetadata.IsElementPresent("id", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: id is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionTableColumnMetadata.IsElementPresent("name", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: name is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionTableColumnMetadata.IsElementPresent("description", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: description is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionTableColumnMetadata.IsElementPresent("tags", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: tags is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionTableColumnMetadata.IsElementPresent("units", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: units is missing", nullptr);
    _ThrowBaseExceptionIf((false == oDatasetVersionTableColumnMetadata.IsElementPresent("type", ANSI_CHARACTER_STRING_VALUE_TYPE)), "INVALID METADATA: type is missing", nullptr);
    // Persist the metadata
    m_oDatasetVersionTableColumnMetadata = oDatasetVersionTableColumnMetadata;
}

/********************************************************************************************/

DatasetVersionTableColumn::~DatasetVersionTableColumn(void)
{
    __DebugFunction();
}

/********************************************************************************************/

std::string __thiscall DatasetVersionTableColumn::GetColumnIdentifier(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionTableColumnMetadata.IsElementPresent("id", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetVersionTableColumnMetadata.GetString("id");
}

/********************************************************************************************/

std::string __thiscall DatasetVersionTableColumn::GetTitle(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionTableColumnMetadata.IsElementPresent("name", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetVersionTableColumnMetadata.GetString("name");
}

/********************************************************************************************/

std::string __thiscall DatasetVersionTableColumn::GetDescription(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionTableColumnMetadata.IsElementPresent("description", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetVersionTableColumnMetadata.GetString("description");
}

/********************************************************************************************/

std::string __thiscall DatasetVersionTableColumn::GetTags(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionTableColumnMetadata.IsElementPresent("tags", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetVersionTableColumnMetadata.GetString("tags");
}

/********************************************************************************************/

std::string __thiscall DatasetVersionTableColumn::GetUnits(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionTableColumnMetadata.IsElementPresent("units", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetVersionTableColumnMetadata.GetString("units");
}

/********************************************************************************************/

std::string __thiscall DatasetVersionTableColumn::GetType(void) const throw()
{
    __DebugFunction();
    __DebugAssert(true == m_oDatasetVersionTableColumnMetadata.IsElementPresent("type", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    return m_oDatasetVersionTableColumnMetadata.GetString("type");
}

/********************************************************************************************/

std::string __thiscall DatasetVersionTableColumn::GetUnitCategories(void) const
{
    __DebugFunction();

    // It is possible for "UnitCategories" not to exits. This is why this method can throw if
    // someone tries to call it
    
    return m_oDatasetVersionTableColumnMetadata.GetString("UnitCategories");
}