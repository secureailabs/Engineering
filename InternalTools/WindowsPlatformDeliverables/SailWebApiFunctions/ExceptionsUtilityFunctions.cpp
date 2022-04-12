#include <Windows.h>

#include "CoreTypes.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "SharedUtilityFunctions.h"

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
extern "C" __declspec(dllexport) unsigned int __cdecl GetExceptionCount(void)
{
    __DebugFunction();

    // [DllImport("SailWebApiPortalFunctions.dll", CallingConvention = CallingConvention.Cdecl )]
    // static extern public uint GetExceptionCount();

    unsigned int unNumberOfExceptions = 0;

    try
    {
        unNumberOfExceptions = ::GetRegisteredExceptionCount();
    }

    catch (...)
    {

    }

    return unNumberOfExceptions;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl GetNextException(void)
{
    __DebugFunction();

    // [DllImport("SailWebApiPortalFunctions.dll", CallingConvention = CallingConvention.Cdecl )]
    // [return: MarshalAs(UnmanagedType.BStr)]
    // static extern public string GetNextException();

    std::string strException = "";

    try
    {
        strException = ::GetNextRegisteredException();
    }

    catch (...)
    {

    }

    return ::ConvertToBSTR(strException);
}