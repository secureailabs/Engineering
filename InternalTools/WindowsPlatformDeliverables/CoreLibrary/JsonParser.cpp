 /*********************************************************************************************
 *
 * @file JsonParser.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Implementation of the Guid class that handles 128 bit (16 bytes) GUID/UUID values.
 *
 ********************************************************************************************/

#include "Base64Encoder.h"
#include "CoreTypes.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "Guid.h"
#include "StructuredBuffer.h"

#define STRING_QUOTE_BLOCK 1
#define CURLY_BRACE_BLOCK 2
#define ARRAY_BLOCK 3
#define TRUE_VALUE 4
#define FALSE_VALUE 5
#define NULL_TYPE 6
#define NUMBER_VALUE 7

// These are strings used to do easy character lookup while parsing. Helps simplify the
// code considerably
static const std::string gsc_strJsonWhitespaceCharacters = "\x09\x0a\x0d\x20";
static const std::string gsc_strJsonValidLeadingNumericalCharacters = "-0123456789";
static const std::string gsc_strJsonValiNumericalCharacters = "0123456789.-Ee";
static const std::string gsc_strJsonHexadecimalCharacters = "0123456789abcdefABCDEF";

// Forward declarations for ParseJsonObjectToStructuredBuffer. This is unfortunately required since
// ParseJsonArrayToStructuredBuffer() needs to recurse into ParseJsonObjectToStructuredBuffer() and it ends
// up being implemented beforehand. If it was the other way around, we'd have to do a forward declarations
// for ParseJsonArrayToStructuredBuffer() instead
static StructuredBuffer __stdcall ParseJsonObjectToStructuredBuffer(
    _in const char * c_szJsonString,
    _inout unsigned int * punOffset
    );

/// <summary>
/// This is used to decode embedded /uxxxx string elements into a corresponding printable ANSI character
/// </summary>
/// <param name="c_szJsonString"></param>
/// <param name="punOffset"></param>
/// <returns></returns>
static char __stdcall ConvertJsonHexCharactersToAnsiCharacter(
    _in const char * c_szJsonString,
    _inout unsigned int * punOffset
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szJsonString);
    __DebugAssert(nullptr != punOffset);

    unsigned int unCurrentOffset = *punOffset;
    char chFirstCharacter = c_szJsonString[unCurrentOffset++];
    char chSecondCharacter = c_szJsonString[unCurrentOffset++];
    char chThirdCharacter = c_szJsonString[unCurrentOffset++];
    char chFourthCharacter = c_szJsonString[unCurrentOffset++];

    // Quick reality check to make sure that we have correct characters
    _ThrowBaseExceptionIf((std::string::npos == gsc_strJsonHexadecimalCharacters.find(chFirstCharacter)), "Invalid hexadecimal character found in JSON string at offset %d", unCurrentOffset);
    _ThrowBaseExceptionIf((std::string::npos == gsc_strJsonHexadecimalCharacters.find(chSecondCharacter)), "Invalid hexadecimal character found in JSON string at offset %d", unCurrentOffset);
    _ThrowBaseExceptionIf((std::string::npos == gsc_strJsonHexadecimalCharacters.find(chThirdCharacter)), "Invalid hexadecimal character found in JSON string at offset %d", unCurrentOffset);
    _ThrowBaseExceptionIf((std::string::npos == gsc_strJsonHexadecimalCharacters.find(chFourthCharacter)), "Invalid hexadecimal character found in JSON string at offset %d", unCurrentOffset);

    // TODO: For now we cheat and only take the LSB in the unicode character, which should work 99.9% of the time
    chThirdCharacter = (chThirdCharacter <= '9') ? (chThirdCharacter - '0') : ((chThirdCharacter & 0x7) + 9);
    chFourthCharacter = (chFourthCharacter <= '9') ? (chFourthCharacter - '0') : ((chFourthCharacter & 0x7) + 9);

    // Make sure to update punOffset
    *punOffset = unCurrentOffset;

    return (char) ((chThirdCharacter << 4) | chFourthCharacter);
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szJsonString"></param>
/// <param name="punOffset"></param>
/// <returns></returns>
static float64_t __stdcall ParseJsonNumber(
    _in const char * c_szJsonString,
    _inout unsigned int * punOffset
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szJsonString);
    __DebugAssert(nullptr != punOffset);

    unsigned int unStartingOffset = *punOffset;
    unsigned int unNumberSizeInBytes = 0;
    
    // The first thing we need to do is figure out the ending offset, this way we know how much
    // to increase punOffset once we are done
    while (std::string::npos != gsc_strJsonValiNumericalCharacters.find(c_szJsonString[unStartingOffset + unNumberSizeInBytes]))
    {
        unNumberSizeInBytes++;
    }
    float64_t fl64JsonNumber;
    _ThrowBaseExceptionIf((1 != ::sscanf_s(&(c_szJsonString[unStartingOffset]), "%lf", &fl64JsonNumber)), "Invalid JSON number encountered at offset %d", unStartingOffset);
    *punOffset = unStartingOffset + unNumberSizeInBytes;

    return fl64JsonNumber;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szJsonString"></param>
