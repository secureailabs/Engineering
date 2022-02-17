/*********************************************************************************************
 *
 * @file ApiCallHelpers.h
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/
 
#include "ApiCallHelpers.h"
#include "Base64Encoder.h"
#include "CurlRest.h"
#include "DateAndTime.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "HttpRequestParser.h"
#include "JsonParser.h"
#include "JsonValue.h"
#include "SmartMemoryAllocator.h"
#include "StructuredBuffer.h"
#include "TlsClient.h"
#include "Utils.h"

#include <iostream>
#include <string>
#include <sstream>
#include <vector>

static std::string gs_strIpAddressOfWebPortalGateway;
static unsigned int gs_unPortAddressOfWebPortalGateway = 0;
    
/*********************************************************************************************/

bool __stdcall SetIpAddressOfSailWebApiPortalGateway(
    _in const std::string & c_strIpAddressOfWebPortalGateway,
    _in Word wPortAddressOfWebPortalGateway
    ) throw()
{
    __DebugFunction();
    __DebugAssert(0 == gs_strIpAddressOfWebPortalGateway.size());
    __DebugAssert(0 < c_strIpAddressOfWebPortalGateway.size());

    // TODO: Hook to IP resolution function
    gs_strIpAddressOfWebPortalGateway = c_strIpAddressOfWebPortalGateway;
    gs_unPortAddressOfWebPortalGateway = wPortAddressOfWebPortalGateway;

    return true;
}

/*********************************************************************************************/

std::string __stdcall LoginToSailWebApiPortal(
    _in const std::string & c_strUsername,
    _in const std::string & c_strPassword
    )
{
    __DebugFunction();
    __DebugAssert(0 < gs_strIpAddressOfWebPortalGateway.size());
    __DebugAssert(0 != gs_unPortAddressOfWebPortalGateway);
    
    std::string strEosb;

    // Build the HTTP request
    std::string strVerb = "POST";
    std::string strApiUrl = "/SAIL/AuthenticationManager/User/Login?Email="+ c_strUsername +"&Password="+ c_strPassword;
    std::string strJsonBody = "";
    // Make the API call and get REST response
    std::vector<Byte> stlRestResponse = ::RestApiCall(gs_strIpAddressOfWebPortalGateway, (Word) gs_unPortAddressOfWebPortalGateway, strVerb, strApiUrl, strJsonBody, true);
    StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
    _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Failed REST Response", nullptr);
    strEosb = oResponse.GetString("Eosb");
    
    return strEosb;
}

/*********************************************************************************************/

StructuredBuffer __stdcall GetSailWebApiPortalBasicUserInformation(
    _in const std::string & c_strEosb
    )
{
    __DebugFunction();
    __DebugAssert(0 < c_strEosb.size());
	
    StructuredBuffer oResponse;
    
    try
    {
        // By default
        oResponse.PutBoolean("Success", false);
        // Build the HTTP request string
        std::string strVerb = "GET";
        std::string strApiUrl = "/SAIL/AuthenticationManager/GetBasicUserInformation?Eosb="+ c_strEosb;
        std::string strJsonBody = "";
        // Make the API call and get REST response
        std::vector<Byte> stlRestResponse = ::RestApiCall(gs_strIpAddressOfWebPortalGateway, (Word) gs_unPortAddressOfWebPortalGateway, strVerb, strApiUrl, strJsonBody, true);
        // Convert the JSON response into a StructuredBuffer for internal use
        oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
        // Throw an exception if the API call to the SAIL Platform Services API Gateway has failed
        _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "API call to GetBasicUserInformation has failed", nullptr);
        // Make sure that the StructuredBuffer returned to the caller contains Success = true
        oResponse.PutBoolean("Success", true);
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    return oResponse;
}

/*********************************************************************************************/

