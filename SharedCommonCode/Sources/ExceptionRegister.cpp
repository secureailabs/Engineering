/*********************************************************************************************
 *
 * @file ExceptionRegister.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Implementations of C functions used to generate quick 64 bit hashes.
 *
 * In some circumstances, it is really useful to use 64-bit hashes as opposed to larger
 * hashes like MD-5 or SHA-1 and SHA-2. The biggest use of such hashes are for indexing
 * element using STL objects, like std::map. Since 64 bit is a native size to the CPU, it
 * indexes a lot quicker within STL than if you used a larger buffer hosting a more
 * traditional hash.
 *
 ********************************************************************************************/

#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "CoreTypes.h"
#include "DebugLibrary.h"

#include <iostream>
#include <mutex>
#include <queue>
#include <string>
#include <thread>
#include <unordered_map>

static uint64_t gs_un64NextAvailableExceptionIdentier = 0;
static std::unordered_map<uint64_t, std::string> gs_stlAllRegisteredExceptions;
static std::unordered_map<std::thread::id, std::queue<uint64_t>> gs_stlRegisteredExceptionsPerThread;
static std::queue<std::thread::id> gs_stlQueueOfExceptionsForAllThreads;
static std::mutex gs_stlMutex;

/// <summary>
/// Register a BaseException in the internal queue
/// </summary>
/// <param name="c_oBaseException"></param>
/// <param name="c_szFunctionName"></param>
/// <param name="c_szFilename"></param>
/// <param name="unLineNumber"></param>
/// <returns></returns>

static void __stdcall RegisterException(
    _in const std::string & c_strExceptionMessage
    ) throw()
{
    __DebugFunction();
    
    try
    {
        // Use a lock_guard to make sure that if gs_stlQueueOfExceptions.push throws and
        // exception, the mutex gets unlocked automatically
        const std::lock_guard<std::mutex> lock(gs_stlMutex);
        // Get the next available registered exception identifier, then increment
        uint64_t un64RegisteredExceptionIdentifier = gs_un64NextAvailableExceptionIdentier++;
        // Register the exception, make sure it is tracked per thread as well
        gs_stlAllRegisteredExceptions[un64RegisteredExceptionIdentifier] = c_strExceptionMessage;
        gs_stlQueueOfExceptionsForAllThreads.push(std::this_thread::get_id());
        gs_stlRegisteredExceptionsPerThread[std::this_thread::get_id()].push(un64RegisteredExceptionIdentifier);
    }
    
    catch(...)
    {
        // We do NOTHING here, since this would cause recursion if we call back into
        // the exception register functions.
    }
}

/// <summary>
/// Register a BaseException in the internal queue
/// </summary>
/// <param name="c_oBaseException"></param>
/// <param name="c_szFunctionName"></param>
/// <param name="c_szFilename"></param>
/// <param name="unLineNumber"></param>
/// <returns></returns>
void __stdcall RegisterBaseException(
    _in const BaseException & c_oBaseException,
    _in const char * c_szFunctionName,
    _in const char * c_szFileName,
    _in unsigned int unLineNumber
    ) throw()
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szFunctionName);

    try
    {
        std::string strExceptionMessage;

        strExceptionMessage = "Thrown from -> |File = ";
        strExceptionMessage += c_oBaseException.GetFilename();
        strExceptionMessage += "\r\n               |Function = ";
        strExceptionMessage += c_oBaseException.GetFunctionName();
        strExceptionMessage += "\r\n               |Line Number = ";
        strExceptionMessage += std::to_string(c_oBaseException.GetLineNumber());
        strExceptionMessage += "\r\n               |Message = ";
        strExceptionMessage += c_oBaseException.GetExceptionMessage();
        strExceptionMessage += "\r\nCaught in ---->|File = ";
        strExceptionMessage += c_szFileName;
        strExceptionMessage += "\r\n               |Function = ";
        strExceptionMessage += c_szFunctionName;
        strExceptionMessage += "\r\n               |Line Number = ";
        strExceptionMessage += std::to_string(unLineNumber);
        
        ::RegisterException(strExceptionMessage);
    }

    catch(...)
    {
        // We do NOTHING here, since this would cause recursion if we call back into
        // the exception register functions.
    }
}

/// <summary>
/// Register an standard exception in the internal queue
/// </summary>
/// <param name="c_szExceptionMessage"></param>
/// <param name="c_szFunctionName"></param>
/// <param name="c_szFilename"></param>
/// <param name="unLineNumber"></param>
/// <returns></returns>
void __stdcall RegisterStandardException(
    _in const std::exception & c_oStandardException,
    _in const char * c_szFunctionName,
    _in const char * c_szFileName,
    _in unsigned int unLineNumber
    ) throw()
{
     __DebugFunction();
    __DebugAssert(nullptr != c_szFunctionName);

    try
    {
        std::string strExceptionMessage;

        strExceptionMessage =  "-----------------> |Message = ";
        strExceptionMessage += c_oStandardException.what();
        strExceptionMessage += "\r\nCaught in ---->|File = ";
        strExceptionMessage += c_szFileName;
        strExceptionMessage += "\r\n               |Function = ";
        strExceptionMessage += c_szFunctionName;
        strExceptionMessage += "\r\n               |Line Number = ";
        strExceptionMessage += std::to_string(unLineNumber);

        ::RegisterException(strExceptionMessage);
    }

    catch(...)
    {
        // We do NOTHING here, since this would cause recursion if we call back into
        // the exception register functions.
    }
}
    