/// <returns></returns>
static std::string __stdcall ParseJsonString(
    _in const char * c_szJsonString,
    _inout unsigned int * punOffset
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szJsonString);
    __DebugAssert(nullptr != punOffset);

    bool fDone = false;
    unsigned int unCurrentOffset = *punOffset;
    unsigned int unActualStringSize = 0;
    std::string strReturnString;

    do
    {
        // For optimization reasons, we want to grow the string in increments of
        // 1000, or else this could get really expensive to
        if (0 == (strReturnString.size() % 1000))
        {
            strReturnString.resize(strReturnString.size() + 1000);
        }
        // First make sure we didn't encounter any invalid characters in the string
        _ThrowBaseExceptionIf((('\x00' <= c_szJsonString[unCurrentOffset])&&('\x1F' >= c_szJsonString[unCurrentOffset])), "Invalid string character found at offset %d", unCurrentOffset);
        // Now let's see if we are trying to escape a character
        if ('\\' == c_szJsonString[unCurrentOffset])
        {
            ++unCurrentOffset;
            if ('\\' == c_szJsonString[unCurrentOffset])
            {
                strReturnString.push_back('\\');
                ++unCurrentOffset;
            }
            else if ('/' == c_szJsonString[unCurrentOffset])
            {
                strReturnString.push_back('/');
                ++unCurrentOffset;
            }
            else if ('b' == c_szJsonString[unCurrentOffset])
            {
                strReturnString.push_back('\b');
                ++unCurrentOffset;
            }
            else if ('f' == c_szJsonString[unCurrentOffset])
            {
                strReturnString.push_back('\f');
                ++unCurrentOffset;
            }
            else if ('n' == c_szJsonString[unCurrentOffset])
            {
                strReturnString.push_back('\n');
                ++unCurrentOffset;
            }
            else if ('r' == c_szJsonString[unCurrentOffset])
            {
                strReturnString.push_back('\r');
                ++unCurrentOffset;
            }
            else if ('t' == c_szJsonString[unCurrentOffset])
            {
                strReturnString.push_back('\t');
                ++unCurrentOffset;
            }
            else if ('u' == c_szJsonString[unCurrentOffset])
            {
                ++unCurrentOffset;
                strReturnString.push_back(::ConvertJsonHexCharactersToAnsiCharacter(c_szJsonString, &unCurrentOffset));
            }
            else
            {
                _ThrowBaseException("Invalid character found in JSON string at offset %d", unCurrentOffset);
            }
        }
        else if ('"' == c_szJsonString[unCurrentOffset])
        {
            ++unCurrentOffset;
            fDone = true;
        }
        else
        {
            strReturnString[unActualStringSize] = c_szJsonString[unCurrentOffset];
            ++unActualStringSize;
            ++unCurrentOffset;
        }
    }
    while (false == fDone);

    // Make sure to update punOffset
    *punOffset = unCurrentOffset;

    return strReturnString;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szJsonString"></param>
