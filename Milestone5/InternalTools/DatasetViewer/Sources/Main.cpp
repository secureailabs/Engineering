/*********************************************************************************************
 *
 * @file Main.cpp
 * @author Shabana Akhtar Baig
 * @date 24 March 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "CommandLine.h"
#include "CompressionHelperFunctions.h"
#include "BinaryFileHandlers.h"
#include "Dataset.h"
#include "DebugLibrary.h"
#include "Exceptions.h"

#include <iostream>

/********************************************************************************************/

static void __stdcall PrintUsage(void)
{
    __DebugFunction();
    
    std::cout << "+======================================================================================+" << std::endl;
    std::cout << "| DatasetViewer, Copyright (C) 2022 Secure AI Labs, Inc., All Rights Reserved.         |" << std::endl;
    std::cout << "+======================================================================================+" << std::endl;
    std::cout << "Usage: DatasetViewer.exe --dataset <filename>" << std::endl;
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
            std::cout << "| Dataset Filename = " << strDatasetFilename << std::endl;
            std::cout << "| Identifier = " << oDataset.GetDatasetIdentifier() << std::endl;
            std::cout << "| Dataset Family Identifier = " << oDataset.GetDatasetFamilyIdentifier() << std::endl;
            std::cout << "| Publisher Identifier = " << oDataset.GetPublisherIdentifier() << std::endl;
            std::cout << "| Title = " << oDataset.GetTitle() << std::endl;
            std::cout << "| Description = " << oDataset.GetDescription() << std::endl;
            std::cout << "| Tags = " << oDataset.GetTags() << std::endl;
            std::cout << "| Creation Time/Date (UTC Epoch) = " << std::to_string(oDataset.GetEpochCreationTimeInSeconds()) << std::endl;
            std::cout << "| Table Count = " << std::to_string(oDataset.GetTableCount()) << std::endl;
            std::cout << "+======================================================================================+" << std::endl;
            // Now loop through all of the tables
            std::vector<std::string> stlListOfTables = oDataset.GetTableIdentifiers();
            for (std::string strTableIdentifier: stlListOfTables)
            {
                DatasetTable oDatasetTable = oDataset.GetDatasetTable(strTableIdentifier.c_str());
                std::cout << "Table Identifier = " << oDatasetTable.GetTableIdentifier() << std::endl;
                std::cout << "Title = " << oDatasetTable.GetTitle() << std::endl;
                std::cout << "Description = " << oDatasetTable.GetDescription() << std::endl;
                std::cout << "Tags = " << oDatasetTable.GetTags() << std::endl;
                std::cout << "Column Count = " << std::to_string(oDatasetTable.GetColumnCount()) << std::endl;
                std::cout << "Row Count = " << std::to_string(oDatasetTable.GetRowCount()) << std::endl;
                StructuredBuffer oInformationForDataAccess(oDatasetTable.GetInformationForDataAccess());
                std::cout << "Compressed Size In Bytes = " << std::to_string(oInformationForDataAccess.GetUnsignedInt64("CompressedSizeInBytes")) << std::endl;
                std::cout << "Data Size In Bytes = " << std::to_string(oInformationForDataAccess.GetUnsignedInt64("DataSizeInBytes")) << std::endl;
                std::cout << "Offset to first byte of compressed data = " << std::to_string(oInformationForDataAccess.GetUnsignedInt64("OffsetToFirstByteOfCompressedData")) << std::endl;
                std::cout << "Filename = " << oInformationForDataAccess.GetString("DatasetFilename") << std::endl << std::endl;
                std::vector<std::string> stlListOfColumns = oDatasetTable.GetColumnIdentifiers();
                for (std::string strColumnIdentifier: stlListOfColumns)
                {
                    DatasetTableColumn oDatasetTableColumn(oDatasetTable.GetTableColumn(strColumnIdentifier.c_str()));
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
                for (std::string strTableIdentifier: stlListOfTables)
                {
                    DatasetTable oDatasetTable = oDataset.GetDatasetTable(strTableIdentifier.c_str());
                    StructuredBuffer oInformationForDataAccess(oDatasetTable.GetInformationForDataAccess());
                    BinaryFileReader oBinaryFileReader(oInformationForDataAccess.GetString("DatasetFilename"));
                    oBinaryFileReader.Seek(eFromBeginningOfFile, oInformationForDataAccess.GetUnsignedInt64("OffsetToFirstByteOfCompressedData"));
                    std::vector<Byte> stlCompressedSerializedData = oBinaryFileReader.Read(oInformationForDataAccess.GetUnsignedInt64("CompressedSizeInBytes"));
                    StructuredBuffer oCompressedSerializedData(stlCompressedSerializedData);
                    std::vector<Byte> stlDecompressedSerializedData = ::DecompressStructuredBuffer(oCompressedSerializedData);
                    std::cout << (const char *) stlDecompressedSerializedData.data() << std::endl;
                }
            }
        }
    }
    
    catch (const BaseException & c_oBaseException)
    {
        std::cout << "Exception: " << std::endl;
        std::cout << c_oBaseException.GetExceptionMessage() << std::endl;
    }
    
    catch (...)
    {
        std::cout << "Error: Unknown exception caught." << std::endl;
    }

    return 0;
}