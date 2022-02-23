/*********************************************************************************************
 *
 * @file Main.cpp
 * @author Prawal Gangwar
 * @date 23 Feb 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "DemoDatabase.h"
#include "ConsoleInputHelperFunctions.h"
#include "CommandLine.h"

#include "getopt.h"

static const char * gsc_szPrintableCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789`~!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/";
static const char * gsc_szIpAddressCharacters = "0123456789.";

// struct containing valid command line options
struct option Options[] = {
    {"create-vm", no_argument, NULL, 'a'},
    {"delete-db", no_argument, NULL, 'd'},
    {NULL, 0, NULL, 0}
};

/********************************************************************************************/

int main(
    _in int nNumberOfArguments,
    _in char ** pszCommandLineArguments
    )
{
    __DebugFunction();

    // Parse the command line
    StructuredBuffer oCommandLineArguments = ::ParseCommandLineParameters((unsigned int) nNumberOfArguments, (const char **) pszCommandLineArguments);
    std::cout << oCommandLineArguments.ToString() << std::endl;

    // Get the IP Address of the SAIL WebPortal. It could either be present
    // as a commnad line argument or be provided separately
    std::string strIpAddress = "";
    unsigned int unPortNumber = 0;
    if (true == oCommandLineArguments.IsElementPresent("PortalIp", ANSI_CHARACTER_STRING_VALUE_TYPE))
    {
        strIpAddress = oCommandLineArguments.GetString("PortalIp");
        if (true == oCommandLineArguments.IsElementPresent("Port", ANSI_CHARACTER_STRING_VALUE_TYPE))
        {
            unPortNumber = std::stoi(oCommandLineArguments.GetString("Port"));
        }
        else
        {
            std::cout << "Port option missing!! --PortalIp=<Ip address> --Port=<port number> [--a create-vm] [--d delete-db]\n";
        }
    }
    else
    {
        strIpAddress = ::GetStringInput("PortalIpAddress: ", 64, false, gsc_szIpAddressCharacters);
        unPortNumber = std::stoi(::GetStringInput("Port: ", 64, false, gsc_szIpAddressCharacters));
    }

    bool fRegisterVm = false, fDeleteDb = false;
    if (true == oCommandLineArguments.IsElementPresent("a", BOOLEAN_VALUE_TYPE))
    {
        fRegisterVm = true;
    }

    if (true == oCommandLineArguments.IsElementPresent("d", BOOLEAN_VALUE_TYPE))
    {
        fDeleteDb = true;
    }

    if (true == oCommandLineArguments.IsElementPresent("help", BOOLEAN_VALUE_TYPE))
    {
        std::cout << "DemoDatabase --PortalIp=<Ip address> --Port=<port number> [--a create-vm] [--d delete-db]\n";
    }

    try
    {
        DemoDatabase oDemoDatabase(strIpAddress.c_str(), unPortNumber);
        if (true == fDeleteDb)
        {
            // Delete database
            oDemoDatabase.DeleteDatabase();
            std::cout << "Database deleted!" << std::endl;
        }
        else
        {
            // Add organizations and their super admins
            oDemoDatabase.AddOrganizationsAndSuperAdmins();
            // Add Dataset Families
            oDemoDatabase.AddDatasetFamilies();
            // Register dataset metadata
            oDemoDatabase.AddDatasets();
            // Register digital contracts for the organizations
            oDemoDatabase.AddDigitalContracts();
            // Accept digital contracts
            oDemoDatabase.AcceptDigitalContracts();
            // Activate digital contracts
            oDemoDatabase.ActivateDigitalContracts();
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
