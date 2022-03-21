/*********************************************************************************************
 *
 * @file AzureHelper.h
 * @author Prawal Gangwar
 * @date 28 July 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "CoreTypes.h"
#include "StructuredBuffer.h"

#include <string>

std::string __stdcall CreateAzureParamterJson(
    _in const std::string & c_strTemplateUrl,
    _in const StructuredBuffer & c_oStructuredBuffer
    );

std::string __stdcall CreateAzureResourceId(
    _in const std::string & c_strSubscriptionIdentifier,
    _in const std::string & c_strResourceGroup,
    _in const std::string & c_strResourceProviderNamespace,
    _in const std::string & c_strResourceType,
    _in const std::string & c_strResourceName
    );

bool __stdcall DoesAzureResourceExist(
    _in const std::string & c_strMicrosoftAzureAccessToken,
    _in const std::string & c_strResourceId
    );

std::string __stdcall LoginToMicrosoftAzureApiPortal(
    _in const std::string & c_szApplicationIdentifier,
    _in const std::string & c_szSecret,
    _in const std::string & c_szTenantIdentifier
    ) throw();

StructuredBuffer __stdcall CreateAzureDeployment(
    _in const std::string & c_strAzureAccessToken,
    _in const std::string & c_strdeploymentParameters,
    _in const std::string & c_strSubscriptionIdentifier,
    _in const std::string & c_strResourceGroup,
    _in const std::string & c_strLocation
    ) throw();

StructuredBuffer __stdcall CopyVirtualMachineImage(
    _in const std::string c_strMicrosoftAzureAccessToken,
    _in const std::string c_strSubscriptionId,
    _in const std::string c_strResourceGroupName,
    _in const std::string c_strLocation,
    _in const std::string c_strImageName
    ) throw();

StructuredBuffer __stdcall DeployVirtualMachineAndWait(
    _in const std::string & c_strApplicationIdentifier,
    _in const std::string & c_strSecret,
    _in const std::string & c_strTenantIdentifier,
    _in const std::string & c_strSubscriptionIdentifier,
    _in const std::string & c_strResourceGroup,
    _in const std::string & c_strVirtualMachineIdentifier,
    _in const std::string & c_strconfidentialVirtualMachineSpecification,
    _in const std::string & c_strLocation
    ) throw();

bool __stdcall DeleteAzureResourceGroup(
    _in const std::string & c_strApplicationIdentifier,
    _in const std::string & c_strTenantIdentifier,
    _in const std::string & c_strSecret,
    _in const std::string & c_strSubscriptionIdentifier,
    _in const std::string & c_stlResourceGroupName
    );

std::vector<std::string> __stdcall AzureResourcesAssociatedWithVirtualMachine(
    const std::string & c_strSubscriptionID,
    const std::string & c_strResourceGroup,
    const std::string & c_strVirtualMachineName
    );

std::string __thiscall __stdcall GetJsonValue(
    _in const std::string & strFullJsonString,
    _in const std::string & strKey
    );

std::string __stdcall ExecuteBashCommandAndGetResult(
    const char* c_szCommnadToRun
    );

bool __stdcall IsServerTimeoutError(
    _in const StructuredBuffer & c_oStructuredBuffer
    );