/// <returns></returns>
static StructuredBuffer __stdcall ParseJsonArrayToStructuredBuffer(
    _in const char * c_szJsonString,
    _inout unsigned int * punOffset
    )
{
    __DebugFunction();
    
    bool fDone = false;
    unsigned int unCurrentOffset = *punOffset;
    StructuredBuffer oJsonObject;
    unsigned int unArrayIndex = 0;
    char szValueName[10];

    // First, skip over any and all white spaces as soon as we enter into the array block.
    // It's also possible that we end up with an empty array block if the first character
    // encountered is a ']'
    while (std::string::npos != gsc_strJsonWhitespaceCharacters.find(c_szJsonString[unCurrentOffset]))
    {
        ++unCurrentOffset;
    }

    // Check to make sure that this isn't an empty block
    if (']' == c_szJsonString[unCurrentOffset])
    {
        fDone = true;
        ++unCurrentOffset;
        oJsonObject.PutBoolean("__IsEmpty__", true);
    }

    // Only loop if this isn't an empty block
    while (false == fDone)
    {
        // First thing we do is, create the array index string
        ::sprintf_s(szValueName, sizeof(szValueName), "%d", unArrayIndex);
        // Arrays are made up of comma delimited values. So the first thing we look for is a value. There are different
        // ways to find a value, based on the conditions below.
        unsigned int unCode = 0;
        do
        {
            if ('"' == c_szJsonString[unCurrentOffset])
            {
                unCode = STRING_QUOTE_BLOCK;
            }
            else if ('{' == c_szJsonString[unCurrentOffset])
            {
                unCode = CURLY_BRACE_BLOCK;
            }
            else if ('[' == c_szJsonString[unCurrentOffset])
            {
                unCode = ARRAY_BLOCK;
            }
            else if (('t' == c_szJsonString[unCurrentOffset])||('T' == c_szJsonString[unCurrentOffset]))
            {
                unCode = TRUE_VALUE;
            }
            else if (('f' == c_szJsonString[unCurrentOffset])||('F' == c_szJsonString[unCurrentOffset]))
            {
                unCode = FALSE_VALUE;
            }
            else if (('n' == c_szJsonString[unCurrentOffset])||('N' == c_szJsonString[unCurrentOffset]))
            {
                unCode = NULL_TYPE;
            }
            else if (std::string::npos != gsc_strJsonValidLeadingNumericalCharacters.find(c_szJsonString[unCurrentOffset]))
            {
                unCode = NUMBER_VALUE;
            }
            else 
            {
                // Check to make sure that the current character is a blank, which means
                // a whitespace, a tab, a linefeed or a carriage return. Otherwise, the JSON
                // is invalid
                _ThrowBaseExceptionIf((std::string::npos == gsc_strJsonWhitespaceCharacters.find(c_szJsonString[unCurrentOffset])), "Invalid JSON string. Invalid character found at offset %d", unCurrentOffset);
                ++unCurrentOffset;
            }
        }
        while (0 == unCode);
        // Based on the code above, let's parse things accordingly
        if (STRING_QUOTE_BLOCK == unCode)
        {
            ++unCurrentOffset;
            std::string strJsonValue = ::ParseJsonString(c_szJsonString, &unCurrentOffset);
            // TODO: Insert strong typing here
            oJsonObject.PutString(szValueName, strJsonValue);
        }
        else if (CURLY_BRACE_BLOCK == unCode)
        {
            ++unCurrentOffset;
            StructuredBuffer oNestedJsonObject(::ParseJsonObjectToStructuredBuffer(c_szJsonString, &unCurrentOffset));
            oJsonObject.PutStructuredBuffer(szValueName, oNestedJsonObject);
        }
        else if (ARRAY_BLOCK == unCode)
        {
            ++unCurrentOffset;
            StructuredBuffer oNestedJsonObject(::ParseJsonArrayToStructuredBuffer(c_szJsonString, &unCurrentOffset));
            oJsonObject.PutStructuredBuffer(szValueName, oNestedJsonObject);
        }
        else if (TRUE_VALUE == unCode)
        {
            unsigned int unExpectedLength = (unsigned int) ::strlen("true");
            _ThrowBaseExceptionIf((0 != ::_strnicmp("true", &(c_szJsonString[unCurrentOffset]), unExpectedLength)), "Invalid JSON string. 'true' token not found at offset %d", unCurrentOffset);
            unCurrentOffset += unExpectedLength;
            oJsonObject.PutBoolean(szValueName, true);
        }
        else if (FALSE_VALUE == unCode)
        {
            unsigned int unExpectedLength = (unsigned int) ::strlen("false");
            _ThrowBaseExceptionIf((0 != ::_strnicmp("false", &(c_szJsonString[unCurrentOffset]), unExpectedLength)), "Invalid JSON string. 'true' token not found at offset %d", unCurrentOffset);
            unCurrentOffset += unExpectedLength;
            oJsonObject.PutBoolean(szValueName, false);
        }
        else if (NULL_TYPE == unCode)
        {
            unsigned int unExpectedLength = (unsigned int) ::strlen("null");
            _ThrowBaseExceptionIf((0 != ::_strnicmp("null", &(c_szJsonString[unCurrentOffset]), unExpectedLength)), "Invalid JSON string. 'true' token not found at offset %d", unCurrentOffset);
            unCurrentOffset += unExpectedLength;
            oJsonObject.PutNull(szValueName);
        }
        else if (NUMBER_VALUE == unCode)
        {
            oJsonObject.PutFloat64(szValueName, ::ParseJsonNumber(c_szJsonString, &unCurrentOffset));
        }
        // Now that we are done parsing the JSON value, whatever that may be, there are two possibilities. Either we find
        // the character ',', or we find the character ']', along with some white spaces.
        while ((',' != c_szJsonString[unCurrentOffset])&&(']' != c_szJsonString[unCurrentOffset]))
        {
            // Check to make sure that the current character is a blank, which means
            // a whitespace, a tab, a linefeed or a carriage return. Otherwise, the JSON
            // is invalid
            _ThrowBaseExceptionIf((std::string::npos == gsc_strJsonWhitespaceCharacters.find(c_szJsonString[unCurrentOffset])), "Invalid JSON string. Invalid character found at offset %d", unCurrentOffset);
            // Keep on moving on
            ++unCurrentOffset;
        }
        // There are only two ways to end up here. Either we encountered a '}' or a ','
        if (']' == c_szJsonString[unCurrentOffset])
        {
            fDone = true;
        }
        ++unCurrentOffset;
        ++unArrayIndex;
    }
    
    // Update the punOffset parameter
    *punOffset = unCurrentOffset;
    // Make sure that the StructuredBuffer is marked as an array
    oJsonObject.PutBoolean("__IsArray__", true);

    return oJsonObject;
}

