/*********************************************************************************************
 *
 * @file DataConnector.cpp
 * @author Prawal Gangwar
 * @date 05 Nov 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "Base64Encoder.h"
#include "BinaryFileHandlers.h"
#include "CompressionHelperFunctions.h"
#include "DataConnector.h"
#include "Dataset.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "StatusMonitor.h"
#include "IpcTransactionHelperFunctions.h"

#include <stdio.h>
#include <string.h>

#include <iostream>
#include <fstream>
#include <sstream>

// Singleton Object
static DataConnector g_oDataConnector;

/********************************************************************************************
 *
 * @function GetDataConnector
 * @brief Gets the singleton instance of the DataConnector object
 *
 ********************************************************************************************/
 
DataConnector * __stdcall GetDataConnector(void) throw()
{
    __DebugFunction();

    return &g_oDataConnector;
}

/********************************************************************************************
 *
 * @class DataConnector
 * @function DataConnector
 * @brief Constructor to create a DataConnector object
 * @param[in] c_szFileName Name of the dataset file(csvp)
 *
 ********************************************************************************************/

DataConnector::DataConnector(void)
{
    __DebugFunction();
}

/********************************************************************************************
 *
 * @class DataConnector
 * @function DataConnector
 * @brief Default copy constructor which is overloaded in order to trap any attempts to copy this singleton object
 *
 ********************************************************************************************/
 
DataConnector::DataConnector(
    _in const DataConnector & c_oDataConnector
    )
{
    __DebugFunction();
    __DebugAssert(false);
}

/********************************************************************************************
 *
 * @class DataConnector
 * @function ~DataConnector
 * @brief object Destructor
 *
 ********************************************************************************************/

DataConnector::~DataConnector(void)
{
    __DebugFunction();
}

/********************************************************************************************
 *
 * @class DataConnector
 * @function LoadAndVerify
 * @brief Loads the csv file by verifying its integerity and storing it in
 *     memory as a 3D vecotr of tables.
 * @return true on successful verification, false otherwise
 *
 ********************************************************************************************/

