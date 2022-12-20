#include "64BitHashes.h"
#include "BinaryFileHandlers.h"
#include "CommandLine.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "JsonParser.h"
#include "Organization.h"
#include "SailPlatformServicesSession.h"

#include <filesystem>
#include <iostream>

#include <libgen.h>         // dirname
#include <unistd.h>         // readlink, chdir
#include <linux/limits.h>   // PATH_MAX

static std::string gs_strIpAddress;

/********************************************************************************************/

static void __stdcall PrintUsage(void)
{
    __DebugFunction();
    
    std::cout << "Usage: DatabaseInitializationTool --ip=<ipaddress> --settings=<json> --step1" << std::endl
              << "   or: DatabaseInitializationTool --ip=<ipaddress> --settings=<json> --step2" << std::endl
              << "   or: DatabaseInitializationTool --ip=<ipaddress> --settings=<json> --step3" << std::endl
              << "   or: DatabaseInitializationTool --ip=<ipaddress> --settings=<json> --allsteps" << std::endl
              << "   or: DatabaseInitializationTool --help" << std::endl << std::endl
              << "Where:" << std::endl
              << "       --ip,          IP address of SAIL Platform Services API Gateway." << std::endl
              << "       --settings,    Name of JSON file containing initialization values." << std::endl
              << "       --help,        Print these instructions." << std::endl
              << "       --step1,       Register organizations, users, administrators, data federations." << std::endl
              << "       --step2,       Register datasets" << std::endl
              << "       --allsteps,    Registers everything (i.e. step1 + step 2)." << std::endl;
}

/********************************************************************************************/

static void __stdcall LoadAndProcessJsonSettingsFile(
    _in const std::string & c_strJsonSettingsFilename,
    _in unsigned int unStepIdentifier
    )
{
    __DebugFunction();
    _ThrowBaseExceptionIf((false == std::filesystem::exists(c_strJsonSettingsFilename)), "ERROR: JSON specification file not found (%s)", c_strJsonSettingsFilename.c_str());

    // Reset the database, but only if we are registering organizations
    if ((1 == unStepIdentifier)||(4 == unStepIdentifier))
    {
        SailPlatformServicesSession oSailPlatformServicesSession(gs_strIpAddress, 8000);
        oSailPlatformServicesSession.ResetDatabase();
        std::cout << "Database has been reset" << std::endl;
    }
    // Container used to keep track of the identifiers for each registered organization. This
    // will be needed when registering digital contracts (i.e. registering organizations
    // generated things like identifiers, etc..., and we need to keep track of then for when
    // we register digital contracts.
    std::unordered_map<std::string, Organization *> stlListOfOrganizationsByName;
    // Open the target JSON settings file
    BinaryFileReader oBinaryFileReader(c_strJsonSettingsFilename);
    // Read the entire file in one single call
    std::vector<Byte> stlJsonData = oBinaryFileReader.Read(oBinaryFileReader.GetSizeInBytes());
    // Convert the input file into a StructuredBuffer
    StructuredBuffer oSettings = ::ConvertJsonStringToStructuredBuffer((const char *) stlJsonData.data());
    // There are two main portions to the JSON file. Organizations and Digital Contracts
    // Let's parse through all of the organization first. The names of each StructuredBuffer
    // element is the name of the organization.
    StructuredBuffer oOrganizations = oSettings.GetStructuredBuffer("Organizations");
    std::vector<std::string> strListOfOrganizationNames = oOrganizations.GetNamesOfElements();
    std::unordered_map<std::string, Guid> stlRegisteredFederations;
    // Register organizations. Based on the step index, this will either:
    //  1 --> Register the organization
    //  2 --> Register the datasets
    //  3 --> Register nothing
    //  4 --> Register the organization and then the datasets
    for (const std::string & c_strOrganizationName: strListOfOrganizationNames)
    {
        // Each element should be a StructuredBuffer, otherwise the application should throw
        // an exception and terminate. This is done automatically when calling GetStructuredBuffer()
        StructuredBuffer oOrganization(oOrganizations.GetStructuredBuffer(c_strOrganizationName.c_str()));
        Organization * poOrganization = new Organization(c_strOrganizationName, oOrganization, unStepIdentifier);
        // Register the organization
        if (true == poOrganization->Register(gs_strIpAddress, 8000, unStepIdentifier, stlRegisteredFederations))
        {
            // Keep track of the name-identifier tuple since it will be needed when registering
            // digital contracts
            stlListOfOrganizationsByName[poOrganization->GetOrganizationalName()] = poOrganization;
            // Print out some information so that we can visibly see what just got registered
            std::cout << "Registered organization \"" << poOrganization->GetOrganizationalName() << "\" which was given identifier " << poOrganization->GetOrganizationalIdentifier() << std::endl;
        }
        else
        {
            // Print out some information so that we can visibly see what just failed
            std::cout << "Failed to registered organization \"" << poOrganization->GetOrganizationalName() << "\"" << std::endl;
            // Make sure to delete the organization object since it won't be used
            poOrganization->Release();
        }
    }

    // Register anything that needs an organization identifier. This will register Data Submitters and Researchers
    if ((2 == unStepIdentifier)||(3 == unStepIdentifier)||(4 == unStepIdentifier))
    {
        // Assign data submitters and researcher to our data federations
        for ( auto organization : stlListOfOrganizationsByName )
        {
            organization.second->RegisterFederationDataSubmitters(gs_strIpAddress, 8000, stlListOfOrganizationsByName);
            organization.second->RegisterFederationResearchers(gs_strIpAddress, 8000, stlListOfOrganizationsByName);
        }
    }
}