/// <summary>
/// Parses a JSON object. The offset that is passed in should point at the first character which follows the '{'
/// The standard for the JSON object parsing can be found at https://www.json.org/img/object.png
/// </summary>
/// <param name="c_szJsonString"></param>
/// <returns></returns>
static StructuredBuffer __stdcall ParseJsonObjectToStructuredBuffer(
    _in const char * c_szJsonString,
    _inout unsigned int * punOffset
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szJsonString);
    __DebugAssert(nullptr != punOffset);

    bool fDone = false;
    unsigned int unCurrentOffset = *punOffset;
    StructuredBuffer oJsonObject;

    do
    {
        // First, skip over any and all white spaces as soon as we enter into the block.
        // White spaces are always ignored
        while (std::string::npos != gsc_strJsonWhitespaceCharacters.find(c_szJsonString[unCurrentOffset]))
        {
            ++unCurrentOffset;
        }

        // Once all of the white spaces have been skipped, there are only two valid values
        // that we can encounter. The '"' character marking the beginning of a value name or,
        // the '}' character, marking the end of the block (i.e. we have an empty block)
        if ('}' == c_szJsonString[unCurrentOffset])
        {
            fDone = true;
            // Make sure that the StructuredBuffer is marked as an array
            oJsonObject.PutBoolean("__IsEmpty__", true);
        }
        else if ('"' != c_szJsonString[unCurrentOffset])
        {
            _ThrowBaseException("Invalid JSON string. Invalid character found at offset %d, was expecting a '\"'", unCurrentOffset);
        }
        // No matter if we encounter '}' or '"', advance the offset by one
        ++unCurrentOffset;

        // If we are not dealing with an empty group
        if (false == fDone)
        {
            // If we get here, then we are at the offset of the first character in the JSON name string value
            std::string strJsonNameString = ::ParseJsonString(c_szJsonString, &unCurrentOffset);
            _ThrowBaseExceptionIf((0 == strJsonNameString.size()), "Invalid JSON value name encountered at offset %d", unCurrentOffset);
            // Once we get a JSON value name by parsing a string, we need to look for the ':' character, which
            // is required, we look for the first '"' which starts the JsonNameString token
            while (':' != c_szJsonString[unCurrentOffset])
            {
                // Check to make sure that the current character is a blank, which means
                // a whitespace, a tab, a linefeed or a carriage return. Otherwise, the JSON
                // is invalid
                _ThrowBaseExceptionIf((std::string::npos == gsc_strJsonWhitespaceCharacters.find(c_szJsonString[unCurrentOffset])), "Invalid JSON string. Invalid character found at offset %d", unCurrentOffset);
                // Keep on moving on
                ++unCurrentOffset;
            }
            ++unCurrentOffset;
            // If we get here, then we are at the offset of the first character that follows the ':' separator. At this point,
            // there are several possibilities. We can find a '{' character, a '[' character, a '"' character,
            // a numerical character, the letter 't', the letter 'f', or the letter 'n'. We can also find whitespaces. Anything
            // else is a JSON encoding error
            unsigned int unCode = 0;
            do
            {
                if ('"' == c_szJsonString[unCurrentOffset])
                {
                    unCode = STRING_QUOTE_BLOCK;
                }
                else if ('{' == c_szJsonString[unCurrentOffset])
                {
                    unCode = CURLY_BRACE_BLOCK;
                }
                else if ('[' == c_szJsonString[unCurrentOffset])
                {
                    unCode = ARRAY_BLOCK;
                }
                else if (('t' == c_szJsonString[unCurrentOffset])||('T' == c_szJsonString[unCurrentOffset]))
                {
                    unCode = TRUE_VALUE;
                }
                else if (('f' == c_szJsonString[unCurrentOffset])||('F' == c_szJsonString[unCurrentOffset]))
                {
                    unCode = FALSE_VALUE;
                }
                else if (('n' == c_szJsonString[unCurrentOffset])||('N' == c_szJsonString[unCurrentOffset]))
                {
                    unCode = NULL_TYPE;
                }
                else if (std::string::npos != gsc_strJsonValidLeadingNumericalCharacters.find(c_szJsonString[unCurrentOffset]))
                {
                    unCode = NUMBER_VALUE;
                }
                else 
                {
                    // Check to make sure that the current character is a blank, which means
                    // a whitespace, a tab, a linefeed or a carriage return. Otherwise, the JSON
                    // is invalid
                    _ThrowBaseExceptionIf((std::string::npos == gsc_strJsonWhitespaceCharacters.find(c_szJsonString[unCurrentOffset])), "Invalid JSON string. Invalid character found at offset %d", unCurrentOffset);
                    ++unCurrentOffset;
                }
            }
            while (0 == unCode);
            // Based on the code above, let's parse things accordingly
            if (STRING_QUOTE_BLOCK == unCode)
            {
                ++unCurrentOffset;
                std::string strJsonValue = ::ParseJsonString(c_szJsonString, &unCurrentOffset);
                oJsonObject.PutString(strJsonNameString.c_str(), strJsonValue);
            }
            else if (CURLY_BRACE_BLOCK == unCode)
            {
                ++unCurrentOffset;
                StructuredBuffer oNestedJsonObject(::ParseJsonObjectToStructuredBuffer(c_szJsonString, &unCurrentOffset));
                oJsonObject.PutStructuredBuffer(strJsonNameString.c_str(), oNestedJsonObject);
            }
            else if (ARRAY_BLOCK == unCode)
            {
                ++unCurrentOffset;
                StructuredBuffer oNestedJsonObject(::ParseJsonArrayToStructuredBuffer(c_szJsonString, &unCurrentOffset));
                oJsonObject.PutStructuredBuffer(strJsonNameString.c_str(), oNestedJsonObject);
            }
            else if (TRUE_VALUE == unCode)
            {
                unsigned int unExpectedLength = (unsigned int) ::strlen("true");
                _ThrowBaseExceptionIf((0 != ::_strnicmp("true", &(c_szJsonString[unCurrentOffset]), unExpectedLength)), "Invalid JSON string. 'true' token not found at offset %d", unCurrentOffset);
                unCurrentOffset += unExpectedLength;
                oJsonObject.PutBoolean(strJsonNameString.c_str(), true);
            }
            else if (FALSE_VALUE == unCode)
            {
                unsigned int unExpectedLength = (unsigned int) ::strlen("false");
                _ThrowBaseExceptionIf((0 != ::_strnicmp("false", &(c_szJsonString[unCurrentOffset]), unExpectedLength)), "Invalid JSON string. 'true' token not found at offset %d", unCurrentOffset);
                unCurrentOffset += unExpectedLength;
                oJsonObject.PutBoolean(strJsonNameString.c_str(), false);
            }
            else if (NULL_TYPE == unCode)
            {
                unsigned int unExpectedLength = (unsigned int) ::strlen("null");
                _ThrowBaseExceptionIf((0 != ::_strnicmp("null", &(c_szJsonString[unCurrentOffset]), unExpectedLength)), "Invalid JSON string. 'true' token not found at offset %d", unCurrentOffset);
                unCurrentOffset += unExpectedLength;
                oJsonObject.PutNull(strJsonNameString.c_str());
            }
            else if (NUMBER_VALUE == unCode)
            {
                oJsonObject.PutFloat64(strJsonNameString.c_str(), ::ParseJsonNumber(c_szJsonString, &unCurrentOffset));
            }
            // Now that we are done parsing the JSON value, whatever that may be, there are two possibilities. Either we find
            // the character ',', or we find the character '}', along with some white spaces.
            while ((',' != c_szJsonString[unCurrentOffset])&&('}' != c_szJsonString[unCurrentOffset]))
            {
                // Check to make sure that the current character is a blank, which means
                // a whitespace, a tab, a linefeed or a carriage return. Otherwise, the JSON
                // is invalid
                _ThrowBaseExceptionIf((std::string::npos == gsc_strJsonWhitespaceCharacters.find(c_szJsonString[unCurrentOffset])), "Invalid JSON string. Invalid character found at offset %d", unCurrentOffset);
                // Keep on moving on
                ++unCurrentOffset;
            }
            // There are only two ways to end up here. Either we encountered a '}' or a ','
            if ('}' == c_szJsonString[unCurrentOffset])
            {
                fDone = true;
            }
            // No matter if we encounter a '}' or a ',', we increment by one
            ++unCurrentOffset;
        }
    }
    while (false == fDone);
    
    *punOffset = unCurrentOffset;

    return oJsonObject;
}

