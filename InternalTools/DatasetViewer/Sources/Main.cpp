/*********************************************************************************************
 *
 * @file Main.cpp
 * @author Shabana Akhtar Baig
 * @date 24 March 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "BinaryFileHandlers.h"
#include "CommandLine.h"
#include "CompressionHelperFunctions.h"
#include "BinaryFileHandlers.h"
#include "Dataset.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "JsonParser.h"
#include "StructuredBuffer.h"

#include <iostream>

/********************************************************************************************/

static void __stdcall PrintUsage(void)
{
    __DebugFunction();
    
    std::cout << "+======================================================================================+" << std::endl;
    std::cout << "| DatasetViewer, Copyright (C) 2022 Secure AI Labs, Inc., All Rights Reserved.         |" << std::endl;
    std::cout << "+======================================================================================+" << std::endl;
    std::cout << "Usage: DatasetViewer --dataset <filename>" << std::endl;
    std::cout << "       DatasetViewer --dataset <filename> --printdata" << std::endl;
    std::cout << "       DatasetViewer --dataset <filename> --raw" << std::endl;
}

/********************************************************************************************/

static void __stdcall PrintData(
    _in const std::vector<Byte> & c_stlDecompressedSerializedData
    )
{
    for (const Byte & c_bCharacter: c_stlDecompressedSerializedData)
    {
        if (0x1F == c_bCharacter)
        {
            std::cout << ",";
        }
        else
        {
            std::cout << (char) c_bCharacter;
        }
    }
    std::cout << std::endl;
}

/********************************************************************************************/

