/*********************************************************************************************
 *
 * @file StringHelperFunctions.h
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

/// <summary>
/// Compares two full strings of ANSI characters until a null terminating character is found. This
/// comparison can be case sensitive, or not
/// </summary>
/// <param name="c_szInputString1"></param>
/// <param name="c_szInputString2"></param>
/// <param name="fCaseSensitive"></param>
/// <returns>Standard strcmp() return values</returns>
extern int __stdcall StringCompare(
	_in const char * c_szInputString1,
	_in const char * c_szInputString2,
	_in bool fCaseSensitive
	) throw();

/// <summary>
/// Compares two full strings of ANSI characters until the desired character cound is met or, until
/// a null terminating character is found. This comparison can be case sensitive, or not
/// </summary>
/// <param name="c_szInputString1"></param>
/// <param name="c_szInputString2"></param>
/// <param name="fCaseSensitive"></param>
/// <param name="unCharacterCount"></param>
/// <returns>Standard strcmp() return values</returns>
extern int __stdcall StringCompare(
	_in const char * c_szInputString1,
	_in const char * c_szInputString2,
	_in bool fCaseSensitive,
	_in unsigned int unCharacterCount
	) throw();