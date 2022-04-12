/*********************************************************************************************
 *
 * @file Main.cpp
 * @author Prawal Gangwar
 * @date 27 January 2022
 * @license Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "CoreTypes.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ConsoleInputHelperFunctions.h"
#include "StructuredBuffer.h"
#include "FileUtils.h"
#include "TlsClient.h"
#include "TlsTransactionHelperFunctions.h"
#include "CommandLine.h"

#include <iostream>
#include <vector>
#include <iostream>
#include <fstream>
#include <memory>

static const char * gsc_szPrintableCharacters = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789`~!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/";
static const char * gsc_szIpAddressCharacters = "0123456789.";

static const std::string gsc_strTarPackageFile = "package.tar.gz";
static const std::string gsc_strInitializationVectorFile = "InitializationVector.json";

void PrintHelp(void)
{
    __DebugFunction();

    std::cout << "Usage: UploadPackageAndInitializationVector --IpAddress=<Virtual Machine IP> --Package=<Tar Package Path> --InitializationVector=<InitializationVector Path> " << std::endl;
    ::exit(1);
}

void UploadPackage(
    _in std::string & c_strVirtualMachineIpAddress,
    _in std::string & c_strPackageFile,
    _in std::string & c_strInitializationVector
    )
{
    __DebugFunction();

    Guid oSafeObjectGuid;

    // Read the package file and initialization vector file as binary data
    std::vector<Byte> stlPackageFileData = ::ReadFileAsByteBuffer(c_strPackageFile);
    std::string strInitializationVectorFileData = ::ReadFileAsString(c_strInitializationVector);

    StructuredBuffer oStructuredBuffer;
    oStructuredBuffer.PutBuffer(gsc_strTarPackageFile.c_str(), stlPackageFileData);
    oStructuredBuffer.PutString(gsc_strInitializationVectorFile.c_str(), strInitializationVectorFileData);

    // Connect to the Virtual Machine
    std::unique_ptr<TlsNode> poTlsNode(::TlsConnectToNetworkSocketWithTimeout(c_strVirtualMachineIpAddress.c_str(), 9090, 5*60*1000, 5000));
    _ThrowIfNull(poTlsNode, "Cannot establish connection.", nullptr);

    // Send the package and initialization vector data to the Virtual Machine
    std::vector<Byte> stlSendPackageResponse = ::PutTlsTransactionAndGetResponse(poTlsNode.get(), oStructuredBuffer, 0);
    _ThrowBaseExceptionIf((0 >= stlSendPackageResponse.size()), "Invalid reponse to send package instructions.", nullptr);
    StructuredBuffer oSendPackageResponse(stlSendPackageResponse);
    _ThrowBaseExceptionIf(("Success" != oSendPackageResponse.GetString("Status")), "Sending package failed", nullptr);

    std::cout << "Package sent successfully" << oSendPackageResponse.ToString() << std::endl;
}

/********************************************************************************************/

int __cdecl main(
    int nNumberOfArguments,
    char ** pszCommandLineArguments
    )
{
    __DebugFunction();

    try
    {
        // Parse the command line
        StructuredBuffer oCommandLineArguments = ::ParseCommandLineParameters((unsigned int) nNumberOfArguments, (const char **) pszCommandLineArguments);
        std::string strVirtualMachineIpAddress;
        std::string strPackageFile;
        std::string strInitializationVector;

        if (nNumberOfArguments < 2)
        {
            strVirtualMachineIpAddress = ::GetStringInput("Virtual Machine Ip Address : ", 64, false, gsc_szIpAddressCharacters);
            strPackageFile = ::GetStringInput("Package file : ", 64, false, gsc_szPrintableCharacters);
            strInitializationVector = ::GetStringInput("InitializationVector file : ", 64, false, gsc_szPrintableCharacters);
        }
        else
        {
            // The other option is when the dataset is already located some folder in
            // the filesystem and can be used directly by the DataConnector

            std::cout << oCommandLineArguments.ToString() << std::endl;
            // Read the IP Address of the Virtual Machine
            if (true == oCommandLineArguments.IsElementPresent("IpAddress", ANSI_CHARACTER_STRING_VALUE_TYPE))
            {
                strVirtualMachineIpAddress = oCommandLineArguments.GetString("IpAddress");
            }
            else
            {
                ::PrintHelp();
            }

            // Read the location of the package file
            if (true == oCommandLineArguments.IsElementPresent("Package", ANSI_CHARACTER_STRING_VALUE_TYPE))
            {
                strPackageFile = oCommandLineArguments.GetString("Package");
            }
            else
            {
                ::PrintHelp();
            }

            // Read the location of the initialization vector file
            if (true == oCommandLineArguments.IsElementPresent("InitializationVector", ANSI_CHARACTER_STRING_VALUE_TYPE))
            {
                strInitializationVector = oCommandLineArguments.GetString("InitializationVector");
            }
            else
            {
                ::PrintHelp();
            }
        }

        ::UploadPackage(strVirtualMachineIpAddress, strPackageFile, strInitializationVector);
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

    catch (const std::exception & c_oBaseException)
    {
        std::cout << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl
                  << "\033[1;31m%s\033[0m" << c_oBaseException.what() << std::endl
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

    return 0;
}
