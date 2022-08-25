/*********************************************************************************************
 *
 * @file Guid.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Implementation of the Guid class that handles 128 bit (16 bytes) GUID/UUID values.
 *
 ********************************************************************************************/

#include "CoreTypes.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "Guid.h"

#include <stdio.h>
#include <string.h>
#include <uuid/uuid.h>

#include <algorithm>
#include <iostream>

#pragma pack(push, 1)
typedef struct _GUID
{
    uint32_t Data1;
    uint16_t Data2;
    uint16_t Data3;
    uint8_t  Data4[8];
}
GUID;
#pragma pack(pop)

/********************************************************************************************
 *
 * @class Guid
 * @function Guid
 * @brief Default constructor
 * @throw bad_alloc If there isn't enough memory left to allocate the internal GUID buffer
 * @note
 *    All new Guid objects automatically get a new GUID generated on instantiation.
 *
 ********************************************************************************************/

Guid::Guid(void)
{
    __DebugFunction();

    uuid_t oUniqueIdentifier;
    uuid_generate(oUniqueIdentifier);
    m_stlRawData.resize(16);
    ::memcpy((void *) m_stlRawData.data(), (void *) &oUniqueIdentifier, 16);
    // The endianness of the UUID in Linux is not compatible with RFC 4122, section 4.1.2
    // Most of the bits are random, but we need to switch out bytes at ince 6 and 7
    Byte bByteSeven = m_stlRawData[7];
    m_stlRawData[7] = m_stlRawData[6];
    m_stlRawData[6] = bByteSeven;
}

/********************************************************************************************
 *
 * @class Guid
 * @function Guid
 * @brief Constructor which takes input from a incoming byte representing an object type and replaces
 * 4 MSBs with it
 * @param[in] bObjectType Byte representation of an object type
 * @throw bad_alloc If there isn't enough memory left to allocate the internal GUID/UUID buffer
 * @par
 *		eUndefined = 0x00,
 *		eOrganization = 0x04,
 *		eGroup = 0x08,
 *		eUser = 0x0C,
 *		eCryptographicKey = 0x10,
 *		eDigitalContract = 0x14,
 *		eDataFederation = 0x18,
 *		eDataset = 0x1C,
 *		eDatasetVersion = 0x20,
 *		eTable = 0x24,
 *		eColumn = 0x28,
 *		eAzureTemplate = 0x2C,
 *		ePlatformServicesVirtualMachine = 0x30,
 *		eDataServicesVirtualMachine = 0x34,
 *		eWebUiVirtualMachine = 0x38,
 *		eRemoteDataConnectorVirtualMachine = 0x3C,
 *		eSecureComputationalVirtualMachine = 0x40,
 *		eSafeFunction = 0x44,
 *		eJobIdentifier = 0x48,
 *		eInputParameterIdentifier = 0x4C,
 *		eOutputParameterIdentifier = 0x50,
 *		eUserSuppliedData = 0x54,
 *		eOrchestratorIdentifier = 0x58,
 *		eAuditEvent_RootNode = 0x5C,
 *		eAuditEvent_DigitalContractBranchNode = 0x60,
 *		eAuditEvent_VirtualMachineBranchNode = 0x64,
 *		eAuditEvent_EncryptedLeafNode = 0x68,
 *		eAuditEvent_PlainTextLeafNode = 0x6C,
 *		eGuidTypeBitMask = 0xFC
 *		
 ********************************************************************************************/

Guid::Guid(
    _in GuidObjectType eObjectType
    )
{
    __DebugFunction();

    uuid_t oUniqueIdentifier;
    ::uuid_generate(oUniqueIdentifier);
    m_stlRawData.resize(16);
    ::memcpy((void *) m_stlRawData.data(), (void *) &oUniqueIdentifier, 16);
    // The endianness of the UUID in Linux is not compatible with RFC 4122, section 4.1.2
    // Most of the bits are random, but we need to switch out bytes at ince 6 and 7
    Byte bByteSeven = m_stlRawData[7];
    m_stlRawData[7] = m_stlRawData[6];
    m_stlRawData[6] = bByteSeven;
    // Change Most significant 6 bits to eObjectType
    m_stlRawData[0] = (m_stlRawData[0] & eNegativeGuidTypeMask) | eObjectType;
}