/// <summary>
/// Function which converts a JSON string into a StructuredBuffer
/// </summary>
/// <param name="c_szJsonString"></param>
/// <returns></returns>
StructuredBuffer __stdcall ConvertJsonStringToStructuredBuffer(
    _in const char * c_szJsonString
    )
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szJsonString);

    unsigned int unCurrentOffset = 0;

    // We look for the first '{' which starts the ball rolling. It's possible to have leading
	// white spaces which we need to skip
    while ('{' != c_szJsonString[unCurrentOffset])
    {
        // Check to make sure that the current character is a blank, which means
        // a whitespace, a tab, a linefeed or a carriage return. Otherwise, the JSON
        // is invalid
        _ThrowBaseExceptionIf((std::string::npos == gsc_strJsonWhitespaceCharacters.find(c_szJsonString[unCurrentOffset])), "Invalid JSON string. Invalid character found at offset %d", unCurrentOffset);
        // Keep on moving on
        ++unCurrentOffset;
    }
    ++unCurrentOffset;

    // There can only be one root object in JSON, so whatever that object is, that
    // is what we return to the caller.
    return ::ParseJsonObjectToStructuredBuffer(c_szJsonString, &unCurrentOffset);
}

/// <summary>
/// 
/// </summary>
/// <param name="c_oStructuredBuffer"></param>
/// <param name="strJsonString"></param>
/// <returns></returns>
static void __stdcall ConvertStructuredBufferToStandardJson(
    _in const StructuredBuffer & c_oStructuredBuffer,
    _out std::string & strJsonString,
    _in unsigned int unIndentationLevel
    )
{
    __DebugFunction();

	// There is a very specific use case with StructuredBuffers, whereas if a StructuredBuffer has the elementName
	// "(boolean) __IsArray__" in it, then the StructuredBuffer contents are coded as a JSON array
    bool fIsArray = c_oStructuredBuffer.IsElementPresent("__IsArray__", BOOLEAN_VALUE_TYPE);
	// Get the list of elements in the current StructuredBuffer
    std::vector<std::string> stlListOfElements = c_oStructuredBuffer.GetNamesOfElements();
	// Figure out what the indentation header is. This helps us produce nice looking JSON output
    std::string strIndentationHeader((unIndentationLevel * 4), ' ');
	// We need to track the number of elements processed since this help us figure out when
	// to put a comma (',') at the end of a value. In our case, we actually print one value and,
	// if we loop around and there is another value to output, we first output the comma (',') and then
	// we print out the value
    unsigned int unNumberOfElementsProcessed = 0;

    // Iterate through each of the elements
    for (const std::string & c_strElementName: stlListOfElements)
    {
        // Never process this reserved element name, so we skip it if we encounter it.
        if ("__IsArray__" != c_strElementName)
        {
			// If we are printing out an array, then the elements of the array do not
			// get a <ElementName>: <ElementValue> format, all they get is <ElementValue>
            std::string strElementName = (true == fIsArray) ? "" : ("\"" + c_strElementName + "\": ");
            // If this is not the first time we iterate through this loop (i.e. not the
			// first element), then before we print out a new element, we need to print
			// out a comma (',')
            if (0 < unNumberOfElementsProcessed)
            {
                strJsonString += ",\r\n";
            }
            // Is the current element a nested structure. There are two types, one which
			// nests using { ... } and the other is an array which nests with [ ... ]
            Byte bElementType = c_oStructuredBuffer.GetElementType(c_strElementName.c_str());
            if (INDEXED_BUFFER_VALUE_TYPE == bElementType)
            {
                StructuredBuffer oNestedStructuredBuffer = c_oStructuredBuffer.GetStructuredBuffer(c_strElementName.c_str());

                if (true == oNestedStructuredBuffer.IsElementPresent("__IsArray__", BOOLEAN_VALUE_TYPE))
                {
                    strJsonString += strIndentationHeader + strElementName + "[\r\n";
					// Resurse into this function
                    ::ConvertStructuredBufferToStandardJson(oNestedStructuredBuffer, strJsonString, (unIndentationLevel + 1));
                    strJsonString += "\r\n" + strIndentationHeader + "]";
                }
                else
                {
                    strJsonString += strIndentationHeader + strElementName + "{\r\n";
					// Resurse into this function
                    ::ConvertStructuredBufferToStandardJson(oNestedStructuredBuffer, strJsonString, (unIndentationLevel + 1));
                    strJsonString += "\r\n" + strIndentationHeader + "}";
                }
            }
            else if (NULL_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + "null";
            }
            else if (BOOLEAN_VALUE_TYPE == bElementType)
            {
                if (true == c_oStructuredBuffer.GetBoolean(c_strElementName.c_str()))
                {
                    strJsonString += strIndentationHeader + strElementName + "true";
                }
                else
                {
                    strJsonString += strIndentationHeader + strElementName + "false";
                }
            }
            else if (ANSI_CHARACTER_VALUE_TYPE == bElementType)
            {
                char chValue = c_oStructuredBuffer.GetCharacter(c_strElementName.c_str());
                strJsonString += strIndentationHeader + strElementName + "\"" + chValue + "\"";
            }
            else if (ANSI_CHARACTER_STRING_VALUE_TYPE == bElementType)
            {
                std::string strValue = c_oStructuredBuffer.GetString(c_strElementName.c_str());
                std::string strEscapedValue;
                unsigned int unInsertedCharacterCount = 0;
                // To be optimal, we pre-allocate the escaped string. At worse, it will be
                // precisely twice as big as the original
                strEscapedValue.resize(strValue.size() * 2);
                // Now let's create the escaped string
                for (unsigned unIndex = 0; unIndex < strValue.size(); ++unIndex)
                {
                    char chCurrentCharacter = strValue[unIndex];
                    _ThrowBaseExceptionIf((('\x00' <= chCurrentCharacter)&&('\x1F' >= chCurrentCharacter)), "Invalid string character 0x%02X found at offset %d", (unsigned int) chCurrentCharacter, unIndex);

                    if ('\\' == chCurrentCharacter)
                    {
                        strEscapedValue[unInsertedCharacterCount++] = '\\';
                        strEscapedValue[unInsertedCharacterCount++] = '\\';
                    }
                    else if ('\b' == chCurrentCharacter)
                    {
                        strEscapedValue[unInsertedCharacterCount++] = '\\';
                        strEscapedValue[unInsertedCharacterCount++] = 'b';
                    }
                    else if ('\f' == chCurrentCharacter)
                    {
                        strEscapedValue[unInsertedCharacterCount++] = '\\';
                        strEscapedValue[unInsertedCharacterCount++] = 'f';
                    }
                    else if ('\n' == chCurrentCharacter)
                    {
                        strEscapedValue[unInsertedCharacterCount++] = '\\';
                        strEscapedValue[unInsertedCharacterCount++] = 'n';
                    }
                    else if ('\r' == chCurrentCharacter)
                    {
                        strEscapedValue[unInsertedCharacterCount++] = '\\';
                        strEscapedValue[unInsertedCharacterCount++] = 'r';
                    }
                    else if ('\t' == chCurrentCharacter)
                    {
                        strEscapedValue[unInsertedCharacterCount++] = '\\';
                        strEscapedValue[unInsertedCharacterCount++] = 't';
                    }
                    else
                    {
                        strEscapedValue[unInsertedCharacterCount++] = chCurrentCharacter;
                    }
                }
                strEscapedValue.resize(unInsertedCharacterCount);

                strJsonString += strIndentationHeader + strElementName + "\"" + strEscapedValue + "\"";
            }
            else if (FLOAT32_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetFloat32(c_strElementName.c_str()));
            }
            else if (FLOAT64_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetFloat64(c_strElementName.c_str()));
            }
            else if (INT8_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetInt8(c_strElementName.c_str()));
            }
            else if (INT16_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetInt16(c_strElementName.c_str()));
            }
            else if (INT32_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetInt32(c_strElementName.c_str()));
            }
            else if (INT64_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetInt64(c_strElementName.c_str()));
            }
            else if (UINT8_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetUnsignedInt8(c_strElementName.c_str()));
            }
            else if (UINT16_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetUnsignedInt16(c_strElementName.c_str()));
            }
            else if (UINT32_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetUnsignedInt32(c_strElementName.c_str()));
            }
            else if (UINT64_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetUnsignedInt64(c_strElementName.c_str()));
            }
            else if (BYTE_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetByte(c_strElementName.c_str()));
            }
            else if (WORD_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetWord(c_strElementName.c_str()));
            }
            else if (DWORD_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetDword(c_strElementName.c_str()));
            }
            else if (QWORD_VALUE_TYPE == bElementType)
            {
                strJsonString += strIndentationHeader + strElementName + std::to_string(c_oStructuredBuffer.GetQword(c_strElementName.c_str()));
            }
            else if (BUFFER_VALUE_TYPE == bElementType)
            {
				// Buffer are coded as Base64 strings
                std::vector<Byte> stlBuffer = c_oStructuredBuffer.GetBuffer(c_strElementName.c_str());
                std::string strBase64Buffer = ::Base64Encode(stlBuffer.data(), (unsigned int) stlBuffer.size());
                strJsonString += strIndentationHeader + strElementName + "\"" + strBase64Buffer + "\"";
            }
            else if (GUID_VALUE_TYPE == bElementType)
            {
                std::string strIdentifier = c_oStructuredBuffer.GetGuid(c_strElementName.c_str()).ToString(eHyphensOnly);
                strJsonString += strIndentationHeader + strElementName + "\"" + strIdentifier + "\"";
            }

            unNumberOfElementsProcessed++;
        }
    }
}

/// <summary>
/// This function converts a StructuredBuffer into a Json string
/// </summary>
/// <param name="c_oStructuredBuffer"></param>
/// <returns></returns>
std::string __stdcall ConvertStructuredBufferToJson(
    _in const StructuredBuffer & c_oStructuredBuffer
    )
{
    __DebugFunction();

    std::string strJsonString = "{\r\n";
    ::ConvertStructuredBufferToStandardJson(c_oStructuredBuffer, strJsonString, 1);
    strJsonString.push_back('\r');
    strJsonString.push_back('\n');
    strJsonString.push_back('}');

    return strJsonString;
}