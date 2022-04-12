/*********************************************************************************************
 *
 * @file DataAndTime.cpp
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @license Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include <windows.h>

#include "DateAndTime.h"
#include "DebugLibrary.h"
#include <time.h>

/********************************************************************************************/

uint64_t __stdcall GetEpochTimeInSeconds(void) throw()
{
    __DebugFunction();

    // et the number of seconds since January 1, 1970 12:00am UTC
    // Code released into public domain; no attribution required.

    const uint64_t un64UnixStartTime = 0x019DB1DED53E8000; // January 1, 1970 (start of Unix epoch) in "ticks"
    const uint64_t un64TicksPerSecond = 10000000; // a tick is 100ns

    FILETIME sFileTime;
    ::GetSystemTimeAsFileTime(&sFileTime); // returns ticks in UTC

    // Copy the low and high parts of FILETIME into a LARGE_INTEGER
    // This is so we can access the full 64-bits as an Int64 without causing an alignment fault
    LARGE_INTEGER sLargeInteger;
    sLargeInteger.LowPart  = sFileTime.dwLowDateTime;
    sLargeInteger.HighPart = sFileTime.dwHighDateTime;
 
    // Convert ticks since 1/1/1970 into seconds
    return (sLargeInteger.QuadPart - un64UnixStartTime) / un64TicksPerSecond;
}

/********************************************************************************************/

uint64_t __stdcall GetEpochTimeInMilliseconds(void) throw()
{
	// et the number of seconds since January 1, 1970 12:00am UTC
    // Code released into public domain; no attribution required.

    const uint64_t un64UnixStartTime = 0x019DB1DED53E8000; // January 1, 1970 (start of Unix epoch) in "ticks"
    const uint64_t un64TicksPerMillisecondSecond = 10000; // a tick is 100ns

    FILETIME sFileTime;
    ::GetSystemTimeAsFileTime(&sFileTime); // returns ticks in UTC

    // Copy the low and high parts of FILETIME into a LARGE_INTEGER
    // This is so we can access the full 64-bits as an Int64 without causing an alignment fault
    LARGE_INTEGER sLargeInteger;
    sLargeInteger.LowPart  = sFileTime.dwLowDateTime;
    sLargeInteger.HighPart = sFileTime.dwHighDateTime;
 
    // Convert ticks since 1/1/1970 into seconds
    return (sLargeInteger.QuadPart - un64UnixStartTime) / un64TicksPerMillisecondSecond;
}
