/*********************************************************************************************
 *
 * @file AzureApiCalls.cpp
 * @author Prawal Gangwar
 * @date 22 November 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "AzureHelper.h"
#include "DebugLibrary.h"
#include "CurlRest.h"
#include "JsonValue.h"
#include "ExceptionRegister.h"
#include "InitializationVector.h"

#include <algorithm>

#include <unistd.h>

/********************************************************************************************
 *
 * @function LoginToMicrosoftAzureApiPortal
 * @brief Function to get small json values which exist in the same line as the key
 * @param[in] c_szApplicationIdentifier Json string to read the value from
 * @param[in] c_szSecret Key for which the value is needed
 * @param[in] c_szTenantIdentifier Key for which the value is needed
 * @return Value corresponding to that key
 * @note
 *
 ********************************************************************************************/

std::string __stdcall LoginToMicrosoftAzureApiPortal(
    _in const std::string & c_szApplicationIdentifier,
    _in const std::string & c_szSecret,
    _in const std::string & c_szTenantIdentifier
    ) throw()
{
    __DebugFunction();

    std::string strAccessToken = "";

    try
    {
        // Build out the API call components
        std::string strVerb = "POST";
        std::string strApiUri = "/" + std::string(c_szTenantIdentifier) + "/oauth2/token";
        std::string strApiContentBody = "grant_type=client_credentials&client_id=" + std::string(c_szApplicationIdentifier) + "&client_secret=" + std::string(c_szSecret) + "&resource=https://management.core.windows.net/";
        std::vector<std::string> stlHeader;
        stlHeader.push_back("Content-Type: application/x-www-form-urlencoded");
        stlHeader.push_back("Accept: */*");
        std::vector<Byte> stlResponse = ::RestApiCall("login.microsoftonline.com", 443, strVerb, strApiUri, strApiContentBody, false, stlHeader);
        StructuredBuffer oMicrosoftAzureResponse = JsonValue::ParseDataToStructuredBuffer((const char*) stlResponse.data());
        _ThrowBaseExceptionIf((false == oMicrosoftAzureResponse.IsElementPresent("access_token", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Microsoft Azure authentication failed. Response JSON is:\r\n%s", (const char *) oMicrosoftAzureResponse.ToString().c_str());
        strAccessToken = oMicrosoftAzureResponse.GetString("access_token");
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return strAccessToken;
}

/********************************************************************************************
 *
 * @function MakeMicrosoftAzureApiCall
 * @brief Function to get small json values which exist in the same line as the key
 * @param[in] c_strMicrosoftAzureAccessToken Azure access token
 * @param[in] c_strVerb HTTP request verb
 * @param[in] c_strResource Azure resource for which the request is being made for
 * @param[in] c_strHost azure domain name to be called here
 * @param[in] c_strContent the JSON content of the request body
 * @param[in] c_strApiVersionDate Azure API version
 * @param[in] c_strSubscriptionIdentifier Subscription identifier
 * @param[in] c_strResourceGroup Azure resource group
 * @param[inout] pnResponse HTTP response code for this request
 * @return Value corresponding to that key
 * @note This is not a perfect function to get a value form the Json object.
 *
 ********************************************************************************************/

static std::vector<Byte> __cdecl MakeMicrosoftAzureApiCall(
    _in const std::string & c_strMicrosoftAzureAccessToken,
    _in const std::string & c_strVerb,
    _in const std::string & c_strResource,
    _in const std::string & c_strHost,
    _in const std::string & c_strContent,
    _in const std::string & c_strApiVersionDate,
    _in const std::string & c_strSubscriptionIdentifier,
    _in const std::string & c_strResourceGroup,
    _inout long * pnResponse
    )
{
    __DebugFunction();

    // Make sure we are not currently logged on
    _ThrowBaseExceptionIf((0 == c_strMicrosoftAzureAccessToken.size()), "Authentication is required...", nullptr);

    // Build out the API call components
    std::string strApiUri = "/subscriptions/" + c_strSubscriptionIdentifier + "/resourceGroups/" + c_strResourceGroup + "/providers/" + c_strResource + "?api-version=" + c_strApiVersionDate;
    std::vector<std::string> stlHeader;
    stlHeader.push_back("Host: " + c_strHost);
    stlHeader.push_back("Authorization: Bearer " + c_strMicrosoftAzureAccessToken);
    if (0 != c_strContent.length())
    {
        stlHeader.push_back("Content-Type: application/json");
    }
    stlHeader.push_back("Content-Length: " + std::to_string(c_strContent.size()));

    return ::RestApiCall(c_strHost, 443, c_strVerb, strApiUri, c_strContent, false, stlHeader, pnResponse);
}

/********************************************************************************************
 *
 * @function MakeMicrosoftAzureApiCall
 * @brief Function to get small json values which exist in the same line as the key
 * @param[in] c_strMicrosoftAzureAccessToken Azure access token
 * @param[in] c_strVerb HTTP request verb
 * @param[in] c_strResource Azure resource for which the request is being made for
 * @param[in] c_strHost azure domain name to be called here
 * @param[in] c_strContent the JSON content of the request body
 * @param[in] c_strApiVersionDate Azure API version
 * @param[in] c_strSubscriptionIdentifier Subscription identifier
 * @param[in] c_strResourceGroup Azure resource group
 * @return Value corresponding to that key
 * @note This is not a perfect function to get a value form the Json object.
 *
 ********************************************************************************************/

static std::vector<Byte> __cdecl MakeMicrosoftAzureApiCall(
    _in const std::string & c_strMicrosoftAzureAccessToken,
    _in const std::string & c_strVerb,
    _in const std::string & c_strResource,
    _in const std::string & c_strHost,
    _in const std::string & c_strContent,
    _in const std::string & c_strApiVersionDate,
    _in const std::string & c_strSubscriptionIdentifier,
    _in const std::string & c_strResourceGroup
    )
{
    __DebugFunction();

    long nResponse;
    return ::MakeMicrosoftAzureApiCall(c_strMicrosoftAzureAccessToken, \
                                        c_strVerb, \
                                        c_strResource, \
                                        c_strHost, \
                                        c_strContent, \
                                        c_strApiVersionDate, \
                                        c_strSubscriptionIdentifier, \
                                        c_strResourceGroup, \
                                        &nResponse);
}

/********************************************************************************************
 *
 * @function CreateResourceGroup
 * @brief Function to get small json values which exist in the same line as the key
 * @param[in] c_strMicrosoftAzureAccessToken Azure access token
 * @param[in] c_strSubscriptionIdentifier Subscription identifier
 * @param[in] c_strResourceGroup Azure resource group
 * @return StructuredBuffer with status
 * @note
 *
 ********************************************************************************************/

StructuredBuffer __stdcall CreateResourceGroup(
    _in const std::string & c_strMicrosoftAzureAccessToken,
    _in const std::string & c_szSubscriptionIdentifier,
    _in const std::string & c_szResourceGroup,
    _in const std::string & c_szResourceGroupSpecification
) throw()
{
    __DebugFunction();

    StructuredBuffer oResponse;
    oResponse.PutString("Status", "Fail");

    try
    {
        // Make sure we are not currently logged on
        _ThrowBaseExceptionIf((0 == c_strMicrosoftAzureAccessToken.size()), "Authentication required...", nullptr);

        // Create a Microsoft Azure public IP address
        std::string strVerb = "PUT";
        std::string strResource = "Microsoft.Network/resourcegroups/" + c_szResourceGroup;
        std::string strHost = "management.azure.com";
        std::string strContent = c_szResourceGroupSpecification;
        std::string strApiVersionDate = "2020-10-01";

        // Build out the API call components
        std::string strApiUri = "/subscriptions/" + c_szSubscriptionIdentifier + "/resourceGroups/" + c_szResourceGroup + "?api-version=" + strApiVersionDate;
        std::vector<std::string> stlHeader;
        stlHeader.push_back("Host: " + strHost);
        stlHeader.push_back("Authorization: Bearer " + c_strMicrosoftAzureAccessToken);
        if (0 != strContent.length())
        {
            stlHeader.push_back("Content-Type: application/json");
        }
        stlHeader.push_back("Content-Length: " + std::to_string(strContent.size()));

        bool fResourceGroupCreated = false;
        do
        {
            std::vector<Byte> stlResponse = ::RestApiCall(strHost, 443, strVerb, strApiUri, strContent, false, stlHeader);
            _ThrowBaseExceptionIf((0 == stlResponse.size()), "Failed to create a Microsoft Azure Resource Group", nullptr);
            stlResponse.push_back(0);
            StructuredBuffer oAzureVmDeployResponse = JsonValue::ParseDataToStructuredBuffer((const char*)stlResponse.data());
            if ((true == oAzureVmDeployResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oAzureVmDeployResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
            {
                if (false == IsServerTimeoutError(oAzureVmDeployResponse))
                {
                    _ThrowBaseExceptionIf((true == oAzureVmDeployResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Failed to create a Microsoft Azure Resource Group with error %s", oAzureVmDeployResponse.GetStructuredBuffer("error").ToString().c_str());
                    _ThrowBaseExceptionIf((true == oAzureVmDeployResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Failed to create a Microsoft Azure Resource Group with error %s", oAzureVmDeployResponse.GetString("error").c_str());
                }
            }
            else
            {
                fResourceGroupCreated = true;
            }
        } while (false == fResourceGroupCreated);

        oResponse.PutString("Status", "Success");
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oResponse.PutString("error", c_oBaseException.GetExceptionMessage());
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oResponse.PutString("error", "internal std error while creating resource group.");
    }
    return oResponse;
}

/********************************************************************************************
 *
 * @function DeployVirtualMachineAndWait
 * @brief Function to get small json values which exist in the same line as the key
 * @param[in] c_szApplicationIdentifier Azure login application id
 * @param[in] c_szSecret Azure login secret
 * @param[in] c_szTenantIdentifier Azure AD Tenant
 * @param[in] c_szSubscriptionIdentifier Subscription identifier
 * @param[in] c_szResourceGroup Azure resource group
 * @param[in] c_szVirtualMachineIdentifier Name of the virtual machine
 * @param[in] c_szconfidentialVirtualMachineSpecification the virtual machine json spec
 * @param[in] c_szLocation azure vm location
 * @return Structuredbuffer with status and Ip Address of the newly created Virtual Machine
 * @note This is a blocking call
 *
 ********************************************************************************************/
std::string GetVirtualMachineIpAddress(
    _in const std::string & c_strMicrosoftAzureAccessToken,
    _in const std::string & c_strSubscriptionIdentifier,
    _in const std::string & c_strResourceGroup,
    _in const std::string & c_strVirtualMachineIdentifier
)
{
    __DebugFunction();

    auto strVerb = "GET";
    auto strResource = "Microsoft.Network/publicIPAddresses/" + c_strVirtualMachineIdentifier + "-ip";
    auto strHost = "management.azure.com";
    auto strContent = "";
    auto strApiVersionDate = "2020-07-01";
    bool fIPAddressFound = false;
    std::string strVirtualMachineIpAddress = "";
    do
    {
        auto stlResponse = ::MakeMicrosoftAzureApiCall(c_strMicrosoftAzureAccessToken, strVerb, strResource, strHost, strContent, strApiVersionDate, c_strSubscriptionIdentifier, c_strResourceGroup);
        _ThrowBaseExceptionIf((0 == stlResponse.size()), "Failed to get the ip address of a Microsoft Azure virtual machine", nullptr);

        stlResponse.push_back(0);
        std::string strResponse = (const char*)stlResponse.data();
        if (std::string::npos != strResponse.find("\"error\""))
        {
            stlResponse.push_back(0);
            StructuredBuffer oResponse = JsonValue::ParseDataToStructuredBuffer((const char*)stlResponse.data());
            if ((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
            {
                if (false == IsServerTimeoutError(oResponse))
                {
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Failed to get the ip address of a Microsoft Azure virtual machine with error %s", oResponse.GetStructuredBuffer("error").ToString().c_str());
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Failed to get the ip address of a Microsoft Azure virtual machine with error %s", oResponse.GetString("error").c_str());
                }
            }
        }
        else
        {
            // TODO: ParseDataToStructuredBuffer cannot handle the escaped strings. The workaround is to manually get
            // the Ip Address from the string response.
            strVirtualMachineIpAddress = ::GetJsonValue(std::string((char*)stlResponse.data(), stlResponse.size()), "\"ipAddress\"");
            _ThrowBaseExceptionIf((0 == strVirtualMachineIpAddress.length()), "No IP Address in the response", nullptr);
            fIPAddressFound = true;
        }
    } while (false == fIPAddressFound);

    return strVirtualMachineIpAddress;
}

/********************************************************************************************
 *
 * @function DeployVirtualMachineAndWait
 * @brief Function to get small json values which exist in the same line as the key
 * @param[in] c_szApplicationIdentifier Azure login application id
 * @param[in] c_szSecret Azure login secret
 * @param[in] c_szTenantIdentifier Azure AD Tenant
 * @param[in] c_szSubscriptionIdentifier Subscription identifier
 * @param[in] c_szResourceGroup Azure resource group
 * @param[in] c_szVirtualMachineIdentifier Name of the virtual machine
 * @param[in] c_szconfidentialVirtualMachineSpecification the virtual machine json spec
 * @param[in] c_szLocation azure vm location
 * @return Structuredbuffer with status and Ip Address of the newly created Virtual Machine
 * @note This is a blocking call
 *
 ********************************************************************************************/
StructuredBuffer DeployVirtualMachineAndWait(
    _in const std::string & c_szApplicationIdentifier,
    _in const std::string & c_szSecret,
    _in const std::string & c_szTenantIdentifier,
    _in const std::string & c_szSubscriptionIdentifier,
    _in const std::string & c_szResourceGroup,
    _in const std::string & c_szVirtualMachineIdentifier,
    _in const std::string & c_szconfidentialVirtualMachineSpecification,
    _in const std::string & c_szLocation
) throw()
{
    __DebugFunction();

    StructuredBuffer oResponse;
    oResponse.PutString("Status", "Fail");

    try
    {
        // Login to the Microsoft Azure API Portal
        const std::string c_strMicrosoftAzureAccessToken = ::LoginToMicrosoftAzureApiPortal(c_szApplicationIdentifier, c_szSecret, c_szTenantIdentifier);
        _ThrowBaseExceptionIf((0 == c_strMicrosoftAzureAccessToken.length()), "Authentication failed...", nullptr);

        StructuredBuffer oDeploymentResult = ::CreateAzureDeployment(c_strMicrosoftAzureAccessToken, c_szconfidentialVirtualMachineSpecification, c_szSubscriptionIdentifier, c_szResourceGroup, c_szLocation);
        _ThrowBaseExceptionIf(("Success" != oDeploymentResult.GetString("Status")), "Failed to create Virtual Machine deployment. %s", oDeploymentResult.GetString("error").c_str());

        // Wait until the virtual machine is running
        bool fIsRunning = false;
        do
        {
            std::string strVerb = "GET";
            std::string strResource = "Microsoft.Compute/virtualMachines/" + c_szVirtualMachineIdentifier;
            std::string strHost = "management.azure.com";
            std::string strContent = "";
            std::string strApiVersionDate = "2020-12-01";
            auto stlResponse = ::MakeMicrosoftAzureApiCall(c_strMicrosoftAzureAccessToken, strVerb, strResource, strHost, strContent, strApiVersionDate, c_szSubscriptionIdentifier, c_szResourceGroup);
            _ThrowBaseExceptionIf((0 == stlResponse.size()), "Failed to get the status of a virtual machine being provisioned", nullptr);
            stlResponse.push_back(0);
            StructuredBuffer oResponse = JsonValue::ParseDataToStructuredBuffer((const char*)stlResponse.data());
            if ((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
            {
                if (false == ::IsServerTimeoutError(oResponse))
                {
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Failed to get the status of a virtual machine being provisioned with error %s", oResponse.GetStructuredBuffer("error").ToString().c_str());
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Failed to get the status of a virtual machine being provisioned with error %s", oResponse.GetString("error").c_str());
                }
            }

            if (true == oResponse.IsElementPresent("properties", INDEXED_BUFFER_VALUE_TYPE))
            {
                StructuredBuffer oProperties = oResponse.GetStructuredBuffer("properties");
                if (true == oProperties.IsElementPresent("provisioningState", ANSI_CHARACTER_STRING_VALUE_TYPE))
                {
                    std::string strProvisioningState = oProperties.GetString("provisioningState");
                    if ("Succeeded" == strProvisioningState)
                    {
                        fIsRunning = true;
                    }
                    else if (("Deleting"== strProvisioningState) || ("Deleted"== strProvisioningState) || ("Canceled"== strProvisioningState) || ("Failed"== strProvisioningState))
                    {
                        _ThrowBaseException("Virtual machine being provisioned. Response: %s", oResponse.ToString().c_str());
                    }
                }
            }

            // We put the thread to sleep while we wait
            if (false == fIsRunning)
            {
                ::sleep(5);
            }
        } while (false == fIsRunning);

        std::string strVirtualMachineIpAddress = GetVirtualMachineIpAddress(c_strMicrosoftAzureAccessToken, \
                                                                            c_szSubscriptionIdentifier, \
                                                                            c_szResourceGroup, \
                                                                            c_szVirtualMachineIdentifier);

        oResponse.PutString("Status", "Success");
        oResponse.PutString("IpAddress", strVirtualMachineIpAddress);
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oResponse.PutString("error", c_oBaseException.GetExceptionMessage());
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oResponse.PutString("error", "std error");
    }

    return oResponse;
}

/********************************************************************************************
 *
 * @function CreateAzureDeployment
 * @brief Deploy a Azure template with parameters
 * @param[in] c_strMicrosoftAzureAccessToken
 * @param[in] c_strSubscriptionIdentifier
 * @param[in] c_strResourceGroup
 * @param[in] c_strVirtualNetworkIdentifier
 * @param[in] c_strLocation
 * @return Id of the created resource
 * @note This is a blocking call
 *
 ********************************************************************************************/

StructuredBuffer CreateAzureDeployment(
    _in const std::string & c_strMicrosoftAzureAccessToken,
    _in const std::string & c_strDeploymentParameters,
    _in const std::string & c_strSubscriptionIdentifier,
    _in const std::string & c_strResourceGroup,
    _in const std::string & c_strLocation
) throw()
{
    __DebugFunction();
    __DebugAssert(0 != c_strMicrosoftAzureAccessToken.length());

    StructuredBuffer oDeploymentResult;
    oDeploymentResult.PutString("Status", "Fail");

    try
    {
        // Create resource group
        std::string resourceGroupSpec = std::string("{\"location\": \"") + c_strLocation + "\"}";
        StructuredBuffer oResourceGroupStatus = ::CreateResourceGroup(c_strMicrosoftAzureAccessToken, c_strSubscriptionIdentifier, c_strResourceGroup, resourceGroupSpec.c_str());
        if ("Success" != oResourceGroupStatus.GetString("Status"))
        {
            _ThrowBaseException("Resource Group Create Fail: %s", oResourceGroupStatus.GetString("error").c_str());
        }

        // Create a Virtual Machine with a pre-existing Azure Template
        std::string strVerb = "PUT";
        std::string strResource = "Microsoft.Resources/deployments/sail-" + Guid().ToString(eRaw) + "-deploy";
        std::string strHost = "management.azure.com";
        std::string strApiVersionDate = "2021-04-01";
        bool fIsDeploymentRequestDone = false;
        do
        {
            std::vector<Byte> stlResponse = ::MakeMicrosoftAzureApiCall(c_strMicrosoftAzureAccessToken, strVerb, strResource, strHost, c_strDeploymentParameters, strApiVersionDate, c_strSubscriptionIdentifier, c_strResourceGroup);
            _ThrowBaseExceptionIf((0 == stlResponse.size()), "Failed to create a Microsoft Azure public IP address", nullptr);
            stlResponse.push_back(0);
            StructuredBuffer oResponse = JsonValue::ParseDataToStructuredBuffer((const char*)stlResponse.data());
            if ((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
            {
                if (true == IsServerTimeoutError(oResponse))
                {
                    fIsDeploymentRequestDone = false;
                }
                else
                {
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Failed to create a Microsoft Azure Deployment with error %s", oResponse.GetStructuredBuffer("error").ToString().c_str());
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Failed to create a Microsoft Azure Deployment with error %s", oResponse.GetString("error").c_str());
                }
            }
            else
            {
                fIsDeploymentRequestDone = true;
            }
        } while(false == fIsDeploymentRequestDone);

        // Wait until the deployment is running
        bool fIsRunning = false;
        do
        {
            strVerb = "GET";
            strApiVersionDate = "2021-04-01";
            auto stlResponse = ::MakeMicrosoftAzureApiCall(c_strMicrosoftAzureAccessToken, strVerb, strResource, strHost, "", strApiVersionDate, c_strSubscriptionIdentifier, c_strResourceGroup);
            _ThrowBaseExceptionIf((0 == stlResponse.size()), "Failed to create a Microsoft Azure Deployment", nullptr);
            stlResponse.push_back(0);
            StructuredBuffer oResponse = JsonValue::ParseDataToStructuredBuffer((const char*)stlResponse.data());
            if ((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
            {
                if (false == IsServerTimeoutError(oResponse))
                {
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Failed to create a Microsoft Azure Deployment with error %s", oResponse.GetStructuredBuffer("error").ToString().c_str());
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Failed to create a Microsoft Azure Deployment with error %s", oResponse.GetString("error").c_str());
                    _ThrowBaseException("Should never be thrown. Something is horribly wrong.", nullptr);
                }
            }

            if (true == oResponse.IsElementPresent("properties", INDEXED_BUFFER_VALUE_TYPE))
            {
                StructuredBuffer oProperties(oResponse.GetStructuredBuffer("properties").GetBase64SerializedBuffer().c_str());
                if (true == oProperties.IsElementPresent("provisioningState", ANSI_CHARACTER_STRING_VALUE_TYPE))
                {
                    std::string strProvisioningState = oProperties.GetString("provisioningState");
                    if ("Succeeded" == strProvisioningState)
                    {
                        fIsRunning = true;
                    }
                    else if ("Failed" == strProvisioningState)
                    {
                        _ThrowBaseExceptionIf((true == oProperties.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Deployment error: %s", oProperties.GetStructuredBuffer("error").ToString().c_str(), nullptr);
                        _ThrowBaseExceptionIf((true == oProperties.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Deployment error: %s", oProperties.GetString("error").c_str(), nullptr);
                        _ThrowBaseException("Unknown Deployment error. Contact SAIL.", nullptr);
                    }
                }
            }
            // Put the thread to sleep while we wait
            if (false == fIsRunning)
            {
                ::sleep(5);
            }
        } while (false == fIsRunning);

        oDeploymentResult.PutString("Status", "Success");
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oDeploymentResult.PutString("error", c_oBaseException.GetExceptionMessage());
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oDeploymentResult.PutString("error", "std error");
    }
    
    return oDeploymentResult;
}

/********************************************************************************************
 *
 * @function DoesAzureResourceExist
 * @brief Check if an Azure resource exists
 * @param[in] c_strApplicationIdentifier
 * @param[in] c_strSecret
 * @param[in] c_strTenantIdentifier
 * @param[in] c_strResourceId
 * @return true if exits, false otherwise
 *
 ********************************************************************************************/

bool DoesAzureResourceExist(
    _in const std::string & c_strMicrosoftAzureAccessToken,
    _in const std::string & c_strResourceId
)
{
    __DebugFunction();

    bool fResourceExist = false;

    std::string strVerb = "GET";
    std::string strContent = "";
    std::string strApiUri = "";
    if (std::string::npos != c_strResourceId.find("Microsoft.Network"))
    {
        strApiUri = c_strResourceId + "?api-version=2021-03-01";
    }
    else if (std::string::npos != c_strResourceId.find("Microsoft.Compute"))
    {
        strApiUri = c_strResourceId + "?api-version=2021-04-01";
    }
    _ThrowBaseExceptionIf((0 == strApiUri.length()), "Incorrect resource type", nullptr);

    std::string strHost = "management.azure.com";
    std::vector<std::string> stlHeader;
    stlHeader.push_back("Host: " + strHost);
    stlHeader.push_back("Authorization: Bearer " + c_strMicrosoftAzureAccessToken);
    stlHeader.push_back("Content-Length: " + std::to_string(strContent.length()));

    long nResponseCode = 0;
    bool fIsValidResponse = false;

    do
    {
        std::vector<Byte> stlResponse = ::RestApiCall(strHost, 443, strVerb, strApiUri, "", false, stlHeader, &nResponseCode);
        if (200 == nResponseCode)
        {
            fResourceExist = true;
            fIsValidResponse = true;
        }
        else
        {
            if (0 < stlResponse.size())
            {
                stlResponse.push_back(0);
                StructuredBuffer oResponse = JsonValue::ParseDataToStructuredBuffer((const char*)stlResponse.data());
                if ((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
                {
                    if (true == ::IsServerTimeoutError(oResponse))
                    {
                        fIsValidResponse = false;
                    }
                    else
                    {
                        fIsValidResponse = true;
                        fResourceExist = false;
                    }
                }
                else
                {
                    fIsValidResponse = true;
                    fResourceExist = false;
                    std::cout << "DoesAzureResourceExist. Unexpected response from server. Response: " << oResponse.ToString() << std::endl;
                }
            }
            else
            {
                fIsValidResponse = true;
                fResourceExist = false;
                std::cout << "DoesAzureResourceExist. No response from server. Response code: " << nResponseCode << std::endl;
            }
        }
    }
    while (false == fIsValidResponse);

    return fResourceExist;
}

/********************************************************************************************
 *
 * @function CopyVirtualMachineImage
 * @brief Copy VM Image from SAIL subscription to given subscription
 * @param[in] c_strMicrosoftAzureAccessToken Azure Authorization token
 * @param[in] c_strSubscriptionId Subscription Guid of the target
 * @param[in] c_strResourceGroupName resource group for the new image
 * @param[in] c_strLocation Location of the New Image Resource group
 * @param[in] c_strImageName Name of the image to be created
 * @return StrructuredBuffer containing status code
 *
 ********************************************************************************************/
StructuredBuffer CopyVirtualMachineImage(
    _in const std::string c_strMicrosoftAzureAccessToken,
    _in const std::string c_strSubscriptionId,
    _in const std::string c_strResourceGroupName,
    _in const std::string c_strLocation,
    _in const std::string c_strImageName
) throw()
{
    __DebugFunction();
    __DebugAssert(0 != c_strMicrosoftAzureAccessToken.length());

    StructuredBuffer oCopyImageResult;
    oCopyImageResult.PutString("Status", "Fail");

    try
    {
        // Create resource group
        std::string strResourceGroupSpec = std::string("{\"location\": \"") + c_strLocation + "\"}";
        StructuredBuffer oResourceGroupStatus = ::CreateResourceGroup(c_strMicrosoftAzureAccessToken, c_strSubscriptionId, c_strResourceGroupName, strResourceGroupSpec.c_str());
        _ThrowBaseExceptionIf(("Success" != oResourceGroupStatus.GetString("Status")), "Resource Group Create Fail: %s", oResourceGroupStatus.GetString("error").c_str());

        // Get a valid Storage Account Name
        std::string strStorageAccountName;
        bool fIsValidName = false;
        do
        {
            strStorageAccountName = "sailimage" + std::to_string(std::rand());
            std::string strVerb = "POST";
            StructuredBuffer oRequest;
            oRequest.PutString("name", strStorageAccountName);
            oRequest.PutString("type", "Microsoft.Storage/storageAccounts");
            auto oJsonResponse = JsonValue::ParseStructuredBufferToJson(oRequest);
            std::string strContent = oJsonResponse->ToString();
            oJsonResponse->Release();
            std::string strApiUri = "/subscriptions/" + c_strSubscriptionId + "/providers/Microsoft.Storage/checkNameAvailability?api-version=2021-04-01";
            std::string strHost = "management.azure.com";

            std::vector<std::string> stlHeader;
            stlHeader.push_back("Host: " + strHost);
            stlHeader.push_back("Authorization: Bearer " + c_strMicrosoftAzureAccessToken);
            stlHeader.push_back("Content-Length: " + std::to_string(strContent.length()));

            long nResponseCode = 0;
            std::vector<Byte> stlResponse = ::RestApiCall(strHost, 443, strVerb, strApiUri, strContent, false, stlHeader, &nResponseCode);
            _ThrowBaseExceptionIf((0 == stlResponse.size()), "Failed to create a Microsoft Azure Deployment", nullptr);
            stlResponse.push_back(0);
            StructuredBuffer oResponse = JsonValue::ParseDataToStructuredBuffer((const char*)stlResponse.data());
            if ((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
            {
                if (false == IsServerTimeoutError(oResponse))
                {
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Storage Account name check: %s", oResponse.GetStructuredBuffer("error").ToString().c_str());
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Storage Account name check: %s", oResponse.GetString("error").c_str());
                    _ThrowBaseException("Should never be thrown. Something is horribly wrong.", nullptr);
                }
            }
            else
            {
                fIsValidName = oResponse.GetBoolean("nameAvailable");
            }
        }
        while(false == fIsValidName);
        _ThrowBaseExceptionIf((0 == strStorageAccountName.length()), "Invaid Storage Account name", nullptr);

        // Create a storage account
        StructuredBuffer oRequest;
        StructuredBuffer oSku;
        oSku.PutString("name", "Premium_LRS");
        oRequest.PutStructuredBuffer("sku", oSku);
        oRequest.PutString("kind", "StorageV2");
        oRequest.PutString("location", c_strLocation);
        auto oJsonResponse = JsonValue::ParseStructuredBufferToJson(oRequest);
        std::string strContent = oJsonResponse->ToString();
        oJsonResponse->Release();

        // Keep making the same request every 5 seconds until the reposne code is 200 or the reponse is not empty
        std::vector<Byte> stlResponse;
        bool fStorageAccountCreated = false;
        StructuredBuffer oResponse;
        do
        {
            long nResponseCode = 0;
            stlResponse = ::MakeMicrosoftAzureApiCall(c_strMicrosoftAzureAccessToken, "PUT", "Microsoft.Storage/storageAccounts/"+ strStorageAccountName, "management.azure.com", strContent, "2021-04-01", c_strSubscriptionId, c_strResourceGroupName, &nResponseCode);
            if (200 == nResponseCode)
            {
                fStorageAccountCreated = true;
                _ThrowBaseExceptionIf((0 == stlResponse.size()), "Unexpected response code %d with no string response", nResponseCode, nullptr);
                stlResponse.push_back(0);
                oResponse = JsonValue::ParseDataToStructuredBuffer((const char*)stlResponse.data());
            }
            else if (202 == nResponseCode)
            {
                ::sleep(5);
            }
            else
            {
                _ThrowBaseExceptionIf((0 == stlResponse.size()), "Unexpected response code %d with no string response", nResponseCode, nullptr);
                stlResponse.push_back(0);
                oResponse = JsonValue::ParseDataToStructuredBuffer((const char*)stlResponse.data());
                if ((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
                {
                    if (false == IsServerTimeoutError(oResponse))
                    {
                        _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Storage Account create error: %s", oResponse.GetStructuredBuffer("error").GetString("message").c_str());
                        _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Storage Account create error: %s", oResponse.GetString("error").c_str());
                        _ThrowBaseException("Should never be thrown. Something is horribly wrong.", nullptr);
                    }
                }
            }
        }
        while(false == fStorageAccountCreated);

        std::string strStorageAccountId = oResponse.GetString("id");
        std::string strBlobLink = oResponse.GetStructuredBuffer("properties").GetStructuredBuffer("primaryEndpoints").GetString("blob");

        // Fetch the keys for the storage account
        bool fStorageAccountKeysFetched = false;
        do
        {
            stlResponse = ::MakeMicrosoftAzureApiCall(c_strMicrosoftAzureAccessToken, "POST", "Microsoft.Storage/storageAccounts/"+ strStorageAccountName + "/listKeys", "management.azure.com", strContent, "2021-04-01", c_strSubscriptionId, c_strResourceGroupName);
            _ThrowBaseExceptionIf((0 == stlResponse.size()), "Cannot fetch storage account keys", nullptr);
            stlResponse.push_back(0);
            oResponse = JsonValue::ParseDataToStructuredBuffer((const char*)stlResponse.data());
            if ((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
            {
                if (false == IsServerTimeoutError(oResponse))
                {
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Cannot fetch storage account keys: %s", oResponse.GetStructuredBuffer("error").ToString().c_str());
                    _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Cannot fetch storage account keys: %s", oResponse.GetString("error").c_str());
                    _ThrowBaseException("Should never be thrown. Something is horribly wrong.", nullptr);
                }
            }
            else
            {
                fStorageAccountKeysFetched = true;
            }
        } while (false == fStorageAccountKeysFetched);
        std::string strBase64EncodedKey = oResponse.GetStructuredBuffer("keys").GetStructuredBuffer("keys0").GetString("value");

        // Create a container in the storage account
        std::string strApiUri = "/subscriptions/" + c_strSubscriptionId + "/resourceGroups/" + c_strResourceGroupName + "/providers/Microsoft.Storage/storageAccounts/"+ strStorageAccountName + "/blobServices/default/containers/images?api-version=2021-04-01";
        std::vector<std::string> stlHeader;
        stlHeader.push_back("Host: management.azure.com");
        stlHeader.push_back("Authorization: Bearer " + c_strMicrosoftAzureAccessToken);
        stlHeader.push_back("Content-Type: application/json");
        stlHeader.push_back("Content-Length: " + std::to_string(2));

        long nResponse = 0;
        bool fContainerCreated = false;
        do
        {
            stlResponse = ::RestApiCall("management.azure.com", 443, "PUT", strApiUri, "{}", false, stlHeader, &nResponse);
            if (201 == nResponse)
            {
                ::sleep(5);
            }
            else
            {
                if (0 < stlResponse.size())
                {
                    stlResponse.push_back(0);
                    oResponse = JsonValue::ParseDataToStructuredBuffer((char *)stlResponse.data());
                    if ((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
                    {
                        if (false == IsServerTimeoutError(oResponse))
                        {
                            _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Container creation: %s", oResponse.GetStructuredBuffer("error").ToString().c_str());
                            _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Container creation: %s", oResponse.GetString("error").c_str());
                            _ThrowBaseException("Should never be thrown. Something is horribly wrong.", nullptr);
                        }
                    }
                    else
                    {
                        fContainerCreated = true;
                    }
                }
                else
                {
                    fContainerCreated = true;
                }
            }
        }
        while(false == fContainerCreated);

        // Create a SAS token
        std::string strContainerName = "images";
        std::string strExpiry = "2025-01-01";
        std::string strCommandToGetSAS = "/usr/bin/az storage container generate-sas -n " + strContainerName + " --account-name "+ strStorageAccountName +" --account-key "+ strBase64EncodedKey +" --https-only --permissions dlrw --expiry "+ strExpiry +" -o tsv";
        std::string strSASToken = ::ExecuteBashCommandAndGetResult(strCommandToGetSAS.c_str());
        _ThrowBaseExceptionIf((0 == strSASToken.length()), "Could not create SAS token.", nullptr);
        strSASToken.erase(std::remove(strSASToken.begin(), strSASToken.end(), '\n'), strSASToken.end());
        strSASToken.erase(std::remove(strSASToken.begin(), strSASToken.end(), '\r'), strSASToken.end());

        // Copy the image blob to the container
        std::string strUrlSas = "https://" + strStorageAccountName + ".blob.core.windows.net/images/sailimage.vhd?" + strSASToken;

        stlHeader.clear();
        stlHeader.push_back("Host: " + strStorageAccountName+".blob.core.windows.net");
        stlHeader.push_back("Content-Length: 0");
        stlHeader.push_back("x-ms-copy-source: "+ ::GetInitializationValue("SecureVirtualMachineImageUrl"));
        long nResponseCode = 0;
        stlResponse = ::RestApiCall(strStorageAccountName+".blob.core.windows.net", 443, "PUT", "/images/sailimage.vhd?" + strSASToken, "", false, stlHeader, &nResponseCode);
        _ThrowBaseExceptionIf((202 != nResponseCode), "Failed to copy the image from SAIL account. Response code: %d %s", nResponseCode, stlResponse.data(), nullptr);

        // Busy wait loop to check if the image copy was complete
        bool fIsCopyComplete = false;
        do
        {
            std::map<std::string, std::string> stlMapOfResponseHeaders;
            stlResponse = ::RestApiCall(strStorageAccountName+".blob.core.windows.net", 443, "HEAD", "/images/sailimage.vhd?" + strSASToken, "", false, stlHeader, &stlMapOfResponseHeaders, &nResponseCode);
            if (std::string::npos != stlMapOfResponseHeaders.at("x-ms-copy-status").find("pending"))
            {
                ::sleep(2);
            }
            else
            {
                fIsCopyComplete = true;
            }
        } while (false == fIsCopyComplete);

        // TODO: Prawal check if it was a success
        StructuredBuffer oImageCreateRequest;
        oImageCreateRequest.PutString("location", c_strLocation);
        StructuredBuffer oProperties;
        oProperties.PutString("hyperVGeneration", "V2");
        StructuredBuffer oStorageProfile;
        oStorageProfile.PutBoolean("zoneResilient", true);
        StructuredBuffer oOsDisk;
        oOsDisk.PutString("osType", "Linux");
        oOsDisk.PutString("blobUri", "https://" + strStorageAccountName + ".blob.core.windows.net/images/sailimage.vhd");
        oOsDisk.PutString("osState", "Generalized");
        oStorageProfile.PutStructuredBuffer("osDisk", oOsDisk);
        oProperties.PutStructuredBuffer("storageProfile", oStorageProfile);
        oImageCreateRequest.PutStructuredBuffer("properties", oProperties);
        oJsonResponse = JsonValue::ParseStructuredBufferToJson(oImageCreateRequest);
        std::string strConvertVhdToImageRequest = oJsonResponse->ToString();
        oJsonResponse->Release();

        strApiUri = "/subscriptions/" + c_strSubscriptionId + "/resourceGroups/" + c_strResourceGroupName + "/providers/Microsoft.Compute/images/"+ c_strImageName + "?api-version=2021-07-01";
        stlHeader.clear();
        stlHeader.push_back("Host: management.azure.com");
        stlHeader.push_back("Authorization: Bearer " + c_strMicrosoftAzureAccessToken);
        stlHeader.push_back("Content-Type: application/json");
        stlHeader.push_back("Content-Length: " + std::to_string(strConvertVhdToImageRequest.length()));

        nResponse = 0;
        bool fImageCreated = false;
        do
        {
            stlResponse = ::RestApiCall("management.azure.com", 443, "PUT", strApiUri, strConvertVhdToImageRequest, false, stlHeader, &nResponse);
            if (201 == nResponse)
            {
                ::sleep(5);
            }
            else
            {
                if (0 < stlResponse.size())
                {
                    stlResponse.push_back(0);
                    oResponse = JsonValue::ParseDataToStructuredBuffer((char *)stlResponse.data());
                    if ((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
                    {
                        if (false == IsServerTimeoutError(oResponse))
                        {
                            _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Image copy: %s", oResponse.GetStructuredBuffer("error").ToString().c_str());
                            _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Image copy: %s", oResponse.GetString("error").c_str());
                            _ThrowBaseException("Should never be thrown. Something is horribly wrong.", nullptr);
                        }
                    }
                    else
                    {
                        fImageCreated = true;
                    }
                }
                else
                {
                    fImageCreated = true;
                }
            }
        }
        while(false == fImageCreated);
        oCopyImageResult.PutString("VirtualImageId", oResponse.GetString("id"));
        oCopyImageResult.PutString("Status", "Success");
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oCopyImageResult.PutString("error", c_oBaseException.GetExceptionMessage());
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oCopyImageResult.PutString("error", "std error");
    }

    return oCopyImageResult;
}

/********************************************************************************************
 *
 * @function DoesAzureResourceExist
 * @brief Check if an Azure resource exists
 * @param[in] c_strApplicationIdentifier
 * @param[in] c_strSecret
 * @param[in] c_strTenantIdentifier
 * @param[in] c_strResourceId
 * @return true if exits, false otherwise
 *
 ********************************************************************************************/

bool DeleteAzureResources(
    _in const std::string & c_strApplicationIdentifier,
    _in const std::string & c_strTenantIdentifier,
    _in const std::string & c_strSecret,
    _in const std::vector<std::string> & c_stlResourceId
)
{
    __DebugFunction();

    bool fResourcesDeleted = false;

    // Login to the Microsoft Azure API Portal
    const std::string c_strMicrosoftAzureAccessToken = ::LoginToMicrosoftAzureApiPortal(c_strApplicationIdentifier, c_strSecret, c_strTenantIdentifier);
    _ThrowBaseExceptionIf((0 == c_strMicrosoftAzureAccessToken.length()), "Azure Authentication failed...", nullptr);

    for (auto strResourceId : c_stlResourceId)
    {
        if (true == ::DoesAzureResourceExist(c_strMicrosoftAzureAccessToken, strResourceId))
        {
            std::string strVerb = "DELETE";
            std::string strContent = "";
            std::string strApiUri = "";
            if (std::string::npos != strResourceId.find("Microsoft.Network"))
            {
                strApiUri = strResourceId + "?api-version=2021-03-01";
            }
            else if (std::string::npos != strResourceId.find("Microsoft.Compute"))
            {
                strApiUri = strResourceId + "?api-version=2021-04-01";
            }
            _ThrowBaseExceptionIf((0 == strApiUri.length()), "Incorrect resource type", nullptr);

            std::string strHost = "management.azure.com";

            std::vector<std::string> stlHeader;
            stlHeader.push_back("Host: " + strHost);
            stlHeader.push_back("Authorization: Bearer " + c_strMicrosoftAzureAccessToken);
            stlHeader.push_back("Content-Length: " + std::to_string(strContent.length()));

            long nResponseCode = 0;
            bool fResourceDeleted = false;
            do
            {
                std::vector<Byte> stlResponse = ::RestApiCall(strHost, 443, strVerb, strApiUri, "", false, stlHeader, &nResponseCode);
                if ((200 == nResponseCode) || (202 == nResponseCode) || (204 == nResponseCode))
                {
                    fResourceDeleted = true;
                }
                else
                {
                    if (0 < stlResponse.size())
                    {
                        stlResponse.push_back(0);
                        StructuredBuffer oResponse = JsonValue::ParseDataToStructuredBuffer((const char*)stlResponse.data());
                        if ((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)) || (true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)))
                        {
                            if (false == ::IsServerTimeoutError(oResponse))
                            {
                                _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", INDEXED_BUFFER_VALUE_TYPE)), "Resource deletion: %s", oResponse.GetStructuredBuffer("error").ToString().c_str());
                                _ThrowBaseExceptionIf((true == oResponse.IsElementPresent("error", ANSI_CHARACTER_STRING_VALUE_TYPE)), "Resource deletion: %s", oResponse.GetString("error").c_str());
                                _ThrowBaseException("Should never be thrown. Something is horribly wrong.", nullptr);
                            }
                        }
                        else
                        {
                            std::cout << "DeleteAzureResources. Unexpected response from server. Response: " << oResponse.ToString() << std::endl;
                        }
                    }
                    else
                    {
                        std::cout << "DeleteAzureResources. No response from server. Response code: " << nResponseCode << std::endl;
                    }
                }
            }
            while (false == fResourceDeleted);

            fResourceDeleted = false;
            // Wait for the resource to be deleted so that no depenedency is blocked or fails later
            while (false == fResourceDeleted)
            {
                if (true == ::DoesAzureResourceExist(c_strMicrosoftAzureAccessToken, strResourceId))
                {
                    ::sleep(5);
                }
                else
                {
                    fResourceDeleted = true;
                }
            }
        }
    }

    // Check again if all the resources are deleted
    fResourcesDeleted = true;
    for (auto strResourceId : c_stlResourceId)
    {
        if (true == ::DoesAzureResourceExist(c_strMicrosoftAzureAccessToken, strResourceId))
        {
            fResourcesDeleted = false;
            break;
        }
    }

    return fResourcesDeleted;
}