/********************************************************************************************
 *
 * @class Guid
 * @function Guid
 * @brief Constructor which takes input from a incoming string representation of a GUID/UUID
 * @param[in] c_szGuid String representation of a GUID/UUID
 * @throw BaseException Invalid or improperly formatted @p c_szGuid parameter value
 * @throw bad_alloc If there isn't enough memory left to allocate the internal GUID/UUID buffer
 * @note
 *    This constructor will parse the incoming string and initialize itself to that value.
 * @par
 *    The Guid() constructor accepts three kinds of string formats for guid:
 *    (1) {6E574DA3-0688-43FD-9690-B5E15DE11402} --> hyphens and braces
 *    (2) 6E574DA3-0688-43FD-9690-B5E15DE11402 ----> hyphens
 *    (3) 6E574DA3068843FD9690B5E15DE11402 --------> raw
 *    Any other format will cause the constructor to throw an exception
 *
 ********************************************************************************************/

Guid::Guid(
    _in const char * c_szGuid
    )
{
    __DebugFunction();

    this->InitializeFromString(c_szGuid);
}

/********************************************************************************************
 *
 * @class Guid
 * @function Guid
 * @brief Constructor which takes input from a incoming string representation of a GUID/UUID
 * @param[in] c_strGuid std::string representation of a GUID/UUID
 * @throw BaseException Invalid or improperly formatted @p c_strGuid parameter value
 * @throw bad_alloc If there isn't enough memory left to allocate the internal GUID/UUID buffer
 * @note
 *    This constructor will parse the incoming string and initialize itself to that value.
 * @par
 *    The Guid() constructor accepts three kinds of string formats for guid:
 *    (1) {6E574DA3-0688-43FD-9690-B5E15DE11402} --> hyphens and braces
 *    (2) 6E574DA3-0688-43FD-9690-B5E15DE11402 ----> hyphens
 *    (3) 6E574DA3068843FD9690B5E15DE11402 --------> raw
 *    Any other format will cause the constructor to throw an exception
 *
 ********************************************************************************************/
Guid::Guid(
    _in const std::string & c_strGuid
    )
{
    __DebugFunction();

    this->InitializeFromString(c_strGuid.c_str());
}

/********************************************************************************************
 *
 * @class Guid
 * @function Guid
 * @brief Constructor which takes input from a incoming 16 byte buffer containing a raw GUID/UUID
 * @param[in] c_pbBinaryBuffer 16 byte buffer containing a raw GUID/UUID
 * @throw bad_alloc If there isn't enough memory left to allocate the internal GUID/UUID buffer
 * @note This instance of the Guid object will be initialized with the GUID/UUID value contained
 * in the first 16 bytes within the buffer pointed to by @p c_pbBinaryBuffer
 *
 ********************************************************************************************/

Guid::Guid(
    _in const Byte * c_pbBinaryBuffer
    )
{
    __DebugFunction();

    m_stlRawData.resize(16);
    if (nullptr != c_pbBinaryBuffer)
    {
        ::memcpy((void *) m_stlRawData.data(), (void *) c_pbBinaryBuffer, 16);
    }
    else
    {
        ::memset((void *) m_stlRawData.data(), 0, 16);
    }
}

/********************************************************************************************
 *
 * @class Guid
 * @function Guid
 * @brief Default copy constructor
 * @param[in] c_oGuid Instance of a Guid object to copy from
 * @throw bad_alloc If there isn't enough memory left to allocate the internal GUID/UUID buffer
 *
 ********************************************************************************************/

Guid::Guid(
    _in const Guid & c_oGuid
    )
{
    __DebugFunction();
    __DebugAssert(16 == c_oGuid.m_stlRawData.size());

    m_stlRawData = c_oGuid.m_stlRawData;
}

/********************************************************************************************
 *
 * @class Guid
 * @function ~Guid
 * @brief Default destructor
 *
 ********************************************************************************************/

Guid::~Guid(void) throw()
{
    __DebugFunction();

    m_stlRawData.clear();
}

/********************************************************************************************
 *
 * @class Guid
 * @function operator =
 * @brief Assignment operator = override
 * @param[in] c_szGuid String representation of a GUID/UUID
 * @throw BaseException Invalid or improperly formatted @p c_szGuid parameter value
 * @throw bad_alloc If there isn't enough memory left to allocate the internal GUID/UUID buffer
 * @return Guid object
 *
 ********************************************************************************************/

