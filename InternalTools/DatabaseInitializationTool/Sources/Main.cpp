#include "64BitHashes.h"
#include "BinaryFileHandlers.h"
#include "CommandLine.h"
#include "DebugLibrary.h"
#include "DigitalContract.h"
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
    
    std::cout << "Usage: DatabaseInitializationTool --ip=<ipaddress> --settings=<json> --step1" << std::endl
              << "   or: DatabaseInitializationTool --ip=<ipaddress> --settings=<json> --step2" << std::endl
              << "   or: DatabaseInitializationTool --ip=<ipaddress> --settings=<json> --allsteps" << std::endl
              << "   or: DatabaseInitializationTool --help" << std::endl << std::endl
              << "Where:" << std::endl
              << "       --ip,          IP address of SAIL Platform Services API Gateway." << std::endl
              << "       --settings,    Name of JSON file containing initialization values." << std::endl
              << "       --help,        Print these instructions." << std::endl
              << "       --step1,       Register organizations, users, administrators, dataset families and data federations." << std::endl
              << "       --step2,       Register datasets and digital contracts." << std::endl
              << "       --allsteps,    Registers everything." << std::endl;
}

/********************************************************************************************/

static void __stdcall LoadAndProcessJsonSettingsFile(
    _in const std::string & c_strJsonSettingsFilename,
    _in unsigned int unStepIdentifier
    )
{
    __DebugFunction();
    
    // Container used to keep track of the identifiers for each registered organization. This
    // will be needed when registering digital contracts (i.e. registering organizations
    // generated things like identifiers, etc..., and we need to keep track of then for when
    // we register digital contracts.
    std::unordered_map<Qword, Organization *> stlListOfOrganizationsByName;
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
    for (const std::string & c_strOrganizationName: strListOfOrganizationNames)
    {
        // Each element should be a StructuredBuffer, otherwise the application should throw
        // an exception and terminate. This is done automatically when calling GetStructuredBuffer()
        StructuredBuffer oOrganization(oOrganizations.GetStructuredBuffer(c_strOrganizationName.c_str()));
        Organization * poOrganization = new Organization(c_strOrganizationName, oOrganization);
        // Register the organization
        if (true == poOrganization->Register(gs_strIpAddress, 6200, unStepIdentifier))
        {
            // Keep track of the name-identifier tuple since it will be needed when registering
            // digital contracts
            stlListOfOrganizationsByName[::Get64BitHashOfNullTerminatedString(poOrganization->GetOrganizationalName().c_str(), false)] = poOrganization;
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
    // Register digital contracts, but only if we are not running step 1
    if ((2 == unStepIdentifier)||(3 == unStepIdentifier))
    {
        // Now that all of the organizations are registered, let's process the digital contracts
        StructuredBuffer oDigitalContracts = oSettings.GetStructuredBuffer("Digital Contracts");
        oDigitalContracts.RemoveElement("__IsArray__");
        std::vector<std::string> strListOfDigitalContracts = oDigitalContracts.GetNamesOfElements();
        for (const std::string & c_strDigitalContractIndex: strListOfDigitalContracts)
        {
            // Each element should be a StructuredBuffer, otherwise the application should throw
            // an exception and terminate. This is done automatically when calling GetStructuredBuffer()
            StructuredBuffer oDigitalContactParameters(oDigitalContracts.GetStructuredBuffer(c_strDigitalContractIndex.c_str()));
            // Figure out the organization identifiers for the two participants in the digital contract
            Qword qwHashOfDataOwnerOrganization = ::Get64BitHashOfNullTerminatedString(oDigitalContactParameters.GetString("DataOwnerOrganization").c_str(), false);
            Qword qwHashOfResearchOrganization = ::Get64BitHashOfNullTerminatedString(oDigitalContactParameters.GetString("ResearchOrganization").c_str(), false);
            // We are dealing with a dataset family. In the JSON specification, this will be the name of a dataset family
            // Let's point to the target data owner organization since we will need information out of that
            _ThrowBaseExceptionIf((stlListOfOrganizationsByName.end() == stlListOfOrganizationsByName.find(qwHashOfDataOwnerOrganization)), "ERROR: Unknown data owner organization %s specified in Digital Contract", oDigitalContactParameters.GetString("DataOwnerOrganization").c_str());
            Organization * poDataOwnerOrganization = stlListOfOrganizationsByName[qwHashOfDataOwnerOrganization];
            // We are dealing with a dataset family. In the JSON specification, this will be the name of a dataset family
            // Let's point to the target data owner organization since we will need information out of that
            _ThrowBaseExceptionIf((stlListOfOrganizationsByName.end() == stlListOfOrganizationsByName.find(qwHashOfResearchOrganization)), "ERROR: Unknown research organization %s specified in Digital Contract", oDigitalContactParameters.GetString("ResearchOrganization").c_str());
            Organization * poResearchOrganization = stlListOfOrganizationsByName[qwHashOfResearchOrganization];
            
            // Okay, let's register the digital contract.
            DigitalContract oDigitalContract(poDataOwnerOrganization, poResearchOrganization, oDigitalContactParameters);
            if (true == oDigitalContract.Register(gs_strIpAddress, 6200))
            {
                // Print out some information so that we can visibly see what just got registered
                std::cout << "Registered digital contract \"" << oDigitalContract.GetContractName() << "\"" << std::endl;
            }
            else
            {
                // Print out some information so that we can visibly see what just failed
                std::cout << "Failed to registered digital contract \"" << oDigitalContract.GetContractName() << "\"" << std::endl;
            }
        }
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
            _ThrowBaseExceptionIf((3 != stlNamesOfCommandLineParameters.size()), "ERROR: Invalid command line arguments.", nullptr);
            _ThrowBaseExceptionIf((false == oCommandLineArguments.IsElementPresent("ip", ANSI_CHARACTER_STRING_VALUE_TYPE)), "ERROR: Invalid command line arguments. No Ip address specified.", nullptr);
            _ThrowBaseExceptionIf((false == oCommandLineArguments.IsElementPresent("settings", ANSI_CHARACTER_STRING_VALUE_TYPE)), "ERROR: Invalid command line arguments. No Json file specified.", nullptr);
            _ThrowBaseExceptionIf(((false == oCommandLineArguments.IsElementPresent("step1", BOOLEAN_VALUE_TYPE))&&(false == oCommandLineArguments.IsElementPresent("step2", BOOLEAN_VALUE_TYPE))&&(false == oCommandLineArguments.IsElementPresent("allsteps", BOOLEAN_VALUE_TYPE))), "ERROR: Invalid command line arguments. No steps specified.", nullptr);
            // Figure out which step the tool will try and run
            unsigned int unStepIdentifier = 0;
            if (true == oCommandLineArguments.IsElementPresent("step1", BOOLEAN_VALUE_TYPE))
            {
                unStepIdentifier = 1;
            }
            else if (true == oCommandLineArguments.IsElementPresent("step2", BOOLEAN_VALUE_TYPE))
            {
                
                unStepIdentifier = 2;
            }
            else
            {
                __DebugAssert(true == oCommandLineArguments.IsElementPresent("allsteps", BOOLEAN_VALUE_TYPE));
                unStepIdentifier = 2;
            }
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
    
    return nReturnValue;
}
