/*********************************************************************************************
 *
 * @file Utils.cpp
 * @author Shabana Akhtar Baig
 * @date 16 Dec 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "Utils.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"

#include <algorithm>
#include <cctype>
#include <cstring>
#include <sstream>

/********************************************************************************************
 *
 * @function IsNumber
 * @brief Check if the argument is a number
 * @param[in] c_strValue string value
 * @return true if its a number
 * @return false otherwise
 *
 ********************************************************************************************/

bool __stdcall IsNumber(
    _in const std::string & c_strValue
    )
{
    __DebugFunction();

    bool fIsNumber = !c_strValue.empty() && std::all_of(c_strValue.begin(), c_strValue.end(), ::isdigit);

    return fIsNumber;
}

/********************************************************************************************
 *
 * @function IsBoolean
 * @brief Check if the argument is a boolean
 * @param[in] c_strValue string value
 * @return true if its a boolean
 * @return false otherwise
 *
 ********************************************************************************************/

bool __stdcall IsBoolean(
    _in const std::string & c_strValue
    )
{
    __DebugFunction();

    bool fIsBoolean = false;

    if ((4 == c_strValue.length()) && (0 == strncasecmp(c_strValue.c_str(), "true", 4)))
    {
        fIsBoolean = true;
    }
    else if ((5 == c_strValue.length()) && (0 == strncasecmp(c_strValue.c_str(), "false", 5)))
    {
        fIsBoolean = true;
    }

    return fIsBoolean;
}

/********************************************************************************************
 *
 * @function EscapeJsonString
 * @brief Escape json string
 * @param[in] c_strData json string
 * @param[in] fPutInQuotes wrap the string in quotes if true
 * @return escaped string
 *
 ********************************************************************************************/

std::string __stdcall EscapeJsonString(
    _in const std::string & c_strData,
    _in bool fPutInQuotes
    )
{
    __DebugFunction();

    std::string strStringValue;
    std::string::const_iterator itrData = c_strData.begin();

    if (true == fPutInQuotes)
    {
        strStringValue = "\"";
    }

    while (c_strData.end() != itrData)
    {
        char szCurrentChar = *itrData;

        switch(szCurrentChar)
        {
            case '"'
            :
                strStringValue += "\\\"";
                break;
            case '\\'
            :
                strStringValue += "\\\\";
                break;
            case '/'
            :
                strStringValue += "\\/";
                break;
            case '\b'
            :
                strStringValue += "\\b";
                break;
            case '\n'
            :
                strStringValue += "\\n";
                break;
            case '\r'
            :
                strStringValue += "\\r";
                break;
            case '\t'
            :
                strStringValue += "\\t";
                break;
            case '\f'
            :
                strStringValue += "\\f";
                break;
            default
            :
            {
                if ('\x00' <= *itrData && *itrData <= '\x1f') 
                {
                    char chUnicode[20];
                    snprintf(chUnicode, sizeof(chUnicode), "\\u%04x", *itrData);
                    strStringValue += std::string(chUnicode);
                } 
                else {
                    strStringValue += szCurrentChar;
                }
                break;
            }
        }
        ++itrData;
    }

    if (true == fPutInQuotes)
    {
        strStringValue += "\"";
    }

    return strStringValue;
}

/********************************************************************************************
 *
 * @function UnEscapeJsonString
 * @brief Unescape json string
 * @param[in] c_strData json string
 * @return unescaped string
 *
 ********************************************************************************************/

std::string __stdcall UnEscapeJsonString(
    _in const std::string & c_strData
    )
{
    __DebugFunction();

    std::string strStringValue;
    bool fEscaped = false;

    std::string::const_iterator itrData = c_strData.begin();

    while (c_strData.end() != itrData)
    {
        char szCurrentChar = *itrData;

        // Unescape charaters
        if (true == fEscaped)
        {
            switch(szCurrentChar)
            {
                case '"'
                :
                    strStringValue += '"';
                    break;
                case '\\'
                :
                    strStringValue += '\\';
                    break;
                case '/'
                :
                    strStringValue += '/';
                    break;
                case 'b'
                :
                    strStringValue += '\b';
                    break;
                case 'n'
                :
                    strStringValue += '\n';
                    break;
                case 'r'
                :
                    strStringValue += '\r';
                    break;
                case 't'
                :
                    strStringValue += '\t';
                    break;
                case 'f'
                :
                    strStringValue += '\f';
                    break;
                case 'u'
                :
                    itrData += 4;
                    break;
                default
                :
                    strStringValue += szCurrentChar;
                    break;
            }

            fEscaped = false;
        }
        else
        {
            if ('\\' == szCurrentChar)
            {
                fEscaped = true;
            }
            else
            {
                strStringValue += szCurrentChar;
            }
        }

        ++itrData;
    }

    return strStringValue;
}

/********************************************************************************************
 *
 * @function PutJsonNumberToStructuredBuffer
 * @brief Add element to the structured buffer based on its type
 * @param[in] c_szRequireParameterName element name
 * @param[in] bElementType element type
 * @param[in] fl64ParameterValue element value
 * @param[in] poRequestStructuredBuffer pointer to StructuredBuffer containing parameters
 *
 ********************************************************************************************/