// TODO: instead of fileName, take the file as a buffer
bool __thiscall DataConnector::LoadAndVerify(
    _in RootOfTrustNode * poRootOfTrustNode
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != poRootOfTrustNode);
    
    // Persist the RootOfTrustNode
    m_poRootOfTrustNode = poRootOfTrustNode;
    // Load the dataset from file
    Dataset oDataset(m_poRootOfTrustNode->GetDatasetFilename().c_str());
    // Initialize m_oDatasetMetadata
    m_oDatasetMetadata.PutString("DatasetIdentifier", oDataset.GetDatasetIdentifier());
    m_oDatasetMetadata.PutString("DatasetFamilyIdentifier", oDataset.GetDatasetFamilyIdentifier());
    m_oDatasetMetadata.PutString("PublisherIdentifier", oDataset.GetPublisherIdentifier());
    m_oDatasetMetadata.PutString("Title", oDataset.GetTitle());
    m_oDatasetMetadata.PutString("Description", oDataset.GetTags());
    m_oDatasetMetadata.PutUnsignedInt64("EpochCreationTimeInSeconds", oDataset.GetEpochCreationTimeInSeconds());
    m_oDatasetMetadata.PutUnsignedInt32("TableCount", oDataset.GetTableCount());
    // Begin initializing m_oAllDatasetIds
    m_oAllDatasetIds.PutString("DatasetUuid", oDataset.GetDatasetIdentifier());
    // Build the table metadata
    StructuredBuffer oAllTablesMetadata;
    // Seek to each tables metadata and store the StructuredBuffer into the class member
    std::vector<std::string> stlListOfTableIdentifiers = oDataset.GetTableIdentifiers();
    __DebugAssert(stlListOfTableIdentifiers.size() == oDataset.GetTableCount());
    for (const std::string c_strTableIdentifier: stlListOfTableIdentifiers)
    {
        DatasetTable oDatasetTable = oDataset.GetDatasetTable(c_strTableIdentifier.c_str());
        // Build the metadata blob for the current table
        StructuredBuffer oTableMedata;
        oTableMedata.PutString("TableIdentifier", oDatasetTable.GetTableIdentifier());
        oTableMedata.PutString("Title", oDatasetTable.GetTitle());
        oTableMedata.PutString("Description", oDatasetTable.GetDescription());
        oTableMedata.PutString("Tags", oDatasetTable.GetTags());
        oTableMedata.PutUnsignedInt64("RowCount", oDatasetTable.GetRowCount());
        oTableMedata.PutUnsignedInt32("ColumnCount", oDatasetTable.GetColumnCount());
        m_stlTableMetaData.push_back(StructuredBuffer(oTableMedata));

        // HACK-DG We want to store everything as eRaw
        Guid oDatasetIdentifier(oDatasetTable.GetTableIdentifier());
        oAllTablesMetadata.PutString(oDatasetTable.GetTitle().c_str(), oDatasetIdentifier.ToString(eRaw));
    }
    m_oAllDatasetIds.PutStructuredBuffer("Tables", oAllTablesMetadata);

    unsigned int unTableIndex = 0;
    // Read each table and store it in a 3D vector of tables
    for (const std::string & c_strTableIdentifier: stlListOfTableIdentifiers)
    {
        // Where to store your individual table.
        std::vector<std::vector<std::string>> stlIndividualTable;
        // Get the dataset table
        DatasetTable oDatasetTable = oDataset.GetDatasetTable(c_strTableIdentifier.c_str());
        // Extract the table into plain-text
        StructuredBuffer oInformationForDataAccess(oDatasetTable.GetInformationForDataAccess());
        BinaryFileReader oBinaryFileReader(oInformationForDataAccess.GetString("DatasetFilename"));
        oBinaryFileReader.Seek(eFromBeginningOfFile, oInformationForDataAccess.GetUnsignedInt64("OffsetToFirstByteOfCompressedData"));
        std::vector<Byte> stlCompressedSerializedData = oBinaryFileReader.Read(oInformationForDataAccess.GetUnsignedInt64("CompressedSizeInBytes"));
        StructuredBuffer oCompressedSerializedData(stlCompressedSerializedData);
        // Make sure to clear the original stlCompressedSerializedData in order to free up memory
        stlCompressedSerializedData.clear();
        std::vector<Byte> stlDecompressedSerializedData = ::DecompressStructuredBuffer(oCompressedSerializedData);
        // Make sure to clear the original oCompressedSerializedData in order to free up memory
        oCompressedSerializedData.Clear();
        // We need to convert the vector into a string
        std::string strDecompressedSerializedData = (const char *) stlDecompressedSerializedData.data();
        // Make sure to clear the original stlDecompressedSerializedData in order to free up memory
        stlDecompressedSerializedData.clear();
        // Now prepare to go through the table, row by row (i.e. string by string)
        std::stringstream stlTableStream(strDecompressedSerializedData);
        for (unsigned int unRowNumber = 0; unRowNumber < oDatasetTable.GetRowCount(); ++unRowNumber)
        {
            std::vector<std::string> stlOneRow;
            std::string strCurrentLine;
            std::getline(stlTableStream, strCurrentLine);
            std::stringstream stlCurrentLineStream(strCurrentLine);
            for (unsigned int unColumnNumber = 0; unColumnNumber < oDatasetTable.GetColumnCount(); ++unColumnNumber)
            {
                std::string strCell;
                std::getline(stlCurrentLineStream, strCell, '\x1f');
                stlOneRow.push_back(strCell);
            }
            stlIndividualTable.push_back(stlOneRow);
        }
        m_stlTableData.push_back(stlIndividualTable);
        // Also add table name to id in the cache map
        m_stlMapOfTableNameToId.insert(std::make_pair(oDatasetTable.GetTitle(), unTableIndex));
        // Increment the table index;
        unTableIndex++;
    }

    StructuredBuffer oEventData;
    oEventData.PutBoolean("Success", true);
    oEventData.PutString("DatasetFilename", m_poRootOfTrustNode->GetDatasetFilename());
    oEventData.PutStructuredBuffer("DatasetMetadata", m_oDatasetMetadata);
    m_poRootOfTrustNode->RecordAuditEvent("LOAD_DATASET", 0x1111, 0x05, oEventData);

    return true;
}

