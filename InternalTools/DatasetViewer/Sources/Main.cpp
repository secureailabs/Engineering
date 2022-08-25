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
#include "DatasetVersion.h"
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
    std::cout << "| DatasetVersionViewer, Copyright (C) 2022 Secure AI Labs, Inc., All Rights Reserved.         |" << std::endl;
    std::cout << "+======================================================================================+" << std::endl;
    std::cout << "Usage: DatasetVersionViewer --dataset <filename>" << std::endl;
    std::cout << "       DatasetVersionViewer --dataset <filename> --printdata" << std::endl;
    std::cout << "       DatasetVersionViewer --dataset <filename> --raw" << std::endl;
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
            std::string strDatasetVersionFilename = oCommandLineArguments.GetString("dataset");
            DatasetVersion oDatasetVersion(strDatasetVersionFilename.c_str());
                
            std::cout << "+======================================================================================+" << std::endl;
            std::cout << "| DatasetVersionViewer, Copyright (C) 2022 Secure AI Labs, Inc., All Rights Reserved.         |" << std::endl;
            std::cout << "+======================================================================================+" << std::endl;

            if (true == oCommandLineArguments.IsElementPresent("raw", BOOLEAN_VALUE_TYPE))
            {
                StructuredBuffer oDatasetVersionMetadata(oDatasetVersion.GetSerializedDatasetVersionMetadata());
                std::cout << oDatasetVersionMetadata.ToString() << std::endl;
            }
            else
            {
                std::cout << "| DatasetVersion Filename = " << strDatasetVersionFilename << std::endl;
                std::cout << "| Identifier = " << oDatasetVersion.GetDatasetVersionIdentifier() << std::endl;
                std::cout << "| Dataset Identifier = " << oDatasetVersion.GetDatasetIdentifier() << std::endl;
                std::cout << "| Publisher Identifier = " << oDatasetVersion.GetPublisherIdentifier() << std::endl;
                std::cout << "| Title = " << oDatasetVersion.GetTitle() << std::endl;
                std::cout << "| Description = " << oDatasetVersion.GetDescription() << std::endl;
                std::cout << "| Tags = " << oDatasetVersion.GetKeywords() << std::endl;
                std::cout << "| Creation Time/Date (UTC Epoch) = " << std::to_string(oDatasetVersion.GetPublishDate()) << std::endl;
                std::cout << "| Table Count = " << std::to_string(oDatasetVersion.GetNumberOfTables()) << std::endl;
                std::cout << "+======================================================================================+" << std::endl;
                // Now loop through all of the tables
                std::vector<std::string> stlListOfTables = oDatasetVersion.GetTableIdentifiers();
                for (const auto & c_strTableIdentifier: stlListOfTables)
                {
                    DatasetVersionTable oDatasetVersionTable = oDatasetVersion.GetDatasetVersionTable(c_strTableIdentifier.c_str());
                    std::cout << "Table Identifier = " << oDatasetVersionTable.GetTableIdentifier() << std::endl;
                    std::cout << "Title = " << oDatasetVersionTable.GetTitle() << std::endl;
                    std::cout << "Description = " << oDatasetVersionTable.GetDescription() << std::endl;
                    std::cout << "Tags = " << oDatasetVersionTable.GetTags() << std::endl;
                    std::cout << "Column Count = " << std::to_string(oDatasetVersionTable.GetColumnCount()) << std::endl;
                    std::cout << "Row Count = " << std::to_string(oDatasetVersionTable.GetRowCount()) << std::endl;
                    StructuredBuffer oInformationForDataAccess(oDatasetVersionTable.GetInformationForDataAccess());
                    std::cout << "Compressed Size In Bytes = " << std::to_string(oInformationForDataAccess.GetUnsignedInt64("CompressedSizeInBytes")) << std::endl;
                    std::cout << "Data Size In Bytes = " << std::to_string(oInformationForDataAccess.GetUnsignedInt64("data_size_in_bytes")) << std::endl;
                    std::cout << "Offset to first byte of compressed data = " << std::to_string(oInformationForDataAccess.GetUnsignedInt64("OffsetToFirstByteOfCompressedData")) << std::endl;
                    std::cout << "Filename = " << oInformationForDataAccess.GetString("DatasetVersionFilename") << std::endl << std::endl;
                    std::vector<std::string> stlListOfColumns = oDatasetVersionTable.GetColumnIdentifiers();
                    for (const std::string & c_strColumnIdentifier: stlListOfColumns)
                    {
                        DatasetVersionTableColumn oDatasetVersionTableColumn(oDatasetVersionTable.GetTableColumn(c_strColumnIdentifier.c_str()));
                        std::cout << "     Column Identifier = " << oDatasetVersionTableColumn.GetColumnIdentifier() << std::endl;
                        std::cout << "     Title = " << oDatasetVersionTableColumn.GetTitle() << std::endl;
                        std::cout << "     Description = " << oDatasetVersionTableColumn.GetDescription() << std::endl;
                        std::cout << "     Tags = " << oDatasetVersionTableColumn.GetTags() << std::endl;
                        std::cout << "     Units = " << oDatasetVersionTableColumn.GetUnits() << std::endl;
                        std::cout << "     Type = " << oDatasetVersionTableColumn.GetType() << std::endl << std::endl;
                    }

                    std::cout << "+======================================================================================+" << std::endl;
                }

                // Should we print the actual data? This prints a whole lot of crap
                if (true == oCommandLineArguments.IsElementPresent("printdata", BOOLEAN_VALUE_TYPE))
                {
                    for (const auto & c_strTableIdentifier: stlListOfTables)
                    {
                        DatasetVersionTable oDatasetVersionTable = oDatasetVersion.GetDatasetVersionTable(c_strTableIdentifier.c_str());
                        StructuredBuffer oInformationForDataAccess(oDatasetVersionTable.GetInformationForDataAccess());
                        BinaryFileReader oBinaryFileReader(oInformationForDataAccess.GetString("DatasetVersionFilename"));
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