/********************************************************************************************/

static unsigned int GetStep(
    _in const StructuredBuffer & c_oCommandLineParameters
    )
{
    __DebugFunction();

    unsigned int unStepIdentifier = 0;

    if (true == c_oCommandLineParameters.IsElementPresent("step1", BOOLEAN_VALUE_TYPE))
    {
        unStepIdentifier = 1;
    }
    else if (true == c_oCommandLineParameters.IsElementPresent("step2", BOOLEAN_VALUE_TYPE))
    {

        unStepIdentifier = 2;
    }
    else if (true == c_oCommandLineParameters.IsElementPresent("step3", BOOLEAN_VALUE_TYPE))
    {

        unStepIdentifier = 3;
    }
    else
    {
        __DebugAssert(true == c_oCommandLineParameters.IsElementPresent("allsteps", BOOLEAN_VALUE_TYPE));
        unStepIdentifier = 4;
    }

    return unStepIdentifier;
}

/********************************************************************************************/

static std::string __stdcall GetExecutableFolder(void) throw()
{
    __DebugFunction();

    std::string strExecutableFolder;
    char szExecutableFullPathName[PATH_MAX] = { 0 };
    if (-1 != ::readlink("/proc/self/exe", szExecutableFullPathName, PATH_MAX))
    {
        strExecutableFolder = ::dirname(szExecutableFullPathName);
    }

    return strExecutableFolder;
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
    std::string strStartingFolder = std::filesystem::current_path();

    try
    {
        // Change the working folder to be that of the executable
        ::chdir(::GetExecutableFolder().c_str());

        // Now run the tool
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
            _ThrowBaseExceptionIf((3 != stlNamesOfCommandLineParameters.size()), "ERROR: Invalid command line arguments.", nullptr);
            _ThrowBaseExceptionIf((false == oCommandLineArguments.IsElementPresent("ip", ANSI_CHARACTER_STRING_VALUE_TYPE)), "ERROR: Invalid command line arguments. No Ip address specified.", nullptr);
            _ThrowBaseExceptionIf((false == oCommandLineArguments.IsElementPresent("settings", ANSI_CHARACTER_STRING_VALUE_TYPE)), "ERROR: Invalid command line arguments. No Json file specified.", nullptr);
            _ThrowBaseExceptionIf(((false == oCommandLineArguments.IsElementPresent("step1", BOOLEAN_VALUE_TYPE))&&(false == oCommandLineArguments.IsElementPresent("step2", BOOLEAN_VALUE_TYPE))&&(false == oCommandLineArguments.IsElementPresent("allsteps", BOOLEAN_VALUE_TYPE))), "ERROR: Invalid command line arguments. No steps specified.", nullptr);
            // Figure out which step the tool will try and run
            unsigned int unStepIdentifier = ::GetStep(oCommandLineArguments);
            // If we get here, all the command line arguments are proper. Let's save the IP address and then load the JSON file
            gs_strIpAddress = oCommandLineArguments.GetString("ip");
            // Load the JSON settings and process/register all of the setting data inside of it
            ::LoadAndProcessJsonSettingsFile(oCommandLineArguments.GetString("settings"), unStepIdentifier);
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

    // Make sure to return to the starting folder before exiting
    ::chdir(strStartingFolder.c_str());

    return nReturnValue;
}