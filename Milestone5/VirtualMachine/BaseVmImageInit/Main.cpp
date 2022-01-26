/*********************************************************************************************
 *
 * @file Main.cpp
 * @author Prawal Gangwar
 * @date 09 March 2021
 * @license Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "CoreTypes.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "StructuredBuffer.h"
#include "TlsServer.h"
#include "TlsTransactionHelperFunctions.h"
#include "FileUtils.h"

#include <iostream>
#include <filesystem>

const std::string gc_strTarPackageFile = "package.tar.gz";
const std::string gc_strInitializationVectorFile = "InitializationVector.json";

/********************************************************************************************
 *
 * @function InitVirtualMachine
 * @brief Download the files and execute them on the Virtual Machine
 *
 ********************************************************************************************/

void __stdcall InitVirtualMachine()
{
    __DebugFunction();

    TlsServer oTlsServer(9090);

    StructuredBuffer oResponseStructuredBuffer;
    oResponseStructuredBuffer.PutString("Status", "Fail");

    bool fSuccess = false;
    while (false == fSuccess)
    {
        std::unique_ptr<TlsNode> poTlsNode(nullptr);
        try
        {
            // We will first try to download all the incoming package data that needs to be installed
            // on the VM and if this fails we try again.
            if (true == oTlsServer.WaitForConnection(1000))
            {
                std::cout << "New Connection" << std::endl;
                poTlsNode.reset(oTlsServer.Accept());
                _ThrowIfNull(poTlsNode, "Cannot establish connection.", nullptr);

                // Fetch the serialized Structure Buffer from the remote
                std::vector<Byte> stlPayload = ::GetTlsTransaction(poTlsNode.get(), 60 * 60 * 1000);
                _ThrowBaseExceptionIf((0 == stlPayload.size()), "Bad Initialization data", nullptr);

                StructuredBuffer oFilesStructuredBuffer(stlPayload);
                // Read the package tarball and write it to the filesystem
                ::WriteBytesAsFile(gc_strTarPackageFile, oFilesStructuredBuffer.GetBuffer(gc_strTarPackageFile.c_str()));
                // Read the initialization vector and write it to the filesystem
                ::WriteStringAsFile(gc_strInitializationVectorFile, oFilesStructuredBuffer.GetString(gc_strInitializationVectorFile.c_str()));

                oResponseStructuredBuffer.PutString("Status", "Success");
                fSuccess = true;
            }
        }

        catch (const BaseException & c_oBaseException)
        {
            oResponseStructuredBuffer.PutString("Status", "Fail");
            oResponseStructuredBuffer.PutString("Error", c_oBaseException.GetExceptionMessage());
        }

        catch (const std::exception & c_oException)
        {
            oResponseStructuredBuffer.PutString("Status", "Fail");
            oResponseStructuredBuffer.PutString("Error", c_oException.what());
        }

        // We again try to send the Status response to the initializer tool so that it could know if the
        // package was installed correctly without any error. But we don't want to risk a failure of this process
        // while that happens and some exception occurs.
        try
        {
            // Send the resposnse to the Remote Initializer Tool
            // There is a chance that this transaction may fail but in that case, we will continue to the run the
            // virtual machine and exit the init process and leave it on the discretion of the initialization tool
            if (nullptr != poTlsNode)
            {
                bool fResponseStatus = ::PutTlsTransaction(poTlsNode.get(), oResponseStructuredBuffer);
            }
        }
        catch(...)
        {
            std::cout << "Unexpected Error while sending init response.";
        }
    }
}

/********************************************************************************************/

int main(
    _in int nNumberOfArguments,
    _in char **pszCommandLineArguments)
{
    __DebugFunction();

    bool fSuccess = false;

    try
    {
        // Call the function only if the package and Initialization Vector are not present
        if (false == std::filesystem::exists(gc_strTarPackageFile) && false == std::filesystem::exists(gc_strInitializationVectorFile))
        {
            ::InitVirtualMachine();
            fSuccess = true;
        }
        else if (false == std::filesystem::exists(gc_strTarPackageFile) || false == std::filesystem::exists(gc_strInitializationVectorFile))
        {
            _ThrowSimpleException("Missing package.tar.gz or InitializationVector.json");
        }
        else
        {
            std::cout << "Files already present.. Continuing.." << std::endl;
            fSuccess = true;
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        std::cout << "Bootstrap" << std::endl
                  << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl
                  << "\033[1;31m" << c_oBaseException.GetExceptionMessage() << "\033[0m" << std::endl
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
        std::cout << "Bootstrap" << std::endl
                  << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl
                  << "\033[1;31mOH NO, AN UNKNOWN EXCEPTION!!!\033[0m" << std::endl
                  << std::endl
                  << "\033[1;31mCaught in -->|File = \033[0m" << __FILE__ << std::endl
                  << "\033[1;31m             |Function = \033[0m" << __func__ << std::endl
                  << "\033[1;31m             |Line number = \033[0m" << __LINE__ << std::endl
                  << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl;
    }

    int nReturnCode = 0;
    if (false == fSuccess)
    {
        nReturnCode = 1;
    }

    return nReturnCode;
}
