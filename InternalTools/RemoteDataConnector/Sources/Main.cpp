/*********************************************************************************************
 *
 * @file Main.cpp
 * @author Prawal Gangwar
 * @date 13 May 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
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
#include "SailPlatformServicesSession.h"
#include "CurlRest.h"
#include "FileUtils.h"
#include "Base64Encoder.h"

#include <iostream>
#include <filesystem>
#include <unistd.h>


/********************************************************************************************/
void InfiniteLoop(
    _in const std::string & c_strIpAddress,
    _in int nPort,
    _in const std::string & c_strUsername,
    _in const std::string & c_strPassword,
    _in const StructuredBuffer & c_oRequestHeartbeat,
    _in const std::unordered_map<std::string, std::string> c_stlMapOfIdToFiles
)
{
    __DebugFunction();

    // Login
    SailPlatformServicesSession oSailPlatformServicesSession(c_strIpAddress, nPort);
    oSailPlatformServicesSession.Login(c_strUsername, c_strPassword);

    std::string strJsonRequest = ::ConvertStructuredBufferToJson(c_oRequestHeartbeat);

    while (true)
    {
        // Request heartbeat
        std::string strVerb = "POST";
        std::string strApiUri = "/remote-data-connectors/";
        std::vector<std::string> stlListOfHeaders;
        stlListOfHeaders.push_back("Authorization: Bearer " + oSailPlatformServicesSession.GetAccessToken());
        stlListOfHeaders.push_back("Content-Type: application/json");
        stlListOfHeaders.push_back("accept: application/json");

        // Send the REST API call to the SAIL Web Api Portal
        auto stlRestResponse = ::RestApiCall(c_strIpAddress, (Word)8000, strVerb, strApiUri, strJsonRequest, true, stlListOfHeaders);
        std::cout << "stlRestResponse " << stlRestResponse.data() << std::endl;
        _ThrowBaseExceptionIf((0 == stlRestResponse.size()), "Failed to get response from SAIL Web Api Portal", nullptr);

        // Parse the returning value.
        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
        StructuredBuffer oWaitingSecureComputationNodes = oResponse.GetStructuredBuffer("secure_computation_nodes");

        _ThrowBaseExceptionIf((false == oWaitingSecureComputationNodes.IsElementPresent("__IsArray__", BOOLEAN_VALUE_TYPE)), "Invalid response from server", nullptr);
        if (false == oWaitingSecureComputationNodes.IsElementPresent("__IsEmpty__", BOOLEAN_VALUE_TYPE))
        {
            auto stlListOfWaitingSecureComputationNodes = oWaitingSecureComputationNodes.GetNamesOfElements();
            for (const std::string & c_strScn : stlListOfWaitingSecureComputationNodes)
            {
                if (("__IsArray__" == c_strScn) || ("__IsEmpty__" == c_strScn))
                {
                    continue;
                }

                StructuredBuffer oWaitingSecureComputationNode = oWaitingSecureComputationNodes.GetStructuredBuffer(c_strScn.c_str());
                std::string strIp = oWaitingSecureComputationNode.GetString("ipaddress");
                std::string strDatasetVersionId = oWaitingSecureComputationNode.GetString("dataset_id");
                _ThrowBaseExceptionIf(c_stlMapOfIdToFiles.find(strDatasetVersionId) == c_stlMapOfIdToFiles.end(), "DatasetVersion not found", nullptr);
                std::string strFileName = c_stlMapOfIdToFiles.at(strDatasetVersionId);
                _ThrowBaseExceptionIf((false == std::filesystem::exists(strFileName)), "Failed to find file %s",  strFileName.c_str(), nullptr);

                // Upload the dataset
                std::cout << "Uploading dataset " << strDatasetVersionId << " to " << strIp << std::endl;

                // Extract some basic information
                StructuredBuffer oVirtualMachineInformation;

                std::vector<Byte> stlDatasetVersionFiledata = ::ReadFileAsByteBuffer(strFileName);
                std::string strEncoded = ::Base64Encode(stlDatasetVersionFiledata.data(), (unsigned int)stlDatasetVersionFiledata.size());
                oVirtualMachineInformation.PutString("Base64EncodedDatasetVersion", strEncoded);
                oVirtualMachineInformation.PutString("DataOwnerAccessToken", oSailPlatformServicesSession.GetAccessToken());
                oVirtualMachineInformation.PutString("SailWebApiPortalIpAddress", c_strIpAddress);
                oVirtualMachineInformation.PutString("DataOwnerUserIdentifier", oSailPlatformServicesSession.GetBasicUserInformation().GetString("id"));
                oVirtualMachineInformation.PutString("DataOwnerOrganizationIdentifier", oSailPlatformServicesSession.GetBasicUserInformation().GetStructuredBuffer("organization").GetString("id"));
                // Prepare the JSON string
                std::string strJson = ::ConvertStructuredBufferToJson(oVirtualMachineInformation);
                // Execute the upload transaction
                auto stlRestResponse = ::RestApiCall(strIp, (Word) 6800, "PUT", "/something", strJson, false);
            }
        }

        // send data to waiting SCNs
        sleep(60);
    }
}

