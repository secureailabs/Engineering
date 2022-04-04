#include "64BitHashes.h"
#include "BinaryFileHandlers.h"
#include "CommandLine.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "JsonParser.h"
#include "Organization.h"

#include <iostream>

static std::string gs_strIpAddress;

/********************************************************************************************/

static void __stdcall PrintUsage(void)
{
    __DebugFunction();
    
    std::cout << "Usage: DatabaseInitializationTool --ip=<ipaddress> -settings=<json>" << std::endl
              << "   or: DatabaseInitializationTool --help" << std::endl << std::endl
              << "Where:" << std::endl
              << "       --ip,          IP address of SAIL Platform Services API Gateway." << std::endl
              << "       --settings,    Name of JSON file containing initialization values." << std::endl
              << "       --help,        Instructs the build tool to print these instructions." << std::endl;
}

/********************************************************************************************/

static void __stdcall LoadAndProcessJsonSettingsFile(
    _in const std::string & c_strJsonSettingsFilename
    )
{
    __DebugFunction();
    
    // Open the target JSON settings file
    BinaryFileReader oBinaryFileReader(c_strJsonSettingsFilename);
    // Read the entire file in one single call
    std::vector<Byte> stlJsonData = oBinaryFileReader.Read(oBinaryFileReader.GetSizeInBytes());
    StructuredBuffer oSettings = ::ConvertJsonStringToStructuredBuffer((const char *) stlJsonData.data());
    // There are two main portions to the JSON file. Organizations and Digital Contracts
    // Let's parse through all of the organization first. The names of each StructuredBuffer
    // element is the name of the organization.
    StructuredBuffer oOrganizations = oSettings.GetStructuredBuffer("Organizations");    
    std::vector<std::string> strListOfOrganizationNames = oOrganizations.GetNamesOfElements();
    for (const std::string c_strOrganizationName: strListOfOrganizationNames)
    {
        // Each element should be a StructuredBuffer, otherwise the application should throw
        // an exception and terminate. This is done automatically when calling GetStructuredBuffer()
        Organization oOrganization(oOrganizations.GetStructuredBuffer(c_strOrganizationName.c_str()));
        oOrganization.Register(gs_strIpAddress);
    }
    // Now that all of the organizations are registered, let's process the digital contracts
    StructuredBuffer oDigitalContracts = oSettings.GetStructuredBuffer("Digital Contracts");
    std::vector<std::string> strListOfDigitalContracts = oDigitalContracts.GetNamesOfElements();
    for (const std::string c_strDigitalContractIndex: strListOfDigitalContracts)
    {
        // Each element should be a StructuredBuffer, otherwise the application should throw
        // an exception and terminate. This is done automatically when calling GetStructuredBuffer()
        DigitalContract oDigitalContract(oDigitalContracts.GetStructuredBuffer(c_strDigitalContractIndex.c_str()));
        oDigitalContract.Register(gs_strIpAddress);
    }
}

/********************************************************************************************/

int __cdecl main(
    _in int nNumberOfArguments,
    _in const char ** pszCommandLineArguments
    )
{
    __DebugFunction();

    // By default
    int nReturnValue = -1;
    
    try
    {
        std::cout << "+=============================================================================================+" << std::endl;
        std::cout << "| Database Initialization Tool, Copyright (C) 2022 Secure AI Labs, Inc., All Rights Reserved. |" << std::endl;
        std::cout << "| by Luis Miguel Huapaya                                                                      |" << std::endl;
        std::cout << "+=============================================================================================+" << std::endl;
        // Parse the command line arguments if any exist   
        StructuredBuffer oCommandLineArguments(ParseCommandLineParameters(nNumberOfArguments, pszCommandLineArguments));
        // Now do some quick checks to see if we want to print usage or just cleanall
        if (true == oCommandLineArguments.IsElementPresent("help", BOOLEAN_VALUE_TYPE))
        {
            ::PrintUsage();
        }
        else
        {
            std::vector<std::string> stlNamesOfCommandLineParameters = oCommandLineArguments.GetNamesOfElements();
            // There should be precisely 2 command line parameters
            _ThrowBaseExceptionIf((2 != stlNamesOfCommandLineParameters.size()), "ERROR: Invalid command line arguments.", nullptr);
            _ThrowBaseExceptionIf((false == oCommandLineArguments.IsElementPresent("ip", ANSI_CHARACTER_STRING_VALUE_TYPE)), "ERROR: Invalid command line arguments.", nullptr);
            _ThrowBaseExceptionIf((false == oCommandLineArguments.IsElementPresent("settings", ANSI_CHARACTER_STRING_VALUE_TYPE)), "ERROR: Invalid command line arguments.", nullptr);
            
            // If we get here, all the command line arguments are proper. Let's save the IP address and then load the JSON file
            gs_strIpAddress = oCommandLineArguments.GetString("ip");
            // Load the JSON settings and process/register all of the setting data inside of it
            ::LoadAndProcessJsonSettingsFile(oCommandLineArguments.GetString("settings"));
        }
        
        // If we get here, everything worked, so the return value should be 0
        nReturnValue = 0;
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
    
    return nReturnValue;
}