bool __stdcall TransmitAuditEventsToSailWebApiPortal(
    _in const std::string & c_strEosb,
    _in const std::string & c_strParentBranchNodeIdentifier,
    _in const StructuredBuffer & c_oAuditEvents
    )
{
    __DebugFunction();
    
    bool fSuccess = false;
    
    try
    {
        if ((0 < c_strEosb.size())&&(0 < c_strParentBranchNodeIdentifier.size()))
        {
            // Build the HTTP request string
            StructuredBuffer oApiBodyContent;
            std::string strVerb = "POST";
            std::string strApiUrl = "/SAIL/AuditLogManager/LeafEvents?Eosb="+ c_strEosb;
            oApiBodyContent.PutString("ParentGuid", c_strParentBranchNodeIdentifier);
            oApiBodyContent.PutStructuredBuffer("LeafEvents", c_oAuditEvents);
            // Make the API call and get REST response
            std::vector<Byte> stlRestResponse = ::RestApiCall(gs_strIpAddressOfWebPortalGateway, (Word) gs_unPortAddressOfWebPortalGateway, strVerb, strApiUrl, ::ConvertStructuredBufferToJson(oApiBodyContent), true);
            StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
            _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Failed REST Response", nullptr);
            fSuccess = true;
        }
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    return fSuccess;
}

/*********************************************************************************************/

StructuredBuffer __stdcall GetListOfDigitalContracts(
    _in const std::string & c_strEosb
    )
{
    __DebugFunction();
    
    StructuredBuffer oListOfDigitalContracts;
    
    try
    {
        if (0 < c_strEosb.size())
        {
            // By default
            oListOfDigitalContracts.PutBoolean("Success", false);
            // Build the HTTP request string
            std::string strVerb = "GET";
            std::string strApiUrl = "/SAIL/DigitalContractManager/DigitalContracts?Eosb="+ c_strEosb;
            std::string strJsonBody = "";
            // Make the API call and get REST response
            std::vector<Byte> stlRestResponse = ::RestApiCall(gs_strIpAddressOfWebPortalGateway, (Word) gs_unPortAddressOfWebPortalGateway, strVerb, strApiUrl, strJsonBody, true);
            StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
            _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "Failed REST Response", nullptr);
            oListOfDigitalContracts.PutStructuredBuffer("ListOfDigitalContracts", oResponse.GetStructuredBuffer("DigitalContracts"));
            oListOfDigitalContracts.PutBoolean("Success", true);
        }
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    return oListOfDigitalContracts;
}

/*********************************************************************************************/

StructuredBuffer __stdcall GetDigitalContract(
    _in const std::string & c_strEosb,
    _in const Guid & c_oDigitalContractIdentifier
    )
{
    __DebugFunction();
    
    StructuredBuffer oDigitalContract;
    
    try
    {
        if (0 < c_strEosb.size())
        {
            // By default
            oDigitalContract.PutBoolean("Success", false);
            // Build the HTTP request string
            StructuredBuffer oApiBodyContent;
            std::string strVerb = "GET";
            std::string strApiUrl = "/SAIL/DigitalContractManager/PullDigitalContract?Eosb="+ c_strEosb;
            oApiBodyContent.PutString("DigitalContractGuid", c_oDigitalContractIdentifier.ToString(eHyphensAndCurlyBraces));
            // Make the API call and get REST response
            std::vector<Byte> stlRestResponse = ::RestApiCall(gs_strIpAddressOfWebPortalGateway, (Word) gs_unPortAddressOfWebPortalGateway, strVerb, strApiUrl, ::ConvertStructuredBufferToJson(oApiBodyContent), true);
            StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
            _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "Error getting list of digital contracts.", nullptr);
            oDigitalContract.PutStructuredBuffer("DigitalContract", oResponse.GetStructuredBuffer("DigitalContract"));
            oDigitalContract.PutBoolean("Success", true);
        }
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oDigitalContract.Clear();
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oDigitalContract.Clear();
        oDigitalContract.PutBoolean("Success", false);
    }
    
    return oDigitalContract;
}

/********************************************************************************************/

