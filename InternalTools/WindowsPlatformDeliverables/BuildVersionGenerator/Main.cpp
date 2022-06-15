// BuildVersionGenerator.cpp : Defines the entry point for the application.
//

#include "CoreTypes.h"
#include "DateAndTime.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"

#include <windows.h>

#include <algorithm>
#include <iostream>
#include <filesystem>
#include <fstream>
#include <string>

/// <summary>
/// 
/// </summary>
/// <param name="c_stlDirectory"></param>
/// <returns></returns>
static std::string __stdcall FindRoot(
    _in const std::filesystem::path & c_stlDirectory
    )
{
    __DebugFunction();

    std::string strRootFolder = "";

    // First we try and determine whether or not we found the './git' folder rooted
    // in the current folder
    for (const auto & entry : std::filesystem::directory_iterator(c_stlDirectory))
    {       
        if ((true == entry.is_directory())&&(0 == strRootFolder.size()))
        {
            std::string strFilename = entry.path().filename().u8string();
            if (".git" == strFilename)
            {
                strRootFolder = c_stlDirectory.u8string();
            }
        }
    }

    // If we haven't found the root folder yet, recurse back
    // into this function using the parent folder
    if (0 == strRootFolder.size())
    {
        strRootFolder = ::FindRoot(c_stlDirectory.parent_path());
    }

    return strRootFolder;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_strRootDirectory"></param>
/// <returns></returns>
static std::string __stdcall GetClippedGitCommitIdentifier(
    _in std::string & c_strRootDirectory
    )
{
    __DebugFunction();
    __DebugAssert((0 < c_strRootDirectory.size())&&(true == std::filesystem::exists(c_strRootDirectory)));

    std::string strClippedGitCommitIdentifier;
    // Build the proper filename for the HEAD file in Git
    std::string strHeadFile = c_strRootDirectory + "\\.git\\HEAD";
    _ThrowBaseExceptionIf((false == std::filesystem::exists(strHeadFile)), "ERROR: Missing Git HEAD file %s", strHeadFile.c_str());
    // Read the first string in the HEAD file. We only need to read and
    // parse the first line
    std::ifstream stlHeadFileStream(strHeadFile);
    std::string strCurrentGitHead;
    if (std::getline(stlHeadFileStream, strCurrentGitHead))
    {
        strCurrentGitHead.erase(strCurrentGitHead.begin(), (strCurrentGitHead.begin() + 5));
        // because STL is wonky, we need to convert possible '/' characters into '\\' characters
        std::replace(strCurrentGitHead.begin(), strCurrentGitHead.end(), '/', '\\');
        // Now that we know which Git HEAD to use, let's build the name of the
        // file containing the commit identifier
        std::string strCommitIdentifierFile = c_strRootDirectory + "\\.git\\" + strCurrentGitHead;
        _ThrowBaseExceptionIf((false == std::filesystem::exists(strCommitIdentifierFile)), "ERROR: Missing Git commit identifier file %s", strCommitIdentifierFile.c_str());
        // Now let's open the commit identifier file and read in the commit identifier
        std::ifstream stlCommitIdentifierFileStream(strCommitIdentifierFile);
        if (std::getline(stlCommitIdentifierFileStream, strClippedGitCommitIdentifier))
        {
            // Since we are clipping the commit identifier, we only need to keep the
            // first 
            strClippedGitCommitIdentifier.resize(7);
        }
        // Make sure to close the commit identifier stream
        stlCommitIdentifierFileStream.close();
    }

    // Make sure to close the head file stream
    stlHeadFileStream.close();

    return strClippedGitCommitIdentifier;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_strRootDirectory"></param>
/// <returns></returns>
static std::string __stdcall GetMajorMinorVersionFromFile(
    _in std::string & c_strRootDirectory
    )
{
    __DebugFunction();

    std::string strMajorMinorVersion = "";
    std::string strMajorMinorVersionFilename = c_strRootDirectory + "\\VersionManagement\\MajorMinorVersion.txt";
    _ThrowBaseExceptionIf((false == std::filesystem::exists(strMajorMinorVersionFilename)), "ERROR: Missing Major/Minor version file %s", strMajorMinorVersionFilename.c_str());
    std::ifstream stlMajorMinorVersionFileStream(strMajorMinorVersionFilename);
    std::getline(stlMajorMinorVersionFileStream, strMajorMinorVersion);
    _ThrowBaseExceptionIf((0 == strMajorMinorVersion.size()), "ERROR: Failed to read Major/Minor version from file %s", strMajorMinorVersionFilename.c_str());

    return strMajorMinorVersion;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_strVersionNumber"></param>
/// <returns></returns>
static void __stdcall SetSessionWideEnvironmentVariable(
    _in const std::string & c_strEnvironmentVariableName,
    _in const std::string & c_strEnvironmentVariableValue
    )
{
    __DebugFunction();

    // First we need to write the environment variable value to HKEY_CURRENT_USER\Environment. We need to do this
    HKEY hRegistryKey = nullptr;
    if (ERROR_SUCCESS == ::RegOpenKeyExA(HKEY_CURRENT_USER, "Environment", 0, (KEY_WOW64_64KEY | KEY_SET_VALUE), &hRegistryKey))
    {
        ::RegSetValueExA(hRegistryKey, c_strEnvironmentVariableName.c_str(), 0, REG_SZ, (const Byte *) c_strEnvironmentVariableValue.c_str(), (DWORD) (c_strEnvironmentVariableValue.size() + 1));
        ::RegCloseKey(hRegistryKey);
    }

    if (ERROR_SUCCESS == ::RegOpenKeyExA(HKEY_CURRENT_USER, "Environment", 0, (KEY_WOW64_32KEY | KEY_SET_VALUE), &hRegistryKey))
    {
        ::RegSetValueExA(hRegistryKey, c_strEnvironmentVariableName.c_str(), 0, REG_SZ, (const Byte *) c_strEnvironmentVariableValue.c_str(), (DWORD) (c_strEnvironmentVariableValue.size() + 1));
        ::RegCloseKey(hRegistryKey);
    }

    // Now we need to send a message to the system to reload environment variables
    const char * c_szEnvironment = "Environment";
    ::SendMessageTimeoutA(HWND_BROADCAST, WM_SETTINGCHANGE, NULL, (LPARAM) c_szEnvironment, SMTO_NORMAL, 1000, nullptr);
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
    UNREFERENCED_PARAMETER(c_szCommandLine);
    UNREFERENCED_PARAMETER(nCommandShow);

    try
    {
        // First we need to find where the root of the GitHub repo. We do this by walking
        // the directory structure backwards until we find a .git folder

        std::string strRootDirectory = ::FindRoot(std::filesystem::current_path());

        // Now we need to extract the Git commit identifier for the current HEAD of
        // this repo
        std::string strClippedGitCommitIdentifier = ::GetClippedGitCommitIdentifier(strRootDirectory);

        // Sweet!!! Now we need to read in the Major.Minor values
        // from the file in .\\VersionManagement\\MajorMinorVersion.txt
        std::string strMajorMinorVersion = ::GetMajorMinorVersionFromFile(strRootDirectory);

        // Get Epoch time in days and number of minutes in the day
        uint64_t un64EpochTimeInSeconds = GetEpochTimeInSeconds();
        uint64_t un64EpochTimeInDays = un64EpochTimeInSeconds / (60 * 60 * 24);
        uint64_t un64NumberOfMinutesInTheDay = (un64EpochTimeInSeconds % 86400) / 60;

        // Now we can build the full version since
        std::string strVersionString = strMajorMinorVersion + "." + std::to_string(un64EpochTimeInDays) + "." + std::to_string(un64NumberOfMinutesInTheDay);

        // Now, let's set some environment variable
        ::SetSessionWideEnvironmentVariable("SAIL_VERSION", strVersionString.c_str());
        ::SetSessionWideEnvironmentVariable("SAIL_COMMIT_ID", strClippedGitCommitIdentifier.c_str());
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return (int) 0;
}
