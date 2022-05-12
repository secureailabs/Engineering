#include <Windows.h>

#include "64BitHashes.h"
#include "CompressionHelperFunctions.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "StructuredBuffer.h"
#include "JsonParser.h"
#include "RestApiHelperFunctions.h"
#include "SailApiBaseServices.h"
#include "SharedUtilityFunctions.h"

#include <map>
#include <mutex>
#include <set>
#include <string>

static std::mutex gs_stlMutex;
static std::set<std::string> gs_stlListOfDatasetFamiliesIdentifiers;
static std::map<Qword, std::string> gs_stlListOfDatasetFamiliesTitles;

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
extern "C" __declspec(dllexport) bool __cdecl UpdateDatasetFamilyInformation(void)
{
    __DebugFunction();

    bool fSuccess = false;

    try
    {
        _ThrowBaseExceptionIf((false == ::IsLoggedOn()), "No active session, cannot complete requested operation", nullptr);
        // Build out the REST API call query
        std::string strVerb = "GET";
        std::string strApiUri = "/datasets-families";
        std::vector<std::string> stlListOfHeaders;
        stlListOfHeaders.push_back("Authorization: Bearer " + ::GetSailPlatformServicesAccessToken());
        std::string strBody = "";
        // Get the list of Dataset Families
        std::vector<Byte> stlRestResponse = ::RestApiCall(::GetSailPlatformServicesIpAddress(), (Word)8000, strVerb, strApiUri, strBody, true, stlListOfHeaders);
        // Parse the returning value.
        StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());

        // Did the transaction succeed?
        _ThrowBaseExceptionIf((false == oResponse.IsElementPresent("dataset_families", INDEXED_BUFFER_VALUE_TYPE)), "Failed to get dataset families.", nullptr);

        // Now we extract the digital families information
        if (true == oResponse.IsElementPresent("dataset_families", INDEXED_BUFFER_VALUE_TYPE))
        {
            StructuredBuffer oDatasetFamilies(oResponse.GetStructuredBuffer("dataset_families"));

            std::vector<std::string> stlListOfDatasetFamilies = oDatasetFamilies.GetNamesOfElements();
            const std::lock_guard<std::mutex> lock(gs_stlMutex);
            for (std::string strDatasetFamilyIdentifier: stlListOfDatasetFamilies)
            {
                if (true == oDatasetFamilies.IsElementPresent(strDatasetFamilyIdentifier.c_str(), INDEXED_BUFFER_VALUE_TYPE))
                {
                    StructuredBuffer oDatasetFamily(oDatasetFamilies.GetStructuredBuffer(strDatasetFamilyIdentifier.c_str()));
                    Qword qwHashOfDatasetFamilyIdentifier = ::Get64BitHashOfNullTerminatedString(oDatasetFamily.GetString("id").c_str(), false);

                    __DebugAssert(true == oDatasetFamily.IsElementPresent("id", ANSI_CHARACTER_STRING_VALUE_TYPE));

                    gs_stlListOfDatasetFamiliesIdentifiers.insert(oDatasetFamily.GetString("id"));
                    gs_stlListOfDatasetFamiliesTitles[qwHashOfDatasetFamilyIdentifier] = oDatasetFamily.GetString("name");
                }
            }
        }
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
/// <param name=""></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl GetListOfDatasetFamilyIdentifiers(void)
{
    __DebugFunction();

    std::string strCommaDelimitedListOfDatasetFamilyIdentifiers;

    try
    {
        const std::lock_guard<std::mutex> lock(gs_stlMutex);
        // Generate a comma delimite list of dataset family identifiers
        for (std::string strDatasetFamilyIdentifier: gs_stlListOfDatasetFamiliesIdentifiers)
        {
            strCommaDelimitedListOfDatasetFamilyIdentifiers += strDatasetFamilyIdentifier;
            strCommaDelimitedListOfDatasetFamilyIdentifiers.push_back(',');
        }
        if (0 < strCommaDelimitedListOfDatasetFamilyIdentifiers.length())
        {
            // Delete the last character in the string, since it's a superfluous comma
            strCommaDelimitedListOfDatasetFamilyIdentifiers.erase(strCommaDelimitedListOfDatasetFamilyIdentifiers.end() - 1);
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return ::ConvertToBSTR(strCommaDelimitedListOfDatasetFamilyIdentifiers);
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szDatasetFamilyTitle"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl GetDatasetFamilyTitle(
    _in const char * c_szDatasetFamilyIdentifier
    )
{
    __DebugFunction();

    std::string strDatasetFamilyTitle;

    try
    {
        const std::lock_guard<std::mutex> lock(gs_stlMutex);
        Qword qwHashOfDatasetFamilyIdentifier = ::Get64BitHashOfNullTerminatedString(c_szDatasetFamilyIdentifier, false);
        if (gs_stlListOfDatasetFamiliesTitles.end() != gs_stlListOfDatasetFamiliesTitles.find(qwHashOfDatasetFamilyIdentifier))
        {
            strDatasetFamilyTitle = gs_stlListOfDatasetFamiliesTitles[qwHashOfDatasetFamilyIdentifier];
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return ::ConvertToBSTR(strDatasetFamilyTitle);
}