StructuredBuffer __stdcall RegisterVirtualMachineAfterInitialization(
    _in const std::string & c_strEosb,
    _in const std::string & c_strVirtualMachineIdentifier,
    _in const std::string & c_strDigitalContractIdentifier,
    _in const std::string & c_strIpAddress
    ) throw()
{
    __DebugFunction();
    __DebugAssert(0 < c_strEosb.size());
    __DebugAssert(0 < c_strVirtualMachineIdentifier.size());

    StructuredBuffer oResponse;

    try
    {
        // Build the HTTP request string
        StructuredBuffer oApiBodyContent;
        std::string strVerb = "POST";
        // HACK-DG - Confirm when we need the EOSB/IEOSB?
        std::string strApiUrl = "/SAIL/VirtualMachineManager/RegisterVM?Eosb="+ c_strEosb;
        oApiBodyContent.PutString("DigitalContractGuid", c_strDigitalContractIdentifier);
        oApiBodyContent.PutString("VirtualMachineGuid", c_strVirtualMachineIdentifier);
        oApiBodyContent.PutString("HeartbeatBroadcastTime", std::to_string(::GetEpochTimeInSeconds()));
        oApiBodyContent.PutString("IPAddress", c_strIpAddress);
        // HACK-DG - Hardcoded these values that aren't passed in and the remote expects
        oApiBodyContent.PutUnsignedInt64("NumberOfVCPU", 1);
        oApiBodyContent.PutString("HostRegion", "USEast");
        oApiBodyContent.PutUnsignedInt64("StartTime", 1);
        oApiBodyContent.PutString("DigitalContractTitle", "Test title");
        // Make the API call and get REST response
        std::cout << "Submitting request " << oApiBodyContent.ToString() << " to " << strApiUrl << std::endl;
        std::vector<Byte> stlRestResponse = ::RestApiCall(gs_strIpAddressOfWebPortalGateway, (Word) gs_unPortAddressOfWebPortalGateway, strVerb, strApiUrl, ::ConvertStructuredBufferToJson(oApiBodyContent), true);
        oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
        _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Error while processing the transaction.", nullptr);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return oResponse;
}

/********************************************************************************************/

StructuredBuffer __stdcall RegisterVirtualMachineDataOwner(
    _in const std::string & c_strEosb,
    _in const std::string & c_strVirtualMachineIdentifier
    ) throw()
{
    __DebugFunction();
    __DebugAssert(0 < c_strEosb.size());
    __DebugAssert(0 < c_strVirtualMachineIdentifier.size());

    StructuredBuffer oResponse;

    try
    {
        // Build the HTTP request string
        StructuredBuffer oApiBodyContent;
        std::string strVerb = "POST";
        std::string strApiUrl = "/SAIL/VirtualMachineManager/DataOwner/RegisterVM?Eosb="+ c_strEosb;
        oApiBodyContent.PutString("VirtualMachineGuid", c_strVirtualMachineIdentifier);
        // Make the API call and get REST response
        std::vector<Byte> stlRestResponse = ::RestApiCall(gs_strIpAddressOfWebPortalGateway, (Word) gs_unPortAddressOfWebPortalGateway, strVerb, strApiUrl, ::ConvertStructuredBufferToJson(oApiBodyContent), true);
        oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
        _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Error while processing the transaction.", nullptr);
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return oResponse;
}

/********************************************************************************************/

StructuredBuffer __stdcall RegisterVirtualMachineResearchUser(
    _in const std::string & c_strEosb,
    _in const std::string & c_strVirtualMachineIdentifier
    ) throw()
{
    __DebugFunction();
    __DebugAssert(0 < c_strEosb.size());
    __DebugAssert(0 < c_strVirtualMachineIdentifier.size());

    StructuredBuffer oResponse;

    try
    {
        // Build the HTTP request string
        std::string strVerb = "POST";
        std::string strApiUrl = "/SAIL/VirtualMachineManager/Researcher/RegisterVM?Eosb="+ c_strEosb;
        std::string strContent = "{\n    \"VirtualMachineGuid\": \""+ c_strVirtualMachineIdentifier +"\""
                                "\n}";
        // Make the API call and get REST response
        std::vector<Byte> stlRestResponse = ::RestApiCall(gs_strIpAddressOfWebPortalGateway, (Word) gs_unPortAddressOfWebPortalGateway, strVerb, strApiUrl, strContent, true);
        oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
        _ThrowBaseExceptionIf((201 != oResponse.GetFloat64("Status")), "Error while processing the transaction.", nullptr);
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return oResponse;
}

/// <summary>
/// This function is used to send a virtual machine heartbeat to the SAIL Platform Services API Gateway
/// </summary>
/// <param name="c_strEosb">This can be the EOSB of the researcher or data owner within the Secure Computational VM</param>
/// <param name="c_strVirtualMachineIdentifier">Virtual machine identifier</param>
/// <param name="dwState"></param>
/// <param name="c_strLoggedOnUserIdentifier">Virtual machine state as defined by VirtualMachineState</param>
/// <returns>Nothing</returns>
bool __stdcall VirtualMachineStatusUpdate(
	_in const std::string & c_strEosb,
	_in const std::string & c_strVirtualMachineIdentifier,
	_in Dword dwState,
	_in const std::string & c_strLoggedOnUserIdentifier
	) throw()
{
	__DebugFunction();
	__DebugAssert(0 < c_strEosb.size());
	__DebugAssert(0 < c_strVirtualMachineIdentifier.size());
	__DebugAssert((1 <= dwState)&&(10 >= dwState));
	
	bool fSuccess = false;
	
	try
    {
        // Build the HTTP request string
        StructuredBuffer oApiCallContent;
        std::string strVerb = "POST";
        std::string strApiUrl = "/SAIL/VirtualMachineManager/Researcher/RegisterVM?Eosb=" + c_strEosb;
		oApiCallContent.PutString("VirtualMachineGuid", c_strVirtualMachineIdentifier);
		oApiCallContent.PutDword("State", dwState);
		oApiCallContent.PutString("VMLoggedInUser", c_strLoggedOnUserIdentifier);
		// Make the API call and get REST response
        std::vector<Byte> stlRestResponse = ::RestApiCall(gs_strIpAddressOfWebPortalGateway, (Word) gs_unPortAddressOfWebPortalGateway, strVerb, strApiUrl, ::ConvertStructuredBufferToJson(oApiCallContent), true);
		// Convert the API call response into a StructuredBuffer
        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
		// Throw an exception if the API call did not succeed.
        _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "Error while processing the transaction.", nullptr);
		// Api call has succeeded if we get here
		fSuccess = true;
    }
    
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return fSuccess;
}