void PutJsonNumberToStructuredBuffer(
    _in const char * c_szRequireParameterName,
    _in Byte bElementType,
    _in float64_t fl64ParameterValue,
    _out StructuredBuffer * poRequestStructuredBuffer
    )
{
    __DebugFunction();

    switch (bElementType)
    {
        case FLOAT32_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutFloat32(c_szRequireParameterName, (float) fl64ParameterValue);
            break;
        case FLOAT64_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutFloat64(c_szRequireParameterName, (double) fl64ParameterValue);
            break;
        case INT8_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutInt8(c_szRequireParameterName, (int8_t) fl64ParameterValue);
            break;
        case INT16_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutInt16(c_szRequireParameterName, (int16_t) fl64ParameterValue);
            break;
        case INT32_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutInt32(c_szRequireParameterName, (int32_t) fl64ParameterValue);
            break;
        case INT64_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutInt64(c_szRequireParameterName, (int64_t) fl64ParameterValue);
            break;
        case UINT8_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutUnsignedInt8(c_szRequireParameterName, (uint8_t) fl64ParameterValue);
            break;
        case UINT16_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutUnsignedInt16(c_szRequireParameterName, (uint16_t) fl64ParameterValue);
            break;
        case UINT32_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutUnsignedInt32(c_szRequireParameterName, (uint32_t) fl64ParameterValue);
            break;
        case UINT64_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutUnsignedInt64(c_szRequireParameterName, (uint64_t) fl64ParameterValue);
            break;
        case BYTE_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutByte(c_szRequireParameterName, (Byte) fl64ParameterValue);
            break;
        case WORD_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutWord(c_szRequireParameterName, (Word) fl64ParameterValue);
            break;
        case DWORD_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutDword(c_szRequireParameterName, (Dword) fl64ParameterValue);
            break;
        case QWORD_VALUE_TYPE
        :
            poRequestStructuredBuffer->PutQword(c_szRequireParameterName, (Qword) fl64ParameterValue);
            break;
        default:
            break;
    }
}

/********************************************************************************************
 *
 * @function ValidateUnsignedNumber
 * @brief Check if the unsigned number is valid according to the specified range or not
 * @param[in] qwParameterValue element value
 * @param[in] c_strRange comma delimitted range
 * @param[in] bRangeType range type
 * @return true if valid
 * @return false otherwise
 *
 ********************************************************************************************/

bool ValidateUnsignedNumber(
    _in Qword qwParameterValue,
    _in const std::string & c_strRange,
    _in Byte bRangeType
    )
{
    __DebugFunction();

    bool fValid = true;

    std::vector<Qword> stlRange;
    std::stringstream oRangeStream(c_strRange);
    std::string strAllowedElement;
    while (getline(oRangeStream, strAllowedElement, ','))
    {
        stlRange.push_back(std::atof(strAllowedElement.c_str()));
    }
    if (ANY_VALUE_TYPE == bRangeType)
    {
        _ThrowBaseExceptionIf((2 > stlRange.size()), "ERROR: Invalid range specified.", nullptr);
        // Check if the number is in the range specified or not
        if ((stlRange[0] > qwParameterValue) || (stlRange[1] < qwParameterValue))
        {
            fValid = false;
        }
    }

    return fValid;
}

/********************************************************************************************
 *
 * @function ValidateSignedNumber
 * @brief Check if the signed number is valid according to the specified range or not
 * @param[in] fl64ParameterValue element value
 * @param[in] c_strRange comma delimitted range
 * @param[in] bRangeType range type
 * @return true if valid
 * @return false otherwise
 *
 ********************************************************************************************/

bool ValidateSignedNumber(
    _in float64_t fl64ParameterValue,
    _in const std::string & c_strRange,
    _in Byte bRangeType
    )
{
    __DebugFunction();

    bool fValid = true;

    std::vector<float64_t> stlRange;
    std::stringstream oRangeStream(c_strRange);
    std::string strAllowedElement;
    while (getline(oRangeStream, strAllowedElement, ','))
    {
        stlRange.push_back(std::atof(strAllowedElement.c_str()));
    }
    // Check if the number is allowed or not
    if (ANY_VALUE_TYPE == bRangeType)
    {
        _ThrowBaseExceptionIf((2 > stlRange.size()), "ERROR: Invalid range specified.", nullptr);
        // Check if the number is in the range specified or not
        if ((stlRange[0] > fl64ParameterValue) || (stlRange[1] < fl64ParameterValue))
        {
            fValid = false;
        }
    }

    return fValid;
}

/********************************************************************************************
 *
 * @function ReplaceAll
 * @brief Replace all the instances of c_strChangeThis to c_strChangeTo
 * @param[inout] strOriginalString Original string which needs to be modified
 * @param[in] c_strChangeThis Original string which needs to be replaced
 * @param[in] c_strChangeTo The string which is put at the replaced position
 *
 ********************************************************************************************/

void __thiscall ReplaceAll(
    _inout std::string & strOriginalString,
    _in const std::string & c_strChangeThis,
    _in const std::string & c_strChangeTo)
{
    size_t start_pos = 0;
    while((start_pos = strOriginalString.find(c_strChangeThis, start_pos)) != std::string::npos)
    {
        strOriginalString.replace(start_pos, c_strChangeThis.length(), c_strChangeTo);
        start_pos += c_strChangeTo.length();
    };
}