/// <summary>
/// Register an unknown exception in the internal queue
/// </summary>
/// <param name="c_szFunctionName"></param>
/// <param name="unLineNumber"></param>
/// <returns></returns>
void __stdcall RegisterUnknownException(
    _in const char * c_szFunctionName,
    _in const char * c_szFileName,
    _in unsigned int unLineNumber
    ) throw()
{
    __DebugFunction();
    __DebugAssert(nullptr != c_szFunctionName);

    try
    {
        std::string strExceptionMessage;

        strExceptionMessage = "UNKNOWN EXCEPTION!!!!!";
        strExceptionMessage += "\r\nCaught in ---->|File = ";
        strExceptionMessage += c_szFileName;
        strExceptionMessage += "\r\n               |Function = ";
        strExceptionMessage += c_szFunctionName;
        strExceptionMessage += "\r\n               |Line Number = ";
        strExceptionMessage += std::to_string(unLineNumber);
        
        ::RegisterException(strExceptionMessage);
    }

    catch(...)
    {
        // We do NOTHING here, since this would cause recursion if we call back into
        // the exception register functions.
    }
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
unsigned int __stdcall GetRegisteredExceptionsCount(void) throw()
{
    __DebugFunction();
    
    unsigned int unRegisteredExceptionCount = 0;

    try
    {
        // Use a lock_guard to make sure that if gs_stlQueueOfExceptions.push throws and
        // exception, the mutex gets unlocked automatically
        const std::lock_guard<std::mutex> lock(gs_stlMutex);
        __DebugAssert(gs_stlQueueOfExceptionsForAllThreads.size() == gs_stlAllRegisteredExceptions.size());
        unRegisteredExceptionCount = (unsigned int) gs_stlAllRegisteredExceptions.size();
    }

    catch(...)
    {
        // We do NOTHING here, since this would cause recursion if we call back into
        // the exception register functions.
    }

    return unRegisteredExceptionCount;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
unsigned int __stdcall GetRegisteredExceptionsCountForCurrentThread(void) throw()
{
    __DebugFunction();
    
    unsigned int unRegisteredExceptionCount = 0;

    try
    {
        // Use a lock_guard to make sure that if gs_stlQueueOfExceptions.push throws and
        // exception, the mutex gets unlocked automatically
        const std::lock_guard<std::mutex> lock(gs_stlMutex);
        unRegisteredExceptionCount = (unsigned int) gs_stlRegisteredExceptionsPerThread[std::this_thread::get_id()].size();
    }

    catch(...)
    {
        // We do NOTHING here, since this would cause recursion if we call back into
        // the exception register functions.
    }

    return unRegisteredExceptionCount;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
std::string __stdcall GetNextRegisteredException(void) throw()
{
    __DebugFunction();

    std::string strNextRegisteredException = "";

    try
    {
        // Use a lock_guard to make sure that if gs_stlQueueOfExceptions.push throws and
        // exception, the mutex gets unlocked automatically
        const std::lock_guard<std::mutex> lock(gs_stlMutex);
        if (false == gs_stlQueueOfExceptionsForAllThreads.empty())
        {
            std::thread::id stlThreadIdentifier = gs_stlQueueOfExceptionsForAllThreads.front();
            gs_stlQueueOfExceptionsForAllThreads.pop();
            if (gs_stlRegisteredExceptionsPerThread.end() != gs_stlRegisteredExceptionsPerThread.find(stlThreadIdentifier))
            {
                uint64_t un64RegisterExceptionIdentifier = gs_stlRegisteredExceptionsPerThread[stlThreadIdentifier].front();
                gs_stlRegisteredExceptionsPerThread[stlThreadIdentifier].pop();
                if (gs_stlAllRegisteredExceptions.end() != gs_stlAllRegisteredExceptions.find(un64RegisterExceptionIdentifier))
                {
                    strNextRegisteredException = gs_stlAllRegisteredExceptions[un64RegisterExceptionIdentifier];
                    gs_stlAllRegisteredExceptions.erase(un64RegisterExceptionIdentifier);
                }
            }
        }
    }

    catch(...)
    {
        // We do NOTHING here, since this would cause recursion if we call back into
        // the exception register functions.
    }

    return strNextRegisteredException;
}