Guid & __thiscall Guid::operator = (
    _in const char * c_szGuid
    )
{
    __DebugFunction();

    this->InitializeFromString(c_szGuid);

    return *this;
}

/********************************************************************************************
 *
 * @class Guid
 * @function operator =
 * @brief Assignment operator = override
 * @param[in] c_oGuid Instance of a Guid object to copy from
 * @throw bad_alloc If there isn't enough memory left to allocate the internal GUID/UUID buffer
 * @return Guid object
 *
 ********************************************************************************************/

Guid & __thiscall Guid::operator = (
    _in const Guid & c_oGuid
    )
{
    __DebugFunction();
    __DebugAssert(16 == c_oGuid.m_stlRawData.size());

    m_stlRawData = c_oGuid.m_stlRawData;

    return *this;
}

/********************************************************************************************
 *
 * @class Guid
 * @function operator ==
 * @brief Comparison operator == override
 * @param[in] c_szGuid String representation of a GUID/UUID
 * @return true if equal
 * @return false otherwise
 *
 ********************************************************************************************/

bool __thiscall Guid::operator == (
    _in const char * c_szGuid
    ) const throw()
{
    __DebugFunction();
    __DebugAssert(16 == m_stlRawData.size());

    bool fIsEqual = false;

    try
    {
        Guid oGuidToCompareTo(c_szGuid);

        fIsEqual = (m_stlRawData == oGuidToCompareTo.m_stlRawData);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return fIsEqual;
}

/********************************************************************************************
 *
 * @class Guid
 * @function operator ==
 * @brief Comparison operator == override
 * @param[in] c_oGuid Instance of a Guid object to compare with
 * @return true if equal
 * @return false otherwise
 *
 ********************************************************************************************/

bool __thiscall Guid::operator == (
    _in const Guid & c_oGuid
    ) const throw()
{
    __DebugFunction();
    __DebugAssert(16 == m_stlRawData.size());
    __DebugAssert(16 == c_oGuid.m_stlRawData.size());

    return (m_stlRawData == c_oGuid.m_stlRawData);
}

/********************************************************************************************
 *
 * @class Guid
 * @function operator !=
 * @brief Comparison operator != override
 * @param[in] c_szGuid String representation of a GUID/UUID
 * @return true if not equal
 * @return false otherwise
 *
 ********************************************************************************************/

bool __thiscall Guid::operator != (
    _in const char * c_szGuid
    ) const throw()
{
    __DebugFunction();
    __DebugAssert(16 == m_stlRawData.size());

    bool fIsDifferent = false;

    try
    {
        Guid oGuidToCompareTo(c_szGuid);

        fIsDifferent = (m_stlRawData != oGuidToCompareTo.m_stlRawData);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return fIsDifferent;
}

/********************************************************************************************
 *
 * @class Guid
 * @function operator !=
 * @brief Comparison operator != override
 * @param[in] c_oGuid Instance of a Guid object to compare with
 * @return true if not equal
 * @return false otherwise
 *
 ********************************************************************************************/

bool __thiscall Guid::operator != (
    _in const Guid & c_oGuid
    ) const throw()
{
    __DebugFunction();
    __DebugAssert(16 == m_stlRawData.size());
    __DebugAssert(16 == c_oGuid.m_stlRawData.size());

    return (m_stlRawData != c_oGuid.m_stlRawData);
}

/********************************************************************************************
 *
 * @class Guid
 * @function GetRawDataPtr
 * @brief Returns a const Byte * to the first byte in the raw data buffer containing the GUID/UUID
 * @return Contant byte pointer to the first byte in the raw data buffer containing the GUID/UUID
 *
 ********************************************************************************************/

const Byte * __thiscall Guid::GetRawDataPtr(void) const throw()
{
    __DebugFunction();
    __DebugAssert(16 == m_stlRawData.size());

    return (const Byte *) m_stlRawData.data();
}

/********************************************************************************************
 *
 * @class Guid
 * @function GetRawData
 * @brief Returns a buffer containing the raw bytes representing the GUID/UUID
 * @return A buffer containing the raw bytes representing the GUID/UUID
 *
 ********************************************************************************************/

std::vector<Byte> __thiscall Guid::GetRawData(void) const throw()
{
    __DebugFunction();
    __DebugAssert(16 == m_stlRawData.size());

    return m_stlRawData;
}

/********************************************************************************************
 *
 * @class Guid
 * @function ToString
 * @brief Returns a string representation of the GUID/UUID
 * @param[in] eGuidFormat Which GUID/UUID format to use in the string formatting (eHyphensOnly, eHyphensAndCurlyBraces, eRaw)
 * @return A string representation of the GUID/UUID
 * @note
 *    The string formatting can be one of:
 *    1. eRaw --> E574DA3068843FD9690B5E15DE11402
 *    2. eHyphensOnly --> E574DA3-0688-43FD-9690-B5E15DE11402
 *    3. eHyphensAndCurlyBraces --> {6E574DA3-0688-43FD-9690-B5E15DE11402}
 *
 ********************************************************************************************/

std::string __thiscall Guid::ToString(
    _in GuidFormat eGuidFormat
    ) const throw()
{
    __DebugAssert(16 == m_stlRawData.size());

    char szGuid[40];
    GUID * pGuid = (GUID *) m_stlRawData.data();

    switch(eGuidFormat)
    {
        case eForceRaw // 6E574DA3068843FD9690B5E15DE11402 --------> raw
        :   ::snprintf(szGuid, sizeof(szGuid), "%08X%04hX%04hX%02hhX%02hhX%02hhX%02hhX%02hhX%02hhX%02hhX%02hhX", pGuid->Data1, pGuid->Data2, pGuid->Data3, pGuid->Data4[0], pGuid->Data4[1], pGuid->Data4[2], pGuid->Data4[3], pGuid->Data4[4], pGuid->Data4[5], pGuid->Data4[6], pGuid->Data4[7]);
            break;
        case eForceHyphensAndCurlyBraces // {6E574DA3-0688-43FD-9690-B5E15DE11402} --> with hyphens and braces
        :   ::snprintf(szGuid, sizeof(szGuid), "{%08X-%04hX-%04hX-%02hhX%02hhX-%02hhX%02hhX%02hhX%02hhX%02hhX%02hhX}", pGuid->Data1, pGuid->Data2, pGuid->Data3, pGuid->Data4[0], pGuid->Data4[1], pGuid->Data4[2], pGuid->Data4[3], pGuid->Data4[4], pGuid->Data4[5], pGuid->Data4[6], pGuid->Data4[7]);
            break;
        default // 6e574da3-0688-43fd-9690-b5e15de11402 ----> with hyphens
        :   ::snprintf(szGuid, sizeof(szGuid), "%08x-%04hx-%04hx-%02hhx%02hhx-%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx", pGuid->Data1, pGuid->Data2, pGuid->Data3, pGuid->Data4[0], pGuid->Data4[1], pGuid->Data4[2], pGuid->Data4[3], pGuid->Data4[4], pGuid->Data4[5], pGuid->Data4[6], pGuid->Data4[7]);
            break;
    };

    return std::string(szGuid);
}

/********************************************************************************************
 *
 * @class Guid
 * @function GetObjectType
 * @brief Method used to fetch type of object represented by the 4 MSBs of the Guid
 * @return Work representing type of object represented by the 4 MSBs of the Guid
 *
 ********************************************************************************************/

GuidObjectType __thiscall Guid::GetObjectType(void) const throw()
{
    __DebugFunction();

	Byte bObjectType = (m_stlRawData[0] & eGuidTypeBitMask);
	
    return (GuidObjectType) bObjectType;
}

/********************************************************************************************
 *
 * @class Guid
 * @function ConvertHexadecimalSubStringIntoIdentifierComponent
 * @brief Internal method used to convert a portion of a hexadecimal string which represents
 * a GUID/UUID into binary before storing the result within the internal m_stlRawData at
 * a particular byte offset. This method is only used by InitializeString
 * @param[in] strHexadecimalString Plain GUID/UUID string
 * @param[in] unStartingOffset Starting offset (in character count) to start parsing the hex number
 * @param[in] unLength Length (in character count) to parse the hex number
 * @param[in] unByteOffsetDestination Destination (in byte offset) to write converted number into m_stlRawData
 * 
 ********************************************************************************************/

void __thiscall Guid::ConvertHexadecimalSubStringIntoIdentifierComponent(
    _in const std::string & strHexadecimalString,
    _in unsigned int unStartingOffset,
    _in unsigned int unLength
    )
{
    __DebugFunction();

    // Extract the target substring from the original hexadecimal string
    std::string strSubString = strHexadecimalString.substr(unStartingOffset, unLength);
    // Convert the hexadecimal substring into a number value
    unsigned int unSubStringValue = std::strtoul(strSubString.c_str(), nullptr, 16);
    // Copy the number value into m_stlRawData at the desired offset
    ::memcpy((void * ) &(m_stlRawData[unStartingOffset/2]), (const void *) &unSubStringValue, (unLength/2));
}

/********************************************************************************************
 *
 * @class Guid
 * @function InitializeFromString
 * @brief Method used to initialize the internal GUID/UUID 16 byte buffer with the value represented with an incoming formatted @p c_szGuid string
 * @param[in] c_szGuid Formatted GUID/UUID string
 * @throw BaseException Invalid or improperly formatted @p c_szGuid parameter value
 * @throw bad_alloc If there isn't enough memory left to allocate the internal GUID/UUID buffer
 *
 ********************************************************************************************/

void __thiscall Guid::InitializeFromString(
    _in const char * c_szGuid
    )
{
    __DebugFunction();

    m_stlRawData.resize(16);
    if (nullptr == c_szGuid)
    {
        // If the incoming string is nullptr, then the GUID/UUID is initialized to all 0's
        ::memset((void *) m_stlRawData.data(), 0, 16);
    }
    else
    {
        std::string strGuid = c_szGuid;
    
        if ('{' == strGuid[0])
        {
            if ((38 == strGuid.size())&&('-' == strGuid[9])&&('-' == strGuid[14])&&('-' == strGuid[19])&&('-' == strGuid[24])&&('}' == strGuid[37]))
            {
                // We need to remove the {, } and - from the string
                strGuid.erase(std::remove(strGuid.begin(), strGuid.end(), '{'), strGuid.end());
                strGuid.erase(std::remove(strGuid.begin(), strGuid.end(), '}'), strGuid.end());
                strGuid.erase(std::remove(strGuid.begin(), strGuid.end(), '-'), strGuid.end());
            }
            else
            {
                _ThrowSimpleException("INVALID FORMAT. Invalid format provided in incoming string.");
            }
        }
        else if ('-' == strGuid[8])
        {
            if ((36 == strGuid.size())&&('-' == strGuid[13])&&('-' == strGuid[18])&&('-' == strGuid[23]))
            {
                // We need to remove the - from the string
                strGuid.erase(std::remove(strGuid.begin(), strGuid.end(), '-'), strGuid.end());   
            }
            else
            {
                _ThrowSimpleException("INVALID FORMAT. Invalid format provided in incoming string.");
            }
        }
        else if (32 != strGuid.size())
        {
            _ThrowSimpleException("INVALID FORMAT. Invalid format provided in incoming string.");
        }

        // Parse the strGuid string. The format is:
        // 
        //   1111111122223333445566778899AABB
        // 
        // where each number is one of the elements of the guid object which needs
        // to be parsed from a hexadecimal value string into a number which is then
        // persisted into m_stlRawData by ConvertHexadecimalSubStringIntoIdentifierComponent()
        this ->ConvertHexadecimalSubStringIntoIdentifierComponent(strGuid, 0, 8);
        this ->ConvertHexadecimalSubStringIntoIdentifierComponent(strGuid, 8, 4);
        this ->ConvertHexadecimalSubStringIntoIdentifierComponent(strGuid, 12, 4);
        this ->ConvertHexadecimalSubStringIntoIdentifierComponent(strGuid, 16, 2);
        this ->ConvertHexadecimalSubStringIntoIdentifierComponent(strGuid, 18, 2);
        this ->ConvertHexadecimalSubStringIntoIdentifierComponent(strGuid, 20, 2);
        this ->ConvertHexadecimalSubStringIntoIdentifierComponent(strGuid, 22, 2);
        this ->ConvertHexadecimalSubStringIntoIdentifierComponent(strGuid, 24, 2);
        this ->ConvertHexadecimalSubStringIntoIdentifierComponent(strGuid, 26, 2);
        this ->ConvertHexadecimalSubStringIntoIdentifierComponent(strGuid, 28, 2);
        this ->ConvertHexadecimalSubStringIntoIdentifierComponent(strGuid, 30, 2);
    }
}