/********************************************************************************************
 *
 * @class DataConnector
 * @function HandleRequest
 * @brief Handle incoming requests for data from the research process
 * @return void
 * @note
 *     The method will stop taking in more requests on request to stop either from the
 *     Root oF Trust or the researcher itself.
 *
 ********************************************************************************************/

// TODO: implement lazy-loading for some requests
void __thiscall DataConnector::HandleRequest(
    _in Socket * poSocket
    ) const throw()
{
    __DebugFunction();
    __DebugAssert(nullptr != poSocket);

    try
    {
        std::vector<Byte> stlRequestBuffer = ::GetIpcTransaction(poSocket, true);
        if (0 < stlRequestBuffer.size())
        {
            // Respose Structured Buffer
            StructuredBuffer oDataResponse;
            StructuredBuffer oResearcherRequest(stlRequestBuffer);

            // Check the digital contract to check if the request is allowed
            bool fAllowed = this->FilterDataRequest(oResearcherRequest);

            // Get the table ID either from the table name provided or the table ID
            uint32_t unTableIndex;
            if (oResearcherRequest.IsElementPresent("TableID", UINT32_VALUE_TYPE))
            {
                unTableIndex = oResearcherRequest.GetUnsignedInt32("TableID");
            }
            else
            {
                std::string strTableName = oResearcherRequest.GetString("TableName");
                if (m_stlMapOfTableNameToId.end() != m_stlMapOfTableNameToId.find(strTableName))
                {
                    unTableIndex = m_stlMapOfTableNameToId.at(strTableName);
                }
                else
                {
                    oDataResponse.PutBoolean("Status", "Fail");
                    oDataResponse.PutString("ResponseString", "Invalid Table Name");
                    fAllowed = false;
                }
            }

            if (true == fAllowed)
            {
                uint8_t requestType = oResearcherRequest.GetInt8("RequestType");

                if (eGetRowRange == requestType)
                {
                    uint32_t unTableRowStart = oResearcherRequest.GetInt32("RowRangeStart");
                    uint32_t unTableRowEnd = oResearcherRequest.GetInt32("RowRangeEnd");
                    StructuredBuffer oTempResponse = GetTableRowRange(unTableIndex, unTableRowStart, unTableRowEnd);
                    oDataResponse.PutBoolean("Status", oTempResponse.GetBoolean("Status"));
                    oDataResponse.PutString("ResponseString", oTempResponse.GetString("ResponseString"));

                    StructuredBuffer oEventData;
                    oEventData.PutBoolean("Success", oTempResponse.GetBoolean("Status"));
                    oEventData.PutUnsignedInt32("TableIdentifier", unTableIndex);
                    oEventData.PutInt32("RowRangeStart", unTableRowStart);
                    oEventData.PutInt32("RowRangeStart", unTableRowEnd);
                    m_poRootOfTrustNode->RecordAuditEvent("DATASET_REQUEST_ROW_RANGE", 0x1100, 0x01, oEventData);
                }
                else if (eGetColumnRange == requestType)
                {
                    uint32_t unTableColumnStart = oResearcherRequest.GetInt32("ColumnRangeStart");
                    uint32_t unTableColumnEnd = oResearcherRequest.GetInt32("ColumnRangeEnd");
                    StructuredBuffer oTempResponse = GetTableColumnRange(unTableIndex, unTableColumnStart, unTableColumnEnd);
                    oDataResponse.PutBoolean("Status", oTempResponse.GetBoolean("Status"));
                    oDataResponse.PutString("ResponseString", oTempResponse.GetString("ResponseString"));

                    StructuredBuffer oEventData;
                    oEventData.PutBoolean("Success", oTempResponse.GetBoolean("Status"));
                    oEventData.PutUnsignedInt32("TableIdentifier", unTableIndex);
                    oEventData.PutInt32("ColumnRangeStart", unTableColumnStart);
                    oEventData.PutInt32("ColumnRangeEnd", unTableColumnEnd);
                    m_poRootOfTrustNode->RecordAuditEvent("DATASET_REQUEST_COLUMN_RANGE", 0x1100, 0x01, oEventData);
                }
                else if (eGetTable == requestType)
                {
                    StructuredBuffer oTempResponse = GetTableRowRange(unTableIndex, 0, m_stlTableMetaData[unTableIndex].GetUnsignedInt64("RowCount")-1);
                    oDataResponse.PutBoolean("Status", oTempResponse.GetBoolean("Status"));
                    oDataResponse.PutString("ResponseString", oTempResponse.GetString("ResponseString"));

                    StructuredBuffer oEventData;
                    oEventData.PutBoolean("Success", oTempResponse.GetBoolean("Status"));
                    oEventData.PutUnsignedInt32("TableIdentifier", unTableIndex);
                    m_poRootOfTrustNode->RecordAuditEvent("DATASET_REQUEST_TABLE", 0x1100, 0x01, oEventData);
                }
                else if (eGetDatasetMetadata == requestType)
                {
                    oDataResponse.PutBoolean("Status", true);
                    oDataResponse.PutStructuredBuffer("ResponseData", m_oDatasetMetadata);

                    m_poRootOfTrustNode->RecordAuditEvent("DATASET_GET_METADATA", 0x1100, 0x01, oDataResponse);
                }
                else if (eGetTableMetadata == requestType)
                {
                    oDataResponse.PutBoolean("Status", true);
                    oDataResponse.PutStructuredBuffer("ResponseData", m_stlTableMetaData[unTableIndex]);

                    m_poRootOfTrustNode->RecordAuditEvent("DATASET_TABLE_GET_METADATA", 0x1100, 0x01, oDataResponse);
                }
                else if (eCloseFile == requestType)
                {
                    oDataResponse.PutBoolean("Status", true);

                    m_poRootOfTrustNode->RecordAuditEvent("DATASET_CLOSE", 0x1100, 0x01, oDataResponse);
                }
                else if (eGetUuids == requestType)
                {
                    oDataResponse.PutBoolean("Status", true);
                    oDataResponse.PutStructuredBuffer("ResponseData", m_oAllDatasetIds);

                    m_poRootOfTrustNode->RecordAuditEvent("DATASET_TABLE_GET_GUID", 0x1100, 0x01, oDataResponse);
                }
                else
                {
                    // Do something for invalid rquest
                    oDataResponse.PutBoolean("Status", false);
                    oDataResponse.PutString("ResponseData", "Invalid Request Type");

                    m_poRootOfTrustNode->RecordAuditEvent("DATASET_INVALID_REQUEST", 0x1100, 0x02, oDataResponse);
                }
            }
            else
            {
                // Send a reply of invalid request
                oDataResponse.PutBoolean("Status", false);
                oDataResponse.PutString("ResponseData", "Permission Denied!!");
            }

            _ThrowBaseExceptionIf((false == ::PutIpcTransaction(poSocket, oDataResponse.GetSerializedBuffer())), "Write response failed.", nullptr);
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        std::cout << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl
                  << "\033[1;31m%s\033[0m" << c_oBaseException.GetExceptionMessage() << std::endl
                  << "\033[1;31mThrow from ->|File = \033[0m" << c_oBaseException.GetFilename() << std::endl
                  << "\033[1;31m             |Function = \033[0m" << c_oBaseException.GetFunctionName() << std::endl
                  << "\033[1;31m             |Line number = \033[0m" << c_oBaseException.GetLineNumber() << std::endl
                  << "\033[1;31mCaught in -->|File = \033[0m" << __FILE__ << std::endl
                  << "\033[1;31m             |Function = \033[0m" << __func__ << std::endl
                  << "\033[1;31m             |Line number = \033[0m" << __LINE__ << std::endl
                  << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl;
    }

    catch (...)
    {
        std::cout << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl
                  << "\033[1;31mOH NO, AN UNKNOWN EXCEPTION!!!\033[0m" << std::endl << std::endl
                  << "\033[1;31mCaught in -->|File = \033[0m" << __FILE__ << std::endl
                  << "\033[1;31m             |Function = \033[0m" << __func__ << std::endl
                  << "\033[1;31m             |Line number = \033[0m" << __LINE__ << std::endl
                  << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl;
    }
}

/********************************************************************************************
 *
 * @class DataConnector
 * @function GetTableRowRange
 * @brief Get a range of rows from the table CSV
 * @param[in] unTableIndex Table ID
 * @param[in] unStartRowNumber Starting Row number to fetch
 * @param[in] unEndRowNumber Last Row number to fetch
 * @return a StructuredBuffer of comma separated row enteries and request status
 *
 ********************************************************************************************/

StructuredBuffer __thiscall DataConnector::GetTableRowRange(
    _in unsigned int unTableIndex,
    _in unsigned int unStartRowNumber,
    _in unsigned int unEndRowNumber
    ) const
{
    __DebugFunction();

    StructuredBuffer oResponseStructuredBuffer;
    std::string strResponseString;

    if ((m_oDatasetMetadata.GetUnsignedInt32("TableCount") <= unTableIndex) || (m_stlTableMetaData[unTableIndex].GetUnsignedInt64("RowCount") <= unEndRowNumber) || (unStartRowNumber > unEndRowNumber))
    {
        oResponseStructuredBuffer.PutBoolean("Status", false);
        oResponseStructuredBuffer.PutString("ResponseString", "Out of Bounds Request");
    }
    else
    {
        for (unsigned int unRowNumber = unStartRowNumber; unRowNumber <= unEndRowNumber; unRowNumber++)
        {
            for (unsigned int unColumnNumber = 0; unColumnNumber < m_stlTableData[unTableIndex][unRowNumber].size(); unColumnNumber++)
            {
                if (unColumnNumber == (m_stlTableData[unTableIndex][unRowNumber].size() -1 ))
                {
                    strResponseString.append(m_stlTableData[unTableIndex][unRowNumber][unColumnNumber] + "\n");
                }
                else
                {
                    strResponseString.append(m_stlTableData[unTableIndex][unRowNumber][unColumnNumber] + "\x1f");
                }
            }
        }
        oResponseStructuredBuffer.PutBoolean("Status", true);
        oResponseStructuredBuffer.PutString("ResponseString", strResponseString);
    }

    return oResponseStructuredBuffer;
}

/********************************************************************************************
 *
 * @class DataConnector
 * @function GetTableColumnRange
 * @brief Get a range of columns from the table CSV
 * @param[in] unTableIndex Table ID
 * @param[in] unStartColumnNumber Starting Column number to fetch
 * @param[in] unEndColumnNumber Last Column number to fetch
 * @return a StructuredBuffer of comma separated column enteries and the request status
 *
 ********************************************************************************************/

StructuredBuffer __thiscall DataConnector::GetTableColumnRange(
    _in unsigned int unTableIndex,
    _in unsigned int unStartColumnNumber,
    _in unsigned int unEndColumnNumber
    ) const
{
    __DebugFunction();

    StructuredBuffer oResponseStructuredBuffer;
    std::string strResponseString;

    if ((m_oDatasetMetadata.GetInt32("NumberTables") <= static_cast<int>(unTableIndex)) || (m_stlTableMetaData[unTableIndex].GetInt32("NumberColumns") <= static_cast<int>(unEndColumnNumber)) || (unStartColumnNumber > unEndColumnNumber))
    {
        oResponseStructuredBuffer.PutBoolean("Status", false);
        oResponseStructuredBuffer.PutString("ResponseString", "Out of Bounds Request");
    }
    else
    {
        for (unsigned int unRowNumber = 0; unRowNumber < m_stlTableData[unTableIndex].size(); unRowNumber++)
        {
            for (unsigned int unColumnNumber = unStartColumnNumber; unColumnNumber <= unEndColumnNumber; unColumnNumber++)
            {
                if (unColumnNumber == unEndColumnNumber)
                {
                    strResponseString.append(m_stlTableData[unTableIndex][unRowNumber][unColumnNumber] + "\n");
                }
                else
                {
                    strResponseString.append(m_stlTableData[unTableIndex][unRowNumber][unColumnNumber] + "\x1f");
                }
            }
        }
        oResponseStructuredBuffer.PutBoolean("Status", true);
        oResponseStructuredBuffer.PutString("ResponseString", strResponseString);
    }

    return oResponseStructuredBuffer;
}

/********************************************************************************************
 *
 * @class DataConnector
 * @function FilterDataRequest
 * @brief Check the request params as per the digital contract and Dataset params
 * @param[in] oDataRequest StructuredBuffer containing the request from research process
 * @return true if values should be returned, else false
 *
 ********************************************************************************************/

bool __thiscall DataConnector::FilterDataRequest(
    _in StructuredBuffer oDataRequest
    ) const
{
    __DebugFunction();

    return true;
}
