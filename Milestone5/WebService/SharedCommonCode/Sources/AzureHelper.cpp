/*********************************************************************************************
 *
 * @file AzureHelper.cpp
 * @author Prawal Gangwar
 * @date 28 July 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "DebugLibrary.h"
#include "Exceptions.h"
#include "CurlRest.h"
#include "StructuredBuffer.h"
#include "JsonValue.h"
#include "Utils.h"
#include "ExceptionRegister.h"

#include <iostream>
#include <sstream>
#include <vector>
#include <iostream>
#include <memory>
#include <algorithm>

#include <netdb.h>
#include <arpa/inet.h>
#include <unistd.h>

/********************************************************************************************
 *
 * @function CreateAzureParamterJson
 * @brief Function to create an Azure Template parameter json from the
 *        propvided StructuredBuffer
 * @param[in] c_strTemplateUrl Template schema url
 * @param[in] c_oStructuredBuffer Structured Buffer to fill the template
 * @return JSON string that woulb be passed on Azure
 *
 ********************************************************************************************/

std::string CreateAzureParamterJson(
    _in const std::string & c_strTemplateUrl,
    _in const StructuredBuffer & c_oStructuredBuffer
)
{
    __DebugFunction();

    std::string strResponse;

    StructuredBuffer oProperties;

    StructuredBuffer oTemplateLink;
    oTemplateLink.PutString("uri", c_strTemplateUrl);
    oProperties.PutStructuredBuffer("templateLink", oTemplateLink);

    StructuredBuffer oParameters;
    for (auto strElement : c_oStructuredBuffer.GetNamesOfElements())
    {
        StructuredBuffer oElement;
        oElement.PutString("value", c_oStructuredBuffer.GetString(strElement.c_str()));
        oParameters.PutStructuredBuffer(strElement.c_str(), oElement);
    }

    oProperties.PutStructuredBuffer("parameters", oParameters);
    oProperties.PutString("mode", "Incremental");

    StructuredBuffer oJson;
    oJson.PutStructuredBuffer("properties", oProperties);

    JsonValue * oOutput = JsonValue::ParseStructuredBufferToJson(oJson);
    strResponse = oOutput->ToString();
    oOutput->Release();

    return strResponse;
}

/********************************************************************************************
 *
 * @function GetJsonValue
 * @brief Function to get small json values which exist in the same line as the key
 * @param[in] strFullJsonString Json string to read the value from
 * @param[in] strKey Key for which the value is needed
 * @return Value corresponding to that key
 * @note This is not a perfect function to get a value form the Json object.
 *      This function would just find the first line with the key value in the format:
 *      "key" : "value"
 *      and return the value. This is the most that was needed in the Azure class.
 *      For other operation we would need a full-fledged Json Module.
 *
 ********************************************************************************************/

std::string __thiscall GetJsonValue(
    _in const std::string & strFullJsonString,
    _in const std::string & strKey
)
{
    __DebugFunction();

    std::string strLineWithKey;
    std::string strTempLine;
    std::istringstream oStringStream(strFullJsonString);
    while (std::getline(oStringStream, strTempLine))
    {
        if (strTempLine.find(strKey) != std::string::npos)
        {
            strLineWithKey = strTempLine;
            break;
        }
    }

    std::string strStartOfValue = strLineWithKey.substr(strLineWithKey.find(": \"")+3);
    return strStartOfValue.substr(0, strStartOfValue.find("\""));
}

/********************************************************************************************
 *
 * @function IsServerTimeoutError
 * @brief Function to
 * @param[in] strFullJsonString Json string to read the value from
 * @param[in] strKey Key for which the value is needed
 * @return Value corresponding to that key
 * @note This is not a perfect function to get a value form the Json object.
 *      This function would just find the first line with the key value in the format:
 *      "key" : "value"
 *      and return the value. This is the most that was needed in the Azure class.
 *      For other operation we would need a full-fledged Json Module.
 *
 ********************************************************************************************/

bool IsServerTimeoutError(
    _in const StructuredBuffer & c_oStructuredBuffer
)
{
    __DebugFunction();

    // The default behaviour is to consider the error as a timeout error
    // Will be changed if the error is not a timeout error
    bool fIsServerTimeoutError = true;

    if (true == c_oStructuredBuffer.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE))
    {
        StructuredBuffer oError = c_oStructuredBuffer.GetStructuredBuffer("error");
        if ("MultipleErrorsOccurred" == oError.GetString("code"))
        {
            StructuredBuffer oErrorDetails = oError.GetStructuredBuffer("details");
            for (auto strElement : oErrorDetails.GetNamesOfElements())
            {
                StructuredBuffer oElement = oErrorDetails.GetStructuredBuffer(strElement.c_str());
                if ("ServerTimeout" == oElement.GetString("code"))
                {
                    fIsServerTimeoutError = (fIsServerTimeoutError && true);
                }
                else
                {
                    fIsServerTimeoutError = (fIsServerTimeoutError && false);
                }
            }
        }
        else if ("ServerTimeout" == oError.GetString("code"))
        {
            fIsServerTimeoutError = true;
        }
        else
        {
            fIsServerTimeoutError = false;
        }
    }

    return fIsServerTimeoutError;
}