int main(
    _in int nNumberOfArguments,
    _in char ** pszCommandLineArguments
    )
{
    __DebugFunction();

    try
    {
        // Parse the command line
        StructuredBuffer oCommandLineArguments = ::ParseCommandLineParameters((unsigned int) nNumberOfArguments, (const char **) pszCommandLineArguments);
        if (true != oCommandLineArguments.IsElementPresent("dataset", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            ::PrintUsage();
        }
        else
        {
            std::string strDatasetFilename = oCommandLineArguments.GetString("dataset");
            Dataset oDataset(strDatasetFilename.c_str());
                
            std::cout << "+======================================================================================+" << std::endl;
            std::cout << "| DatasetViewer, Copyright (C) 2022 Secure AI Labs, Inc., All Rights Reserved.         |" << std::endl;
            std::cout << "+======================================================================================+" << std::endl;

            if (true == oCommandLineArguments.IsElementPresent("raw", BOOLEAN_VALUE_TYPE))
            {
                StructuredBuffer oDatasetMetadata(oDataset.GetSerializedDatasetMetadata());
                std::cout << oDatasetMetadata.ToString() << std::endl;
            }
            else
            {
                std::cout << "| Dataset Filename = " << strDatasetFilename << std::endl;
                std::cout << "| Identifier = " << oDataset.GetDatasetIdentifier() << std::endl;
                std::cout << "| Dataset Family Identifier = " << oDataset.GetDatasetFamilyIdentifier() << std::endl;
                std::cout << "| Publisher Identifier = " << oDataset.GetPublisherIdentifier() << std::endl;
                std::cout << "| Title = " << oDataset.GetTitle() << std::endl;
                std::cout << "| Description = " << oDataset.GetDescription() << std::endl;
                std::cout << "| Tags = " << oDataset.GetKeywords() << std::endl;
                std::cout << "| Creation Time/Date (UTC Epoch) = " << std::to_string(oDataset.GetPublishDate()) << std::endl;
                std::cout << "| Table Count = " << std::to_string(oDataset.GetNumberOfTables()) << std::endl;
                std::cout << "+======================================================================================+" << std::endl;
                // Now loop through all of the tables
                std::unordered_map<std::string, int> stlListOfTables = oDataset.GetTableIdentifiers();
                for (const auto & c_strTableIdentifier: stlListOfTables)
                {
                    DatasetTable oDatasetTable = oDataset.GetDatasetTable(c_strTableIdentifier.first.c_str());
                    std::cout << "Table Identifier = " << oDatasetTable.GetTableIdentifier() << std::endl;
                    std::cout << "Title = " << oDatasetTable.GetTitle() << std::endl;
                    std::cout << "Description = " << oDatasetTable.GetDescription() << std::endl;
                    std::cout << "Tags = " << oDatasetTable.GetTags() << std::endl;
                    std::cout << "Column Count = " << std::to_string(oDatasetTable.GetColumnCount()) << std::endl;
                    std::cout << "Row Count = " << std::to_string(oDatasetTable.GetRowCount()) << std::endl;
                    StructuredBuffer oInformationForDataAccess(oDatasetTable.GetInformationForDataAccess());
                    std::cout << "Compressed Size In Bytes = " << std::to_string(oInformationForDataAccess.GetUnsignedInt64("CompressedSizeInBytes")) << std::endl;
                    std::cout << "Data Size In Bytes = " << std::to_string(oInformationForDataAccess.GetUnsignedInt64("data_size_in_bytes")) << std::endl;
                    std::cout << "Offset to first byte of compressed data = " << std::to_string(oInformationForDataAccess.GetUnsignedInt64("OffsetToFirstByteOfCompressedData")) << std::endl;
                    std::cout << "Filename = " << oInformationForDataAccess.GetString("DatasetFilename") << std::endl << std::endl;
                    std::vector<std::string> stlListOfColumns = oDatasetTable.GetColumnIdentifiers();
                    for (const std::string & c_strColumnIdentifier: stlListOfColumns)
                    {
                        DatasetTableColumn oDatasetTableColumn(oDatasetTable.GetTableColumn(c_strColumnIdentifier.c_str()));
                        std::cout << "     Column Identifier = " << oDatasetTableColumn.GetColumnIdentifier() << std::endl;
                        std::cout << "     Title = " << oDatasetTableColumn.GetTitle() << std::endl;
                        std::cout << "     Description = " << oDatasetTableColumn.GetDescription() << std::endl;
                        std::cout << "     Tags = " << oDatasetTableColumn.GetTags() << std::endl;
                        std::cout << "     Units = " << oDatasetTableColumn.GetUnits() << std::endl;
                        std::cout << "     Type = " << oDatasetTableColumn.GetType() << std::endl << std::endl;
                    }

                    std::cout << "+======================================================================================+" << std::endl;
                }

                // Should we print the actual data? This prints a whole lot of crap
                if (true == oCommandLineArguments.IsElementPresent("printdata", BOOLEAN_VALUE_TYPE))
                {
                    for (const auto & c_strTableIdentifier: stlListOfTables)
                    {
                        DatasetTable oDatasetTable = oDataset.GetDatasetTable(c_strTableIdentifier.first.c_str());
                        StructuredBuffer oInformationForDataAccess(oDatasetTable.GetInformationForDataAccess());
                        BinaryFileReader oBinaryFileReader(oInformationForDataAccess.GetString("DatasetFilename"));
                        oBinaryFileReader.Seek(eFromBeginningOfFile, oInformationForDataAccess.GetUnsignedInt64("OffsetToFirstByteOfCompressedData"));
                        std::vector<Byte> stlCompressedSerializedData = oBinaryFileReader.Read(oInformationForDataAccess.GetUnsignedInt64("CompressedSizeInBytes"));
                        StructuredBuffer oCompressedSerializedData(stlCompressedSerializedData);
                        std::vector<Byte> stlDecompressedSerializedData = ::DecompressStructuredBuffer(oCompressedSerializedData);
                        ::PrintData(stlDecompressedSerializedData);
                    }
                }
            }
        }
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    // Print out any lingered exceptions before exiting
    while (0 < ::GetRegisteredExceptionsCount())
    {
        std::string strRegisteredException = ::GetNextRegisteredException();
        std::cout << strRegisteredException << std::endl << std::endl;
    }

    return 0;
}