/********************************************************************************************/

static void __stdcall PrintUsage(void)
{
    __DebugFunction();

    std::cout << "+========================================================================================+" << std::endl;
    std::cout << "| Remote Data Connector, Copyright (C) 2022 Secure AI Labs, Inc., All Rights Reserved.   |" << std::endl;
    std::cout << "+=====================================================================--=================+" << std::endl;
    std::cout << "Usage: Remote Data Connector --ip <api_service> --port <api_service_port> --user <username> --password <password> --folder <foldername>" << std::endl;
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
        std::unordered_map<std::string, std::string> stlMapOfIdToFiles;
        StructuredBuffer oRequestHeartbeat;
        StructuredBuffer oDatasetVersions;
        // Parse the command line
        StructuredBuffer oCommandLineArguments = ::ParseCommandLineParameters((unsigned int) nNumberOfArguments, (const char **) pszCommandLineArguments);
        if (false == oCommandLineArguments.IsElementPresent("folder", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            ::PrintUsage();
        }
        else if (false == oCommandLineArguments.IsElementPresent("user", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            ::PrintUsage();
        }
        else if (false == oCommandLineArguments.IsElementPresent("ip", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            ::PrintUsage();
        }
        else if (false == oCommandLineArguments.IsElementPresent("port", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            ::PrintUsage();
        }
        else if (false == oCommandLineArguments.IsElementPresent("password", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            ::PrintUsage();
        }
        else
        {
            std::string strDatasetVersionFolder = oCommandLineArguments.GetString("folder");
            std::string strUsername = oCommandLineArguments.GetString("user");
            std::string strPassword = oCommandLineArguments.GetString("password");
            std::string strIpAddress = oCommandLineArguments.GetString("ip");
            int wPortNumber = std::atoi(oCommandLineArguments.GetString("port").c_str());

            int nDatasetVersionCount = 0;
            oDatasetVersions.PutBoolean("__IsArray__", true);
            if(true == std::filesystem::exists(strDatasetVersionFolder))
            {
                // Look at all the files in the folder
                for (const auto & entry : std::filesystem::directory_iterator(strDatasetVersionFolder))
                {
                    DatasetVersion oDatasetVersion(entry.path().c_str());
                    std::cout << "Identifier = " << oDatasetVersion.GetDatasetVersionIdentifier() << " for " << entry.path() << std::endl;
                    oDatasetVersions.PutString(std::to_string(nDatasetVersionCount).c_str(), oDatasetVersion.GetDatasetVersionIdentifier());

                    stlMapOfIdToFiles.insert(std::make_pair(oDatasetVersion.GetDatasetVersionIdentifier(), entry.path()));
                    nDatasetVersionCount++;
                }
            }
            oRequestHeartbeat.PutStructuredBuffer("datasets", oDatasetVersions);

            ::InfiniteLoop(strIpAddress, wPortNumber, strUsername, strPassword, oRequestHeartbeat, stlMapOfIdToFiles);
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
