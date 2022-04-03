/*********************************************************************************************
 *
 * @file Main.cpp
 * @author Prawal Gangwar
 * @date 27 June 2020
 * @license Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "CommandLine.h"
#include "CoreTypes.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "StructuredBuffer.h"
#include "JobEngine.h"
#include "SocketClient.h"
#include "IpcTransactionHelperFunctions.h"
#include "Enums.h"

#include <iostream>

JobEngine JobEngine::m_oJobEngine;

/********************************************************************************************
 *
 * @function RegisterProcess
 * @brief Register a process with CommunicationPortal
 * @param[in] c_strProcessName Process name
 *
 ********************************************************************************************/

Socket * const __stdcall RegisterProcess(
    _in const std::string & c_strProcessName
)
{
    __DebugFunction();

    // Establish a connection and register with the Communication Module
    Socket * poSocket = ::ConnectToUnixDomainSocket(gc_strCommunicationPortalAddress);

    StructuredBuffer oStructuredBufferProcessInformation;
    oStructuredBufferProcessInformation.PutString("ProcessName", c_strProcessName);

    ::PutIpcTransaction(poSocket, oStructuredBufferProcessInformation);

    return poSocket;
}

int __cdecl main(
    _in int nNumberOfArguments,
    _in char ** pszCommandLineArguments
    )
{
    __DebugFunction();

    try
    {
        // Parse the command line
        StructuredBuffer oCommandLineArguments = ::ParseCommandLineParameters((unsigned int) nNumberOfArguments, (const char **) pszCommandLineArguments);

        // First we initialize the RootOfTrustNode. Without that, nothing else matters
        RootOfTrustNode * poRootOfTrustNode = new RootOfTrustNode(oCommandLineArguments.GetString("ipc").c_str());

        // Connect and Register to the Communication module for further communication
        std::cout << "Registering the JobEngine on Communication Server..." << std::endl;
        Socket * const poSocket = ::RegisterProcess("JobEngine");

        // Get the singleton object of the Job Engine
        JobEngine & oJobEngine = JobEngine::Get();
        oJobEngine.SetRootOfTrustNode(poRootOfTrustNode);
        oJobEngine.StartServer(poSocket);

        poRootOfTrustNode->Release();
    }
    
    catch (const BaseException & c_oBaseException)
    {
        std::cout << "JobEngine" << std::endl
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
        std::cout << "JobEngine" << std::endl
                  << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl
                  << "\033[1;31mOH NO, AN UNKNOWN EXCEPTION!!!\033[0m" << std::endl << std::endl
                  << "\033[1;31mCaught in -->|File = \033[0m" << __FILE__ << std::endl
                  << "\033[1;31m             |Function = \033[0m" << __func__ << std::endl
                  << "\033[1;31m             |Line number = \033[0m" << __LINE__ << std::endl
                  << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl;
    }

    return 0;
}
