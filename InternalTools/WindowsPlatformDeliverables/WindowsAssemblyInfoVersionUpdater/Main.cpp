// BuildVersionGenerator.cpp : Defines the entry point for the application.
//

#include "CoreTypes.h"
#include "DateAndTime.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"

#include <windows.h>

#include <filesystem>
#include <fstream>
#include <iostream>
#include <regex>
#include <sstream>
#include <string>

/// <summary>
/// 
/// </summary>
/// <param name="c_strInputString"></param>
/// <param name="c_strStringToLookFor"></param>
/// <param name="c_strStringToReplaceWith"></param>
/// <returns></returns>
static std::string __stdcall ReplaceInString(
    _in const std::string & c_strInputString,
    _in const std::string & c_strStringToLookFor,
    _in const std::string & c_strStringToReplaceWith
    )
{
    __DebugFunction();

    std::string strNewString = c_strInputString;
    int nOffset = (int) c_strInputString.find(c_strStringToLookFor);
    if (std::string::npos != nOffset)
    {
        strNewString.replace(nOffset, c_strStringToLookFor.length(), c_strStringToReplaceWith);
    }
    
    return strNewString;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
static std::string __stdcall GetVersionString(void)
{
    __DebugFunction();

    std::string strVersionString = "0.0.0.0";
    HKEY hRegistryKey;
    if (ERROR_SUCCESS == ::RegOpenKeyExA(HKEY_CURRENT_USER, "Environment", 0, (KEY_WOW64_64KEY | KEY_QUERY_VALUE), &hRegistryKey))
    {
        Dword dwType = REG_SZ;
        char szVersionString[30];
        unsigned int unSizeInCharactersOfVersionString = sizeof(szVersionString);
        if (ERROR_SUCCESS == ::RegQueryValueExA(hRegistryKey, "SAIL_VERSION", 0, (LPDWORD) &dwType, (LPBYTE) szVersionString, (LPDWORD) &unSizeInCharactersOfVersionString))
        {
            strVersionString = szVersionString;
        }
        ::RegCloseKey(hRegistryKey);
    }

    return strVersionString;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
static std::string __stdcall GetCommitIdentifier(void)
{
    __DebugFunction();

    std::string strCommitIdentifier = "000000";
    HKEY hRegistryKey;
    if (ERROR_SUCCESS == ::RegOpenKeyExA(HKEY_CURRENT_USER, "Environment", 0, (KEY_WOW64_64KEY | KEY_QUERY_VALUE), &hRegistryKey))
    {
        Dword dwType = REG_SZ;
        char szVersionString[30];
        unsigned int unSizeInCharactersOfVersionString = sizeof(szVersionString);
        if (ERROR_SUCCESS == ::RegQueryValueExA(hRegistryKey, "SAIL_COMMIT_ID", 0, (LPDWORD) &dwType, (LPBYTE) szVersionString, (LPDWORD) &unSizeInCharactersOfVersionString))
        {
            strCommitIdentifier = szVersionString;
        }
        ::RegCloseKey(hRegistryKey);
    }

    return strCommitIdentifier;
}

/// <summary>
/// Reads a text file and returns an array of strings, each representing
/// a line in the file
/// </summary>
/// <param name="c_strAssemblyInfoFilename"></param>
/// <returns></returns>
static std::vector<std::string> __stdcall ReadAssemblyInfoFromFile(
    _in const std::string & c_strAssemblyInfoFilename
    )
{
    __DebugFunction();

    std::vector<std::string> stlArrayOfStrings;
    _ThrowBaseExceptionIf((false == std::filesystem::exists(c_strAssemblyInfoFilename)), "ERROR: Assembly Info file %s not found", c_strAssemblyInfoFilename.c_str());
    std::ifstream stlAssemblyInfoFileStream(c_strAssemblyInfoFilename);
    std::string strLineOfText;
    while (std::getline(stlAssemblyInfoFileStream, strLineOfText))
    {
        stlArrayOfStrings.push_back(strLineOfText);
    }
    
    return stlArrayOfStrings;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_strAssemblyInfoFilename"></param>
/// <param name="c_strAssemblyInfo"></param>
/// <returns></returns>
static void __stdcall WriteAssemblyInfoFile(
    _in const std::string & c_strAssemblyInfoFilename,
    _in const std::vector<std::string> & c_strAssemblyInfo
    )
{
    __DebugFunction();

    std::ofstream stlAssemblyInfoStream(c_strAssemblyInfoFilename, std::ios::trunc);
    for (const std::string strLineOfText: c_strAssemblyInfo)
    {
        stlAssemblyInfoStream << strLineOfText << std::endl;
    }
    stlAssemblyInfoStream.close();
}

/// <summary>
/// 
/// </summary>
/// <param name="c_strAssemblyInfoTargetFilename"></param>
/// <param name="c_strVersionString"></param>
/// <returns></returns>
static int __stdcall UpdateVersionInformationInAssemblyInfoFile(
    _in const std::string & c_strAssemblyInfoFilename,
    _in const std::string & c_strVersionString,
    _in const std::string & c_strCommitIdentifier
    )
{
    __DebugFunction();

    int nReturnValue = -1;
    // Read the assembly info into a string buffer
    std::vector<std::string> stlAssemblyInfo = ::ReadAssemblyInfoFromFile(c_strAssemblyInfoFilename);
    // Now replace the version information in the assembly info buffer
    int nAssemblyTitleIndex = -1;
    int nAssemblyVersionIndex = -1;
    int nAssemblyFileVersionIndex = -1;
    int nAssemblyProductIndex = -1;
    std::string strUpdatedAssemblyVersion = "[assembly: AssemblyVersion(\"" + c_strVersionString + "\")]";
    std::string strUpdatedAssemblyFileVersion = "[assembly: AssemblyFileVersion(\"" + c_strVersionString + "\")]";
    for (unsigned int unIndex = 0; unIndex < stlAssemblyInfo.size(); ++unIndex)
    {
        if (std::string::npos != stlAssemblyInfo[unIndex].find("[assembly: AssemblyVersion("))
        {
            nAssemblyVersionIndex = (int) unIndex;
        }

        if (std::string::npos != stlAssemblyInfo[unIndex].find("[assembly: AssemblyFileVersion("))
        {
            nAssemblyFileVersionIndex = (int) unIndex;
        }

        if (std::string::npos != stlAssemblyInfo[unIndex].find("[assembly: AssemblyTitle("))
        {
            nAssemblyTitleIndex = (int) unIndex;
        }

        if (std::string::npos != stlAssemblyInfo[unIndex].find("[assembly: AssemblyProduct("))
        {
            nAssemblyProductIndex = (int) unIndex;
        }
    }

    // Now do the actual replacing of values. In some cases, if the
    // value was not found (i.e. index is -1), the we insert it
    if (-1 == nAssemblyVersionIndex)
    {
        stlAssemblyInfo.push_back(strUpdatedAssemblyVersion);
    }
    else
    {
        stlAssemblyInfo[nAssemblyVersionIndex] = strUpdatedAssemblyVersion;
    }
    if (-1 == nAssemblyFileVersionIndex)
    {
        stlAssemblyInfo.push_back(strUpdatedAssemblyFileVersion);
    }
    else
    {
        stlAssemblyInfo[nAssemblyFileVersionIndex] = strUpdatedAssemblyFileVersion;
    }
    if ((-1 != nAssemblyTitleIndex)&&(-1 != nAssemblyProductIndex))
    {
        std::string strCurrentString = stlAssemblyInfo[nAssemblyProductIndex];
        std::string strModification = " - Version " + c_strVersionString + " (" + c_strCommitIdentifier + ")\")]";
        strCurrentString = ::ReplaceInString(strCurrentString, "\")]", strModification);
        strCurrentString = ::ReplaceInString(strCurrentString, "AssemblyProduct", "AssemblyTitle");
        stlAssemblyInfo[nAssemblyTitleIndex] = strCurrentString;
    }

    // Now write the results back to the original assembly info file
    ::WriteAssemblyInfoFile(c_strAssemblyInfoFilename, stlAssemblyInfo);

    return nReturnValue;
}

/// <summary>
/// 
/// </summary>
/// <param name="hInstance"></param>
/// <param name="hPrevInstance"></param>
/// <param name="c_wzCommandLine"></param>
/// <param name="nCommandShow"></param>
/// <returns></returns>
INT WINAPI WinMain(
     _in HINSTANCE hInstance,
     _in HINSTANCE hPrevInstance,
     _in PSTR c_szCommandLine,
     _in INT nCommandShow
    )
{
    __DebugFunction();

    UNREFERENCED_PARAMETER(hInstance);
    UNREFERENCED_PARAMETER(hPrevInstance);
    UNREFERENCED_PARAMETER(nCommandShow);

    int nReturnValue = -1;

    try
    {
        // Get the current version string. Whoever is calling this application should also
        // make sure to call WindowsBuildVersionGenerator.exe first
        std::string strVersion = ::GetVersionString();
        std::string strCommitIdentifier = ::GetCommitIdentifier();
        // Read in the entire AssemblyInfo file into a string
        std::string strTargetAssemblyInfoFile = c_szCommandLine;
        // Erase any quotation marks if they exist in strTargetAssemblyInfoFile
        strTargetAssemblyInfoFile.erase(remove(strTargetAssemblyInfoFile.begin(), strTargetAssemblyInfoFile.end(), '\"'), strTargetAssemblyInfoFile.end());
        // Now update the version information into the target file
        nReturnValue = ::UpdateVersionInformationInAssemblyInfoFile(strTargetAssemblyInfoFile, strVersion, strCommitIdentifier);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return (int) nReturnValue;
}
