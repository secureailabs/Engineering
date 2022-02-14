/*********************************************************************************************
 *
 * @file RootOfTrustCoreProperties.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "64BitHashes.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "RootOfTrustCoreProperties.h"

/*********************************************************************************************/

RootOfTrustCoreProperties::RootOfTrustCoreProperties(void)
{
    __DebugFunction();
}

/*********************************************************************************************/

RootOfTrustCoreProperties::~RootOfTrustCoreProperties(void)
{
    __DebugFunction();
}

/*********************************************************************************************/

std::string __thiscall RootOfTrustCoreProperties::GetProperty(
    _in const char * c_szPropertyName
    ) const throw()
{
    __DebugFunction();

    std::string strPropertyValue;

    try
    {
        Qword qwPropertyNameHash = ::Get64BitHashOfNullTerminatedString(c_szPropertyName, false);
        const std::lock_guard<std::mutex> lock(m_stlMutex);
        _ThrowBaseExceptionIf((m_stlProperties.end() == m_stlProperties.find(qwPropertyNameHash)), "Property %s not found in RootOfTrustCoreProperties", c_szPropertyName);
        strPropertyValue = m_stlProperties.at(qwPropertyNameHash);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return strPropertyValue;
}

/*********************************************************************************************/

void __thiscall RootOfTrustCoreProperties::SetProperty(
    _in const char * c_szPropertyName,
    _in const std::string & c_szPropertyValue
    ) throw()
{
    __DebugFunction();

    try
    {
        Qword qwPropertyNameHash = ::Get64BitHashOfNullTerminatedString(c_szPropertyName, false);
        const std::lock_guard<std::mutex> lock(m_stlMutex);
        m_stlProperties[qwPropertyNameHash] = c_szPropertyValue;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
}