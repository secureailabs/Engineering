/*********************************************************************************************
 *
 * @file CurlRest.cpp
 * @author Prawal Gangwar
 * @date 10 Sept 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "JsonParser.h"
#include "StructuredBuffer.h"
#include "Utils.h"

#include <curl/curl.h>

#include <iostream>
#include <string>
#include <vector>
#include <map>

/********************************************************************************************
 *
 * @function CurlWriteCallback
 * @brief Callback function used by psCurl to write data to the vector
 * @param[in] c_pszData pointer to the data pointer
 * @return Keys in JsonObject
 *
 ********************************************************************************************/
static size_t __stdcall CurlHeaderWriteCallback(
    _in const Byte * c_pbAdditionalData,
    _in size_t unSizeOfElements,
    _in size_t unNumberOfElements,
    _in std::map<std::string, std::string> * pstlHeaderMap
    ) throw()
{
    __DebugFunction();

    try
    {
        std::string strHeader((char*) c_pbAdditionalData, unSizeOfElements * unNumberOfElements);
        size_t nSeperatorIndex = strHeader.find_first_of(":");

        if (std::string::npos != nSeperatorIndex)
        {
            std::string strHeaderKey = strHeader.substr(0, nSeperatorIndex);
            std::string strHeaderValue = strHeader.substr(nSeperatorIndex + 1, strHeader.length() - nSeperatorIndex - 3);

            pstlHeaderMap->insert(std::make_pair(strHeaderKey, strHeaderValue));
        }
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return unSizeOfElements * unNumberOfElements;
}

/********************************************************************************************
 *
 * @function CurlWriteCallback
 * @brief Callback function used by psCurl to write data to the vector
 * @param[in] c_pszData pointer to the data pointer
 * @return Keys in JsonObject
 *
 ********************************************************************************************/
static size_t __stdcall CurlWriteCallback(
    _in const Byte * c_pbAdditionalData,
    _in size_t unSizeOfElements,
    _in size_t unNumberOfElements,
    _in std::vector<Byte> * pstlResponseBuffer
    ) throw()
{
    __DebugFunction();

    // Store the number of bytes received / taken care of by the callback function
    unsigned int unNumberOfBytesReceived = 0;

    try
    {
        if (nullptr != pstlResponseBuffer)
        {
            // Only append additional data if the incoming parameters are valid
            if ((nullptr != c_pbAdditionalData) && (0 < unSizeOfElements) && (0 < unNumberOfElements))
            {
                // Figure out how many additional bytes will be we appending to the existing response buffer
                unNumberOfBytesReceived = (unsigned int) (unSizeOfElements * unNumberOfElements);
                pstlResponseBuffer->insert(pstlResponseBuffer->end(), c_pbAdditionalData, (c_pbAdditionalData + unNumberOfBytesReceived));
            }
        }
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return unNumberOfBytesReceived;
}

/********************************************************************************************
 *
 * @function RestApiCall
 * @brief Make Rest API calls using psCurl
 * @param[in] c_pszData pointer to the data pointer
 * @return Rest Response
 *
 ********************************************************************************************/

std::vector<Byte> __stdcall RestApiCall(
    _in const std::string & c_strHostIpAddress,
    _in const Word nPort,
    _in const std::string & c_strVerb,
    _in const std::string & c_strApiUri,
    _in const std::string & c_strJsonBody,
    _in bool fIsJsonResponse
    ) throw()
{
    __DebugFunction();

    std::vector<Byte> stlResponse;

    try
    {
        // Initialize CURL
        CURL * psCurl = nullptr;
        ::curl_global_init(CURL_GLOBAL_DEFAULT);
        psCurl = ::curl_easy_init();
        _ThrowBaseExceptionIf((nullptr == psCurl), "curl_easy_init() has failed", nullptr);

        // Disable diagnostic messages
        ::curl_easy_setopt(psCurl, CURLOPT_VERBOSE, 0L);
        std::string strUrl = "https://" + c_strHostIpAddress + ":" + std::to_string(nPort) + c_strApiUri;
        ::curl_easy_setopt(psCurl, CURLOPT_CUSTOMREQUEST, c_strVerb.c_str());
        ::curl_easy_setopt(psCurl, CURLOPT_URL, strUrl.c_str());
        ::curl_easy_setopt(psCurl, CURLOPT_POSTFIELDS, c_strJsonBody.c_str());
        // Disbaling the SSL certificate verification
        ::curl_easy_setopt(psCurl, CURLOPT_SSL_VERIFYPEER, 0L); //only for https
        ::curl_easy_setopt(psCurl, CURLOPT_SSL_VERIFYHOST, 0L); //only for https
        ::curl_easy_setopt(psCurl, CURLOPT_WRITEFUNCTION, CurlWriteCallback);
        ::curl_easy_setopt(psCurl, CURLOPT_WRITEDATA, &stlResponse);
        if (0 < c_strJsonBody.length())
        {
            struct curl_slist * psHeaders = nullptr;
            psHeaders = ::curl_slist_append(psHeaders, "Content-Type: application/json");
            psHeaders = ::curl_slist_append(psHeaders, "Accept: */*");
            psHeaders = ::curl_slist_append(psHeaders, "Host: localhost:6200");
            ::curl_easy_setopt(psCurl, CURLOPT_HTTPHEADER, psHeaders);
        }

        // Execute the API call
        unsigned int unResponse = ::curl_easy_perform(psCurl);
        ::curl_easy_cleanup(psCurl);
        if (CURLE_OK == unResponse)
        {
            if (true == fIsJsonResponse)
            {
                // Make sure there is a null-terminating character
                stlResponse.insert(stlResponse.end(), 0);
            }
        }
        else if (true == fIsJsonResponse)
        {
            // stlResponse = "{\n\t"Status"=400\n}"
            stlResponse = { 0x7b, 0x0a, 0x09, 0x22, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x22, 0x3d, 0x34, 0x30, 0x30, 0x0a, 0x7d };
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

    return stlResponse;
}

/********************************************************************************************
 *
 * @function RestApiCall
 * @brief Make Rest API calls using psCurl
 * @param[in] c_pszData pointer to the data pointer
 * @return Rest Response
 *
 ********************************************************************************************/
std::vector<Byte> __stdcall RestApiCall(
    _in const std::string & c_strHostIpAddress,
    _in const Word nPort,
    _in const std::string & c_strVerb,
    _in const std::string & c_strApiUri,
    _in const std::string & c_strContent,
    _in bool fDisableSslCertificateVerification,
    _in const std::vector<std::string> & c_stlListOfHeaders,
    _out long * nResponseCode
    ) throw()
{
    __DebugFunction();

    std::vector<Byte> stlResponse;

    try
    {
        // Initialize CURL
        CURL * psCurl = nullptr;
        ::curl_global_init(CURL_GLOBAL_DEFAULT);
        psCurl = ::curl_easy_init();
        _ThrowBaseExceptionIf((nullptr == psCurl), "curl_easy_init() has failed", nullptr);

        // Disable diagnostic messages
        ::curl_easy_setopt(psCurl, CURLOPT_VERBOSE, 0L);

        std::string strUrl = "https://" + c_strHostIpAddress + ":" + std::to_string(nPort) + c_strApiUri;
        ::curl_easy_setopt(psCurl, CURLOPT_CUSTOMREQUEST, c_strVerb.c_str());
        ::curl_easy_setopt(psCurl, CURLOPT_URL, strUrl.c_str());
        ::curl_easy_setopt(psCurl, CURLOPT_POSTFIELDS, c_strContent.c_str());

        // Disaling the SSL certificate verification
        if (true == fDisableSslCertificateVerification)
        {
            ::curl_easy_setopt(psCurl, CURLOPT_SSL_VERIFYPEER, 0L); //only for https
            ::curl_easy_setopt(psCurl, CURLOPT_SSL_VERIFYHOST, 0L); //only for https
        }

        // Setup callback for Header Write
        ::curl_easy_setopt(psCurl, CURLOPT_HEADERFUNCTION, CurlHeaderWriteCallback);
        std::map<std::string, std::string> stlMapOfHeaders;
        ::curl_easy_setopt(psCurl, CURLOPT_HEADERDATA, &stlMapOfHeaders);
        // Setup callback function for the response body
        ::curl_easy_setopt(psCurl, CURLOPT_WRITEFUNCTION, CurlWriteCallback);
        ::curl_easy_setopt(psCurl, CURLOPT_WRITEDATA, &stlResponse);
        struct curl_slist * psHeaders = nullptr;
        // Append all the headers to the request
        for (const std::string & c_strSingleHeader : c_stlListOfHeaders)
        {
            psHeaders = ::curl_slist_append(psHeaders, c_strSingleHeader.c_str());
        }
        ::curl_easy_setopt(psCurl, CURLOPT_HTTPHEADER, psHeaders);

        // Execute the API call
        unsigned int unResponse = ::curl_easy_perform(psCurl);
        ::curl_easy_cleanup(psCurl);
        stlResponse.insert(stlResponse.end(), 0);
        if (CURLE_OK == unResponse)
        {
            // Save the response HTTP code
            if (nullptr != nResponseCode)
            {
                ::curl_easy_getinfo(psCurl, CURLINFO_RESPONSE_CODE, nResponseCode);
            }
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

    return stlResponse;
}

/********************************************************************************************
 *
 * @function RestApiCall
 * @brief Make Rest API calls using psCurl
 * @param[in] c_pszData pointer to the data pointer
 * @return Rest Response
 *
 ********************************************************************************************/
std::vector<Byte> __stdcall RestApiCall(
    _in const std::string & c_strHostIpAddress,
    _in const Word nPort,
    _in const std::string & c_strVerb,
    _in const std::string & c_strApiUri,
    _in const std::string & c_strContent,
    _in bool fDisableSslCertificateVerification,
    _in const std::vector<std::string> & c_stlListOfHeaders
    ) throw()
{
    __DebugFunction();

    return ::RestApiCall(c_strHostIpAddress, nPort, c_strVerb, c_strApiUri, c_strContent, fDisableSslCertificateVerification, c_stlListOfHeaders, nullptr);
}

/********************************************************************************************
 *
 * @function RestApiCall
 * @brief Make Rest API calls using psCurl
 * @param[in] c_pszData pointer to the data pointer
 * @return Rest Response
 *
 ********************************************************************************************/
std::vector<Byte> __stdcall RestApiCall(
    _in const std::string & c_strHostIpAddress,
    _in const Word nPort,
    _in const std::string & c_strVerb,
    _in const std::string & c_strApiUri,
    _in const std::string & c_strContent,
    _in bool fDisableSslCertificateVerification,
    _in const std::vector<std::string> & c_stlListOfHeaders,
    _in const std::map<std::string, std::string> * stlMapOfHeaders,
    _inout long * nResponseCode
    ) throw()
{
    __DebugFunction();

    std::vector<Byte> stlResponse;

    try
    {
        // Initialize CURL
        CURL * psCurl = nullptr;
        ::curl_global_init(CURL_GLOBAL_DEFAULT);
        psCurl = ::curl_easy_init();
        _ThrowBaseExceptionIf((nullptr == psCurl), "curl_easy_init() has failed", nullptr);

        // Disable diagnostic messages
        ::curl_easy_setopt(psCurl, CURLOPT_VERBOSE, 0L);

        std::string strUrl = "https://" + c_strHostIpAddress + ":" + std::to_string(nPort) + c_strApiUri;
        ::curl_easy_setopt(psCurl, CURLOPT_CUSTOMREQUEST, c_strVerb.c_str());
        ::curl_easy_setopt(psCurl, CURLOPT_URL, strUrl.c_str());
        ::curl_easy_setopt(psCurl, CURLOPT_POSTFIELDS, c_strContent.c_str());

        // Disaling the SSL certificate verification
        if (true == fDisableSslCertificateVerification)
        {
            ::curl_easy_setopt(psCurl, CURLOPT_SSL_VERIFYPEER, 0L); //only for https
            ::curl_easy_setopt(psCurl, CURLOPT_SSL_VERIFYHOST, 0L); //only for https
        }

        // Setup callback for Header Write
        ::curl_easy_setopt(psCurl, CURLOPT_HEADERFUNCTION, CurlHeaderWriteCallback);
        ::curl_easy_setopt(psCurl, CURLOPT_HEADERDATA, stlMapOfHeaders);
        // Setup callback function for the response body
        ::curl_easy_setopt(psCurl, CURLOPT_WRITEFUNCTION, CurlWriteCallback);
        ::curl_easy_setopt(psCurl, CURLOPT_WRITEDATA, &stlResponse);
        struct curl_slist * psHeaders = nullptr;
        // Append all the headers to the request
        for (const std::string & c_strSingleHeader : c_stlListOfHeaders)
        {
            psHeaders = ::curl_slist_append(psHeaders, c_strSingleHeader.c_str());
        }
        ::curl_easy_setopt(psCurl, CURLOPT_HTTPHEADER, psHeaders);

        // Execute the API call
        unsigned int unResponse = ::curl_easy_perform(psCurl);
        ::curl_easy_cleanup(psCurl);
        stlResponse.insert(stlResponse.end(), 0);
        if (CURLE_OK == unResponse)
        {
            // Save the response HTTP code
            if (nullptr != nResponseCode)
            {
                ::curl_easy_getinfo(psCurl, CURLINFO_RESPONSE_CODE, nResponseCode);
            }
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

    return stlResponse;
}


std::vector<Byte> __stdcall RestApiCallHTTP(
    _in const std::string & c_strHostIpAddress,
    _in const Word nPort,
    _in const std::string & c_strVerb,
    _in const std::string & c_strApiUri,
    _in const std::string & c_strContent,
    _in bool fDisableSslCertificateVerification,
    _in const std::vector<std::string> & c_stlListOfHeaders,
    _out long * nResponseCode
    ) throw()
{
    __DebugFunction();

    std::vector<Byte> stlResponse;

    try
    {
        // Initialize CURL
        CURL * psCurl = nullptr;
        ::curl_global_init(CURL_GLOBAL_DEFAULT);
        psCurl = ::curl_easy_init();
        _ThrowBaseExceptionIf((nullptr == psCurl), "curl_easy_init() has failed", nullptr);

        // Disable diagnostic messages
        ::curl_easy_setopt(psCurl, CURLOPT_VERBOSE, 0L);

        std::string strUrl = "http://" + c_strHostIpAddress + ":" + std::to_string(nPort) + c_strApiUri;
        ::curl_easy_setopt(psCurl, CURLOPT_CUSTOMREQUEST, c_strVerb.c_str());
        ::curl_easy_setopt(psCurl, CURLOPT_URL, strUrl.c_str());
        ::curl_easy_setopt(psCurl, CURLOPT_POSTFIELDS, c_strContent.c_str());

        // Disaling the SSL certificate verification
        if (true == fDisableSslCertificateVerification)
        {
            ::curl_easy_setopt(psCurl, CURLOPT_SSL_VERIFYPEER, 0L); //only for https
            ::curl_easy_setopt(psCurl, CURLOPT_SSL_VERIFYHOST, 0L); //only for https
        }

        // Setup callback for Header Write
        ::curl_easy_setopt(psCurl, CURLOPT_HEADERFUNCTION, CurlHeaderWriteCallback);
        std::map<std::string, std::string> stlMapOfHeaders;
        ::curl_easy_setopt(psCurl, CURLOPT_HEADERDATA, &stlMapOfHeaders);
        // Setup callback function for the response body
        ::curl_easy_setopt(psCurl, CURLOPT_WRITEFUNCTION, CurlWriteCallback);
        ::curl_easy_setopt(psCurl, CURLOPT_WRITEDATA, &stlResponse);
        struct curl_slist * psHeaders = nullptr;
        // Append all the headers to the request
        for (const std::string & c_strSingleHeader : c_stlListOfHeaders)
        {
            psHeaders = ::curl_slist_append(psHeaders, c_strSingleHeader.c_str());
        }
        ::curl_easy_setopt(psCurl, CURLOPT_HTTPHEADER, psHeaders);

        // Execute the API call
        unsigned int unResponse = ::curl_easy_perform(psCurl);
        ::curl_easy_cleanup(psCurl);
        stlResponse.insert(stlResponse.end(), 0);
        if (CURLE_OK == unResponse)
        {
            // Save the response HTTP code
            if (nullptr != nResponseCode)
            {
                ::curl_easy_getinfo(psCurl, CURLINFO_RESPONSE_CODE, nResponseCode);
            }
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

    return stlResponse;
}

