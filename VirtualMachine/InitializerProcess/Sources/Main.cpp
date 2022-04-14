/*********************************************************************************************
 *
 * @file Main.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @license Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "Base64Encoder.h"
#include "BinaryFileHandlers.h"
#include "CommandLine.h"
#include "CoreTypes.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "HardCodedCryptographicKeys.h"
#include "SocketTransactionHelperFunctions.h"
#include "IpcTransactionHelperFunctions.h"
#include "SocketServer.h"
#include "SocketClient.h"
#include "StructuredBuffer.h"
#include "JsonValue.h"
#include "InitializationVector.h"

#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <fstream>
#include <memory>

/********************************************************************************************/

static std::vector<Byte> __stdcall WaitForInitializationParameters(void)
{
    __DebugFunction();

    StructuredBuffer oAllInitializationParameters;

    // Read the initialization parameters from the InitializationVector.json file
    oAllInitializationParameters.PutString("VirtualMachineName", ::GetInitializationValue("NameOfVirtualMachine"));
    oAllInitializationParameters.PutString("VirtualMachineIpAddress", ::GetInitializationValue("IpAddressOfVirtualMachine"));
    oAllInitializationParameters.PutString("VirtualMachineIdentifier", ::GetInitializationValue("VirtualMachineIdentifier"));
    oAllInitializationParameters.PutString("VirtualMachineClusterIdentifier", ::GetInitializationValue("ClusterIdentifier"));
    oAllInitializationParameters.PutString("DigitalContractIdentifier", ::GetInitializationValue("DigitalContractIdentifier"));
    oAllInitializationParameters.PutString("DatasetIdentifier", ::GetInitializationValue("DatasetIdentifier"));
    oAllInitializationParameters.PutString("DataDomainIdentifier", ::GetInitializationValue("DataConnectorDomainIdentifier"));
    oAllInitializationParameters.PutString("RootOfTrustDomainIdentifier", ::GetInitializationValue("RootOfTrustDomainIdentifier"));
    oAllInitializationParameters.PutString("ComputationalDomainIdentifier", ::GetInitializationValue("ComputationalDomainIdentifier"));
    oAllInitializationParameters.PutString("DataConnectorDomainIdentifier", ::GetInitializationValue("DataConnectorDomainIdentifier"));
    oAllInitializationParameters.PutString("VmEosb", ::GetInitializationValue("VmEosb"));

    // Next step is to wait for the dataset from the Remote data connector, the process will wait for the dataset
    // and dataOwner information
    SocketServer oSocketServer(6800);
    while (false == oSocketServer.WaitForConnection(1000))
    {
        // Put the thread into efficient sleep to give a chance for the other process
        // to connect. This reduces thread contention.
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }

    // The second connection are the initialization parameters sent from the
    // Remote data connector which has information about the dataowner and the dataset
    std::unique_ptr<Socket> poSocket(oSocketServer.Accept());
    _ThrowBaseExceptionIf((nullptr == poSocket), "Unexpected nullptr returned from oSocketServer.Accept()", nullptr);

    auto stlDatasetParameters = ::GetSocketTransaction(poSocket.get(), 60*60*1000);
    _ThrowBaseExceptionIf((0 == stlDatasetParameters.size()), "Unexpected empty dataset parameters", nullptr);

    std::string stlDatasetFilename = "//tmp//" + Guid().ToString(eHyphensOnly) + ".csvp";
    StructuredBuffer oRemoteDatasetParameters(stlDatasetParameters);
    oAllInitializationParameters.PutString("DataOwnerEosb", ::UnEscapeJsonString(oRemoteDatasetParameters.GetString("DataOwnerAccessToken").c_str()));
    oAllInitializationParameters.PutString("SailWebApiPortalIpAddress", oRemoteDatasetParameters.GetString("SailWebApiPortalIpAddress"));
    oAllInitializationParameters.PutString("DataOwnerUserIdentifier", oRemoteDatasetParameters.GetString("DataOwnerUserIdentifier"));
    oAllInitializationParameters.PutString("DataOwnerOrganizationIdentifier", oRemoteDatasetParameters.GetString("DataOwnerOrganizationIdentifier"));
    oAllInitializationParameters.PutString("DatasetFilename", stlDatasetFilename);
    // At this point, we need to extract the Base64 encoded dataset and write the contents to a file on disk, since it's\033
    // possible for the dataset to be very big, so passing this along in memory would create multiple copies of a large
    // dataset in memory.
    // TODO: In the future, we should deliver the dataset in chunk instead of trying to put everything into memory. This
    // needs to be done at the Data Annocation Tool level (i.e. a single table is actually compressed in separate chunks)
    std::vector<Byte> stlUnencodedData = ::Base64Decode(::UnEscapeJsonString(oRemoteDatasetParameters.GetString("Base64EncodedDataset")).c_str());
    BinaryFileWriter oBinaryFileWriter(stlDatasetFilename);
    oBinaryFileWriter.Write(stlUnencodedData);
    // Now return the status to the caller
    StructuredBuffer oStructuredBufferResponse;
    oStructuredBufferResponse.PutString("Status", "Success");
    ::PutSocketTransaction(poSocket.get(), oStructuredBufferResponse.GetSerializedBuffer());

    return oAllInitializationParameters.GetSerializedBuffer();
}

/********************************************************************************************/

static void __stdcall InitializeRootOfTrust(
    _in const char * c_szIpcPathForInitialization,
    _in const std::vector<Byte> & c_oSerializedInitializationParameters
    )
{
    __DebugFunction();

    StructuredBuffer oInitializationData(c_oSerializedInitializationParameters);
    Socket * poSocket = ::ConnectToUnixDomainSocket(c_szIpcPathForInitialization);
    (void) ::PutIpcTransaction(poSocket, oInitializationData);
    poSocket->Release();
}

/********************************************************************************************/

int __cdecl main(
    _in int nNumberOfArguments,
    _in char ** pszCommandLineArguments
    )
{
    __DebugFunction();

    try
    {
        std::cout << ">>> Initializer process" << std::endl;
        // Parse the command line
        StructuredBuffer oCommandLineArguments = ::ParseCommandLineParameters((unsigned int) nNumberOfArguments, (const char **) pszCommandLineArguments);
        // First we wait for the initialization parameters
        std::vector<Byte> stdInitializationParameters = ::WaitForInitializationParameters();
        // Now we initialize the RootOfTrustNode. Without that, we will not know how to
        // communicate securely back to the RootOfTrust to initialize it.
        ::InitializeRootOfTrust(oCommandLineArguments.GetString("ipc").c_str(), stdInitializationParameters);
        std::cout << "<<< Initializer process" << std::endl;
    }

    catch (const BaseException & c_oBaseException)
    {
        std::cout << "InitializerProcess" << std::endl
                  << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl
                  << "\033[1;31m%s\033[0m" << c_oBaseException.GetExceptionMessage() << std::endl
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
        std::cout << "InitializerProcess" << std::endl
                  << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl
                  << "\033[1;31mOH NO, AN UNKNOWN EXCEPTION!!!\033[0m" << std::endl << std::endl
                  << "\033[1;31mCaught in -->|File = \033[0m" << __FILE__ << std::endl
                  << "\033[1;31m             |Function = \033[0m" << __func__ << std::endl
                  << "\033[1;31m             |Line number = \033[0m" << __LINE__ << std::endl
                  << "\r\033[1;31m---------------------------------------------------------------------------------\033[0m" << std::endl;
    }

    return 0;
}
