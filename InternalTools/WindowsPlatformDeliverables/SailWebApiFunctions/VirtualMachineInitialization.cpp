/*********************************************************************************************
 *
 * @file VirtualMachineInitialization.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Implementation of the Guid class that handles 128 bit (16 bytes) GUID/UUID values.
 *
 ********************************************************************************************/

#include <Windows.h>

#include "64BitHashes.h"
#include "Base64Encoder.h"
#include "CompressionHelperFunctions.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "JsonParser.h"
#include "RestApiHelperFunctions.h"
#include "SailApiBaseServices.h"
#include "StructuredBuffer.h"
#include "SmartMemoryAllocator.h"

#include <fstream>
#include <iostream>
#include <memory>
#include <mutex>
#include <thread>

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
extern "C" __declspec(dllexport) bool __cdecl UploadInstallationPackageToVirtualMachine(
    _in const char * c_szIpAddressOfVirtualMachine,
    _in const char * c_szBase64EncodedInstallationPackage
    )
{
    __DebugFunction();

    // [DllImport("SailWebApiPortalFunctions.dll", CallingConvention = CallingConvention.Cdecl )]
    // static extern public bool UploadInstallationPackageToVirtualMachine(string virtualMachineIpAddress, string base64EncodedInstallationPackage);

    bool fSuccess = false;

    try
    {
        _ThrowBaseExceptionIf((false == ::IsLoggedOn()), "Cannot upload installation package to a virtual machine while not logged on", nullptr);

        std::vector<std::string> stlHeaders;
        std::vector<Byte> stlResponse;
        unsigned int unLoopCounter = 120;
        do
        {
            stlResponse = ::RestApiCall(c_szIpAddressOfVirtualMachine, 9090, "POST", "/UploadData", c_szBase64EncodedInstallationPackage, true, stlHeaders);
            if (0 == stlResponse.size())
            {
                unLoopCounter -= 1;
                ::Sleep(5000);
            }
        }
        while ((0 <= unLoopCounter) && (0 == stlResponse.size()));

        fSuccess = true;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return fSuccess;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szNameOfVirtualMachine"></param>
/// <param name="c_szIpAddressOfVirtualMachine"></param>
/// <param name="c_szVirtualMachineIdentifier"></param>
/// <param name="c_szClusterIdentifier"></param>
/// <param name="c_szDigitalContractIdentifier"></param>
/// <param name="c_szDatasetIdentifier"></param>
/// <param name="c_szRootOfTrustDomainIdentifier"></param>
/// <param name="c_szComputationalDomainIdentifier"></param>
/// <param name="c_szDataConnectorDomainIdentifier"></param>
/// <param name="c_szSailWebApiPortalIpAddress"></param>
/// <param name="c_szBase64EncodedDataset"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) bool __cdecl UploadInitializationParametersToVirtualMachine(
    _in const char * c_szNameOfVirtualMachine,
    _in const char * c_szIpAddressOfVirtualMachine,
    _in const char * c_szVirtualMachineIdentifier,
    _in const char * c_szClusterIdentifier,
    _in const char * c_szDigitalContractIdentifier,
    _in const char * c_szDatasetIdentifier,
    _in const char * c_szRootOfTrustDomainIdentifier,
    _in const char * c_szComputationalDomainIdentifier,
    _in const char * c_szDataConnectorDomainIdentifier,
    _in const char * c_szSailWebApiPortalIpAddress,
    _in const char * c_szBase64EncodedDataset
    )
{
    __DebugFunction();

    // [DllImport("SailWebApiPortalFunctions.dll", CallingConvention = CallingConvention.Cdecl )]
    // static extern public bool UploadInitializationParametersToVirtualMachine(string nameOfVirtualMachine, string ipAddressOfVirtualMachine, string virtualMachineIdentifier, string clusterIdentifier, string digitalContractIdentifier, string datasetIdentifier, string rootOfTrustDomainIdentifier, string computationalDomainIdentifier, string dataConnectorDomainIdentifier, string ipAddressOfSailWebApiPortal, string base64EncodedDataset, string importorEosb);
    
    bool fSuccess = false;

    try
    {
        _ThrowBaseExceptionIf((false == ::IsLoggedOn()), "Cannot upload initialization parameters to a virtual machine while not logged on", nullptr);

        // First we need to build out the huge StructuredBuffer with all of the initialization parameters
        StructuredBuffer oInitializationParameters;
        oInitializationParameters.PutString("NameOfVirtualMachine", c_szNameOfVirtualMachine);
        oInitializationParameters.PutString("IpAddressOfVirtualMachine", c_szIpAddressOfVirtualMachine);
        oInitializationParameters.PutString("VirtualMachineIdentifier", c_szVirtualMachineIdentifier);
        oInitializationParameters.PutString("ClusterIdentifier", c_szClusterIdentifier);
        oInitializationParameters.PutString("DigitalContractIdentifier", c_szDigitalContractIdentifier);
        oInitializationParameters.PutString("DatasetIdentifier", c_szDatasetIdentifier);
        oInitializationParameters.PutString("RootOfTrustDomainIdentifier", c_szRootOfTrustDomainIdentifier);
        oInitializationParameters.PutString("ComputationalDomainIdentifier", c_szComputationalDomainIdentifier);
        oInitializationParameters.PutString("DataConnectorDomainIdentifier", c_szDataConnectorDomainIdentifier);
        oInitializationParameters.PutString("SailWebApiPortalIpAddress", c_szSailWebApiPortalIpAddress);
        oInitializationParameters.PutString("Base64EncodedDataset", c_szBase64EncodedDataset);
        oInitializationParameters.PutString("DataOwnerAccessToken", ::GetSailPlatformServicesEosb());
        oInitializationParameters.PutString("DataOwnerOrganizationIdentifier", ::GetSailPlatformServicesUserOrganizationIdentifier());
        oInitializationParameters.PutString("DataOwnerUserIdentifier", ::GetSailPlatformServicesUserIdentifier());
        // Now we blast out the transaction
        std::vector<std::string> stlHeaders;
        std::vector<Byte> stlRestResponse;

        unsigned int unLoopCounter = 120;
        do
        {
            stlRestResponse = ::RestApiCall(c_szIpAddressOfVirtualMachine, 6200, "POST", "/SAIL/InitializationParameters", oInitializationParameters.GetBase64SerializedBuffer(), true, stlHeaders);
            if (0 == stlRestResponse.size())
            {
                unLoopCounter -= 1;
                ::Sleep(5000);
            }
            else
            {
                 // Parse the returning value.
                 StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
                 // Did the transaction succeed?
                 _ThrowBaseExceptionIf(("Success" != oResponse.GetString("Status")), "Initialization has failed. %s", (const char*) stlRestResponse.data(),nullptr);
                 fSuccess = true;
            }
        } while ((0 <= unLoopCounter) && (false == fSuccess));
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return fSuccess;
}