/********************************************************************************************
 *
 * @function CreateAzureResourceId
 * @brief Function to create an Azure format Id of a resource
 * @param[in] c_strSubscriptionIdentifier Subscription Id
 * @param[in] c_strResourceGroup Resource group where the resource is present
 * @param[in] c_strResourceProviderNamespace Resource provider namespace
 * @param[in] c_strResourceType Type of azure resource as defined on Azure
 * @param[in] c_strResourceName Name of the resource
 * @return Azure format resource id
 *
 ********************************************************************************************/

std::string CreateAzureResourceId(
    _in const std::string & c_strSubscriptionIdentifier,
    _in const std::string & c_strResourceGroup,
    _in const std::string & c_strResourceProviderNamespace,
    _in const std::string & c_strResourceType,
    _in const std::string & c_strResourceName
)
{
    __DebugFunction();

    std::string gc_strAzureIdFormat = "/subscriptions/{{SubscriptionUuid}}/resourceGroups/{{ResourceGroup}}/{{ResourceProvidernamespcae}}/{{ResourceType}}/{{ResourceName}}";

    ::ReplaceAll(gc_strAzureIdFormat, "{{SubscriptionUuid}}", c_strSubscriptionIdentifier);
    ::ReplaceAll(gc_strAzureIdFormat, "{{ResourceGroup}}", c_strResourceGroup);
    ::ReplaceAll(gc_strAzureIdFormat, "{{ResourceProvidernamespcae}}", c_strResourceProviderNamespace);
    ::ReplaceAll(gc_strAzureIdFormat, "{{ResourceType}}", c_strResourceType);
    ::ReplaceAll(gc_strAzureIdFormat, "{{ResourceName}}", c_strResourceName);

    return gc_strAzureIdFormat;
}

/********************************************************************************************
 *
 * @function ExecuteBashCommandAndGetResult
 * @brief Run a shell command and get the result as string
 * @param[in] c_szCommnadToRun Command to run
 * @return string result of the command that was run
 *
 ********************************************************************************************/

std::string ExecuteBashCommandAndGetResult(
    const char* c_szCommnadToRun
    )
{
    std::vector<char> strTempBuffer(1024);
    std::string result;

    auto oPopenPipe = ::popen(c_szCommnadToRun, "r");
    _ThrowIfNull(oPopenPipe, "Could not create shell process", nullptr);

    while (0 == ::feof(oPopenPipe))
    {
        if (nullptr != ::fgets(strTempBuffer.data(), 1024, oPopenPipe))
        {
            result += std::string(strTempBuffer.data());
        }
    }

    auto nExistStatus = ::pclose(oPopenPipe);
    if (EXIT_SUCCESS != nExistStatus)
    {
        result = "";
    }

    return result;
}

/********************************************************************************************
 *
 * @function AzureResourcesAssociatedWithVirtualMachine
 * @brief List of all the resources associated with the virtual machine
 * @param[in] c_strSubscriptionID Subscription id
 * @param[in] c_strResourceGroup Resource group
 * @param[in] c_strVirtualMachineName Virtual machine name
 * @return list of all the resources associsted with the provided virtual machine name
 *
 ********************************************************************************************/

std::vector<std::string> AzureResourcesAssociatedWithVirtualMachine(
    const std::string & c_strSubscriptionID,
    const std::string & c_strResourceGroup,
    const std::string & c_strVirtualMachineName
)
{
    __DebugFunction();

    std::vector<std::string> stlResponseListOfResourceIds;

    // VirtualMachineId
    stlResponseListOfResourceIds.push_back(::CreateAzureResourceId(c_strSubscriptionID, c_strResourceGroup, "providers/Microsoft.Compute", "virtualMachines", c_strVirtualMachineName));
    // OsDisk Id
    std::string strResourceGroupUpperCase = c_strResourceGroup;
    std::transform(strResourceGroupUpperCase.begin(), strResourceGroupUpperCase.end(),strResourceGroupUpperCase.begin(), ::toupper);
    stlResponseListOfResourceIds.push_back(::CreateAzureResourceId(c_strSubscriptionID, strResourceGroupUpperCase, "providers/Microsoft.Compute", "disks", c_strVirtualMachineName + "-disk"));
    // Network Interface Id
    stlResponseListOfResourceIds.push_back(::CreateAzureResourceId(c_strSubscriptionID, c_strResourceGroup, "providers/Microsoft.Network", "networkInterfaces", c_strVirtualMachineName + "-nic"));
    // IpAddressId
    stlResponseListOfResourceIds.push_back(::CreateAzureResourceId(c_strSubscriptionID, c_strResourceGroup, "providers/Microsoft.Network", "publicIPAddresses", c_strVirtualMachineName + "-ip"));

    return stlResponseListOfResourceIds;
}
