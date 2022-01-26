#include <Windows.h>

#include "64BitHashes.h"
#include "CompressionHelperFunctions.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "StructuredBuffer.h"
#include "JsonParser.h"
#include "JsonValue.h"
#include "RestApiHelperFunctions.h"
#include "SailApiBaseServices.h"
#include "SharedUtilityFunctions.h"

static std::map<unsigned int, std::string> gs_stlIndexedListOfSerializedBase64DigitalContracts;

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
extern "C" __declspec(dllexport) unsigned int __cdecl LoadDigitalContracts(void)
{
    __DebugFunction();

    // [DllImport("SailWebApiPortalFunctions.dll", CallingConvention = CallingConvention.Cdecl )]
    // static extern public uint LoadDigitalContracts();

    unsigned int unDigitalContractsCount = 0;

    try
    {
        _ThrowBaseExceptionIf((false == ::IsLoggedOn()), "No active session, cannot complete requested operation", nullptr);
        // Build out the REST API call query
        std::string strVerb = "GET";
        std::string strApiUri = "/SAIL/DigitalContractManager/DigitalContracts";
        std::string strJsonBody = "{\n    \"Eosb\": \"" + ::GetSailPlatformServicesEosb() + "\"\n}";
        // Send the REST API call to the SAIL Web Api Portal
        std::vector<Byte> stlRestResponse = ::RestApiCall(::GetSailPlatformServicesIpAddress(), (Word) 6200, strVerb, strApiUri, strJsonBody, true);
        // Parse the returning value.
        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
        // Did the transaction succeed?
        _ThrowBaseExceptionIf((200 != oResponse.GetFloat64("Status")), "Sail Web Api Portal Transaction has failed.", nullptr);
        // Extract the Eosb (in this case an importer EOSB) from the transaction response
        StructuredBuffer oDigitalContracts = oResponse.GetStructuredBuffer("DigitalContracts");
        // Clear the currently cached list of Digital Contracts
        gs_stlIndexedListOfSerializedBase64DigitalContracts.clear();
        // Now let's extract each individual digital contract and registered them in a way
        // were they can be accessed using an index. The StructuredBuffer is a collection of
        // StructuredBuffers whereas the name of each StructuredBuffer is the identifier
        // of the Digital Contract
        unsigned int unIndex = 0;
        for (std::string strElement : oDigitalContracts.GetNamesOfElements())
        {
            StructuredBuffer oElement(oDigitalContracts.GetStructuredBuffer(strElement.c_str()));
            oElement.PutString("DigitalContractIdentifier", strElement);
            gs_stlIndexedListOfSerializedBase64DigitalContracts[unIndex] = oElement.GetBase64SerializedBuffer();
            unIndex++;
        }
        // Return the number of digital contracts downloaded
        __DebugAssert(unIndex == gs_stlIndexedListOfSerializedBase64DigitalContracts.size());
        unDigitalContractsCount = (unsigned int) gs_stlIndexedListOfSerializedBase64DigitalContracts.size();
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return unDigitalContractsCount;
}

/// <summary>
/// 
/// </summary>
/// <param name="unIndex"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl GetDigitalContractIdentifierAtIndex(
    _in unsigned unIndex
    )
{
    __DebugFunction();

    // [DllImport("SailWebApiPortalFunctions.dll", CallingConvention = CallingConvention.Cdecl )]
    // [return: MarshalAs(UnmanagedType.BStr)]
    // static extern public string GetDigitalContractIdentifierAtIndex(uint index);

    std::string strDigitalContractIdentifier;

    try
    {
        _ThrowBaseExceptionIf((false == ::IsLoggedOn()), "No active session, cannot complete requested operation", nullptr);
        // Make sure the index provided is not out of range
        _ThrowBaseExceptionIf((gs_stlIndexedListOfSerializedBase64DigitalContracts.end() == gs_stlIndexedListOfSerializedBase64DigitalContracts.find(unIndex)), "Index (%d) out of maximum range (%d)", unIndex, (gs_stlIndexedListOfSerializedBase64DigitalContracts.size() - 1));
        // Deserialize the Base64 bit serialized StructuredBuffer containing the Digital Contract
        StructuredBuffer oDigitalContract(gs_stlIndexedListOfSerializedBase64DigitalContracts.at(unIndex).c_str());
        // As an optimization, we use GimLet to compute the string hashes of different values at author
        // time so that at runtime, we do not have to do a whole bunch of string compares over and over
        // again
        strDigitalContractIdentifier = oDigitalContract.GetString("DigitalContractIdentifier");
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return ::ConvertToBSTR(strDigitalContractIdentifier);
}
/// <summary>
/// 
/// </summary>
/// <param name="unIndex"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl GetDigitalContractProperty(
    _in const char * c_szDigitalContractIdentifier,
    _in const char * c_szPropertyName
    )
{
    __DebugFunction();

    // [DllImport("SailWebApiPortalFunctions.dll", CallingConvention = CallingConvention.Cdecl )]
    // [return: MarshalAs(UnmanagedType.BStr)]
    // static extern public string GetDigitalContractProperty(string digitalContractIdentifier, string propertyName);

    std::string strDigitalContractProperty;

    try
    {
        _ThrowBaseExceptionIf((false == ::IsLoggedOn()), "No active session, cannot complete requested operation", nullptr);

        for (auto base64SerializedDigitalContract : gs_stlIndexedListOfSerializedBase64DigitalContracts)
        {
            StructuredBuffer oDigitalContract(base64SerializedDigitalContract.second.c_str());
            std::string strDigitalContractIdentifier = oDigitalContract.GetString("DigitalContractIdentifier");
            if (0 == ::_strnicmp(c_szDigitalContractIdentifier, strDigitalContractIdentifier.c_str(), strDigitalContractIdentifier.size()))
            {
                // As an optimization, we use GimLet to compute the string hashes of different values at author
                // time so that at runtime, we do not have to do a whole bunch of string compares over and over
                // again
                switch (::Get64BitHashOfNullTerminatedString(c_szPropertyName, false))
                {
                    case 0x75D4B1A0DB8B9719 // "DigitalContractIdentifier"
                    :   strDigitalContractProperty = oDigitalContract.GetString("DigitalContractIdentifier");
                        break;
                    case 0xBAAEC6D09BC73437 // "VersionNumber"
                    :   strDigitalContractProperty = oDigitalContract.GetString("VersionNumber");
                        break;
                    case 0xE300C5F310350276 // "ContractStage"
                    :   strDigitalContractProperty = std::to_string((uint64_t) oDigitalContract.GetFloat64("ContractStage"));
                        break;
                    case 0x7A2F25973EEED0EE // "SubscriptionDays"
                    :   strDigitalContractProperty = std::to_string((uint64_t) oDigitalContract.GetFloat64("SubscriptionDays"));
                        break;
                    case 0xC7A10710CA77FF2A // "DatasetGuid"
                    :   strDigitalContractProperty = oDigitalContract.GetString("DatasetGuid");
                        break;
                    case 0x31829862E822916F // "ActivationTime"
                    :   strDigitalContractProperty = ::GetDateStringFromEpochMillisecondTimestamp((uint64_t) oDigitalContract.GetFloat64("ActivationTime"));
                        break;
                    case 0xCD578C737408CB7E // "ExpirationTime"
                    :   strDigitalContractProperty = ::GetDateStringFromEpochMillisecondTimestamp((uint64_t) oDigitalContract.GetFloat64("ExpirationTime"));
                        break;
                    case 0x8620265CA83C7F6E // "EulaAcceptedByDOOAuthorizedUser"
                    :   strDigitalContractProperty = oDigitalContract.GetString("EulaAcceptedByDOOAuthorizedUser");
                        break;
                    case 0xAACB401BA7F6F09F // "EulaAcceptedByROAuthorizedUser"
                    :   strDigitalContractProperty = oDigitalContract.GetString("EulaAcceptedByROAuthorizedUser");
                        break;
                    case 0x9A55771E1A635A3A // "LegalAgreement"
                    :   strDigitalContractProperty = oDigitalContract.GetString("LegalAgreement");
                        break;
                    default
                    :   _ThrowBaseException("Invalid Digital Contract property %s specified.", c_szPropertyName);
                        break;
                }

                // Break out of the loop
                break;
            }
        }        
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return ::ConvertToBSTR(strDigitalContractProperty);
}