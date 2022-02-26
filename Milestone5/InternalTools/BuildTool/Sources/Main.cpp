#include "64BitHashes.h"
#include "CommandLine.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "StringHelperFunctions.h"
#include "TextFileHandlers.h"

#include <algorithm>
#include <filesystem>
#include <iostream>
#include <unordered_map>
#include <unordered_set>

/********************************************************************************************/

static std::unordered_map<Qword, StructuredBuffer> gs_stlListOfNodes;
static std::unordered_set<Qword> gs_stlListOfNodesThatHaveBeenCleaned;
static std::unordered_set<Qword> gs_stlListOfNodesThatHaveBeenBuilt;
static std::string gs_strRootFolder;
static std::string gs_strCurrentFolder;
static std::string gs_strBuildMode{"debug"};
static std::string gs_strVersionString{"0.0.0"};

/********************************************************************************************/

static void __stdcall PrintUsage(void)
{
    __DebugFunction();
    
    std::cout << "Usage: BuiltTool --all <--clean> <--cleanonly>" << std::endl
              << "   or: BuiltTool --this <--clean> <--cleanonly>" << std::endl
              << "   or: BuiltTool --cleanall" << std::endl
              << "   or: BuiltTool --printnodes" << std::endl
              << "   or: BuiltTool --help" << std::endl << std::endl
              << "Where:" << std::endl
              << "       --all,         Instructs the build tool to build everything." << std::endl
              << "       --this,        Instructs the build tool to build only the project within the current." << std::endl
              << "                      folder, and all associated dependencies." << std::endl
              << "       --clean,       Instructs the build tool to clean all target projects before building." << std::endl
              << "       --cleanonly,   Instructs the build tool to clean all target projects and NOT build anything." << std::endl
              << "       --cleanall,    Instructs the build tool to clean everything and remove the build folder." << std::endl
              << "       --printnodes,  Instructs the build tool to print all build nodes everywhere." << std::endl
              << "       --help,        Instructs the build tool to print these instructions." << std::endl;
}

/********************************************************************************************/

static void __stdcall CleanNode(
    _in const StructuredBuffer & c_oCurrentBuildNode
    )
{
    __DebugFunction();
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("Identifier", GUID_VALUE_TYPE));
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("BuildNodeFullPathName", ANSI_CHARACTER_STRING_VALUE_TYPE));
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("BuildNodeHostFolder", ANSI_CHARACTER_STRING_VALUE_TYPE));
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("Name", ANSI_CHARACTER_STRING_VALUE_TYPE));
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("Os", ANSI_CHARACTER_STRING_VALUE_TYPE));
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("Type", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    // Figure out the hash of the identifier of the node
    std::string strBuildNodeIdentifier = c_oCurrentBuildNode.GetGuid("Identifier").ToString(eHyphensOnly);
    Qword qwHashOfNodeIdentifier = ::Get64BitHashOfNullTerminatedString(strBuildNodeIdentifier.c_str(), false);
    // Only build the node if it hasn't been built yet
    if (gs_stlListOfNodesThatHaveBeenCleaned.end() == gs_stlListOfNodesThatHaveBeenCleaned.find(qwHashOfNodeIdentifier))
    {
        // First, we mark down that this node has been built (or at least, we tried)
        gs_stlListOfNodesThatHaveBeenCleaned.insert(qwHashOfNodeIdentifier);
        // Now we figure out which dependencies need to be built first
        if (true == c_oCurrentBuildNode.IsElementPresent("Dependencies", INDEXED_BUFFER_VALUE_TYPE))
        {
            // Dependencies are stored within a nested StructuredBuffer made of
            // null values, whereupon the name of the values are the identifiers of the
            // nodes to build
            StructuredBuffer oDependencies(c_oCurrentBuildNode.GetStructuredBuffer("Dependencies"));
            // Just get the names of all of the elements. Effectively, each element name
            // should be the identifier of a node which is a dependency of the current node
            std::vector<std::string> strListOfIdentifiers{oDependencies.GetNamesOfElements()};
            for (const std::string & c_strBuildNodeIdentifier: strListOfIdentifiers)
            {
                Qword qwHashOfNodeIdentifier = ::Get64BitHashOfNullTerminatedString(c_strBuildNodeIdentifier.c_str(), false);
                if (gs_stlListOfNodes.end() != gs_stlListOfNodes.find(qwHashOfNodeIdentifier))
                {
                    ::CleanNode(gs_stlListOfNodes.at(qwHashOfNodeIdentifier));
                }
            }
        }
        
        // TODO: Eventually, we will look at the OS here, but for now, only Linux is supported
        if (::Get64BitHashOfNullTerminatedString("linux", false) == ::Get64BitHashOfNullTerminatedString(c_oCurrentBuildNode.GetString("Os").c_str(), false))
        {
            // TODO: For now, the only supported target is make, but eventually we will be able to support different tools
            if (::Get64BitHashOfNullTerminatedString("make", false) == ::Get64BitHashOfNullTerminatedString(c_oCurrentBuildNode.GetString("Type").c_str(), false))
            {
                std::filesystem::current_path(c_oCurrentBuildNode.GetString("BuildNodeHostFolder"));
                std::string strCommandLine = "make clean --silent ROOT=\"" + gs_strRootFolder + "\"";
                ::system(strCommandLine.c_str());
                std::cout << "Cleaned --> " << c_oCurrentBuildNode.GetString("Name") << std::endl;
            }
        }
        
        // Now we need to delete all published header files and libraries (if any)
        // First we start with include files
        if (true == c_oCurrentBuildNode.IsElementPresent("HeaderFilesToPublish", INDEXED_BUFFER_VALUE_TYPE))
        {
            std::vector<std::string> stlListOfIncludeFilesToPublish = c_oCurrentBuildNode.GetStructuredBuffer("HeaderFilesToPublish").GetNamesOfElements();
            for (const std::string & c_strIncludeFileName: stlListOfIncludeFilesToPublish)
            {
                // Build up for source and destination filenames
                std::string strTargetFilename = gs_strRootFolder + "/Build/Include/" + c_strIncludeFileName;
                if (true == std::filesystem::exists(strTargetFilename))
                {
                    // Build the string for the copy operation
                    std::string strDeleteOperation = "rm -f " + strTargetFilename + " 2>/dev/null || :";
                    ::system(strDeleteOperation.c_str());
                    // Now make sure the file is there
                    _ThrowBaseExceptionIf((true == std::filesystem::exists(strTargetFilename)), "UNEXPECTED ERROR: The include file %s failed to get deleted.", strTargetFilename.c_str());
                }
            }
        }
        // Now we delete the library files
        if (true == c_oCurrentBuildNode.IsElementPresent("LibrariesToPublish", INDEXED_BUFFER_VALUE_TYPE))
        {
            std::vector<std::string> stlListOfLibraryFilesToPublish = c_oCurrentBuildNode.GetStructuredBuffer("LibrariesToPublish").GetNamesOfElements();
            for (const std::string & c_strLibraryFileName: stlListOfLibraryFilesToPublish)
            {
                // Build up for source and destination filenames
                std::string strTargetFilename = gs_strRootFolder + "/Build/Libraries/" + c_strLibraryFileName;
                if (true == std::filesystem::exists(strTargetFilename))
                {
                    // Build the string for the copy operation
                    std::string strDeleteOperation = "rm -f " + strTargetFilename + " 2>/dev/null || :";
                    ::system(strDeleteOperation.c_str());
                    // Now make sure the file is there
                    _ThrowBaseExceptionIf((true == std::filesystem::exists(strTargetFilename)), "UNEXPECTED ERROR: The library file %s failed to get deleted.", strTargetFilename.c_str());
                }
            }
        }
    }
}

/********************************************************************************************/

static void __stdcall CleanAll(void)
{
    __DebugFunction();
    
    // To build all, we effectively just call BuildNode against all the elements in
    // gs_stlListOfNodes
    for (const auto & c_stlElement: gs_stlListOfNodes)
    {
        ::CleanNode(c_stlElement.second);
    }
}

/********************************************************************************************/

static void __stdcall BuildNode(
    _in const StructuredBuffer & c_oCurrentBuildNode
    )
{
    __DebugFunction();
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("Identifier", GUID_VALUE_TYPE));
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("BuildNodeFullPathName", ANSI_CHARACTER_STRING_VALUE_TYPE));
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("BuildNodeHostFolder", ANSI_CHARACTER_STRING_VALUE_TYPE));
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("Name", ANSI_CHARACTER_STRING_VALUE_TYPE));
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("Os", ANSI_CHARACTER_STRING_VALUE_TYPE));
    __DebugAssert(true == c_oCurrentBuildNode.IsElementPresent("Type", ANSI_CHARACTER_STRING_VALUE_TYPE));
    
    // Figure out the hash of the identifier of the node
    std::string strBuildNodeIdentifier = c_oCurrentBuildNode.GetGuid("Identifier").ToString(eHyphensOnly);
    Qword qwHashOfNodeIdentifier = ::Get64BitHashOfNullTerminatedString(strBuildNodeIdentifier.c_str(), false);
    // Only build the node if it hasn't been built yet
    if (gs_stlListOfNodesThatHaveBeenBuilt.end() == gs_stlListOfNodesThatHaveBeenBuilt.find(qwHashOfNodeIdentifier))
    {
        // First, we mark down that this node has been built (or at least, we tried)
        gs_stlListOfNodesThatHaveBeenBuilt.insert(qwHashOfNodeIdentifier);
        // Now we figure out which dependencies need to be built first
        if (true == c_oCurrentBuildNode.IsElementPresent("Dependencies", INDEXED_BUFFER_VALUE_TYPE))
        {
            // Dependencies are stored within a nested StructuredBuffer made of
            // null values, whereupon the name of the values are the identifiers of the
            // nodes to build
            StructuredBuffer oDependencies(c_oCurrentBuildNode.GetStructuredBuffer("Dependencies"));
            // Just get the names of all of the elements. Effectively, each element name
            // should be the identifier of a node which is a dependency of the current node
            std::vector<std::string> strListOfIdentifiers{oDependencies.GetNamesOfElements()};
            for (const std::string & c_strBuildNodeIdentifier: strListOfIdentifiers)
            {
                Qword qwHashOfNodeIdentifier = ::Get64BitHashOfNullTerminatedString(c_strBuildNodeIdentifier.c_str(), false);
                if (gs_stlListOfNodes.end() != gs_stlListOfNodes.find(qwHashOfNodeIdentifier))
                {
                    ::BuildNode(gs_stlListOfNodes.at(qwHashOfNodeIdentifier));
                }
            }
        }
        // TODO: Eventually, we will look at the OS here, but for now, only Linux is supported
        if (::Get64BitHashOfNullTerminatedString("linux", false) == ::Get64BitHashOfNullTerminatedString(c_oCurrentBuildNode.GetString("Os").c_str(), false))
        {
            // TODO: For now, the only supported target is make, but eventually we will be able to support different tools
            if (::Get64BitHashOfNullTerminatedString("make", false) == ::Get64BitHashOfNullTerminatedString(c_oCurrentBuildNode.GetString("Type").c_str(), false))
            {
                std::cout << "Building --> " << c_oCurrentBuildNode.GetString("Name") << " ... ";
                std::filesystem::current_path(c_oCurrentBuildNode.GetString("BuildNodeHostFolder"));
                std::string strCommandLine = "make all --silent -j 16 Version=" + gs_strVersionString + " MODE=" + gs_strBuildMode + " ROOT=\"" + gs_strRootFolder + "\"";
                _ThrowBaseExceptionIf((0 != ::system(strCommandLine.c_str())), "CRAP", nullptr);
                std::cout << "Done!" << std::endl;
            }
        }
        // If we get here, we are ready to publish include files and libraries
        // First we start with include files
        if (true == c_oCurrentBuildNode.IsElementPresent("HeaderFilesToPublish", INDEXED_BUFFER_VALUE_TYPE))
        {
            std::vector<std::string> stlListOfIncludeFilesToPublish = c_oCurrentBuildNode.GetStructuredBuffer("HeaderFilesToPublish").GetNamesOfElements();
            for (const std::string & c_strIncludeFileName: stlListOfIncludeFilesToPublish)
            {
                // Build up for source and destination filenames
                std::string strSourceFilename = c_oCurrentBuildNode.GetString("BuildNodeHostFolder") + "/Include/" + c_strIncludeFileName;
                std::string strDestinationFilename = gs_strRootFolder + "/Build/Include/" + c_strIncludeFileName;
                // Build the string for the copy operation
                std::string strCopyOperation = "cp -f -T " + strSourceFilename + " " + strDestinationFilename + " 2>/dev/null || :";
                ::system(strCopyOperation.c_str());
                // Now make sure the file is there
                _ThrowBaseExceptionIf((false == std::filesystem::exists(strDestinationFilename)), "UNEXPECTED ERROR: The include file %s failed to get published.", strDestinationFilename.c_str());
            }
        }
        // Now we publish the library files
        if (true == c_oCurrentBuildNode.IsElementPresent("LibrariesToPublish", INDEXED_BUFFER_VALUE_TYPE))
        {
            std::vector<std::string> stlListOfLibraryFilesToPublish = c_oCurrentBuildNode.GetStructuredBuffer("LibrariesToPublish").GetNamesOfElements();
            for (const std::string & c_strLibraryFileName: stlListOfLibraryFilesToPublish)
            {
                // Build up for source and destination filenames
                std::string strSourceFilename = gs_strRootFolder + "/Build/Binaries/" + c_strLibraryFileName;
                std::string strDestinationFilename = gs_strRootFolder + "/Build/Libraries/" + c_strLibraryFileName;
                // Build the string for the copy operation
                std::string strCopyOperation = "cp -f -T " + strSourceFilename + " " + strDestinationFilename + " 2>/dev/null || :";
                ::system(strCopyOperation.c_str());
                // Now make sure the file is there
                _ThrowBaseExceptionIf((false == std::filesystem::exists(strDestinationFilename)), "UNEXPECTED ERROR: The library file %s failed to get published.", strDestinationFilename.c_str());
            }
        }
    }
}

/********************************************************************************************/

static void __stdcall BuildAll(void)
{
    __DebugFunction();
    
    // To build all, we effectively just call BuildNode against all the elements in
    // gs_stlListOfNodes
    for (const auto & c_stlElement: gs_stlListOfNodes)
    {
        ::BuildNode(c_stlElement.second);
    }
}

/********************************************************************************************/

static std::vector<std::string> __stdcall SplitString(
    _in const std::string & c_strLineOfText,
    _in  char c_chSeparator
    )
{
    __DebugFunction();
    __DebugAssert(0 < c_strLineOfText.size());
    
    std::vector<std::string> strLinesOfSplitText;
    std::string::size_type stlPreviousPosition = 0, stlPosition = 0;
    while (std::string::npos != (stlPosition = c_strLineOfText.find(c_chSeparator, stlPosition)))
    {
        std::string stlSubstring(c_strLineOfText.substr(stlPreviousPosition, stlPosition-stlPreviousPosition));
        // Trim white spaces from the end of the string, just in case
        stlSubstring.erase(std::find_if(stlSubstring.rbegin(), stlSubstring.rend(), std::not1(std::ptr_fun<int, int>(std::isspace))).base(), stlSubstring.end());
        strLinesOfSplitText.push_back(stlSubstring);
        stlPreviousPosition = ++stlPosition;
    }
    std::string stlOtherSubstring = c_strLineOfText.substr(stlPreviousPosition, (stlPosition - stlPreviousPosition));
    // Trim white spaces from the end of the string, just in case
    stlOtherSubstring.erase(std::find_if(stlOtherSubstring.rbegin(), stlOtherSubstring.rend(), std::not1(std::ptr_fun<int, int>(std::isspace))).base(), stlOtherSubstring.end());
    strLinesOfSplitText.push_back(stlOtherSubstring);
    
    return strLinesOfSplitText;
}

/********************************************************************************************/

static StructuredBuffer __stdcall GetNode(
    _in const std::string & c_strCurrentFolder
    )
{
    __DebugFunction();
    __DebugAssert(0 < c_strCurrentFolder.size());
    
    StructuredBuffer oCurrentBuildNode;
    StructuredBuffer oCurrentBuildNodeDependencies;
    StructuredBuffer oCurrentBuildNodePublishIncludes;
    StructuredBuffer oCurrentBuildNodePublishLibraries;
    // Only get the node if the current folder contains a 'build.node' file, otherwise
    // return an empty StructuredBuffer object
    std::string strBuildNodeFilename = c_strCurrentFolder + "/build.node";
    if (true == std::filesystem::exists(strBuildNodeFilename))
    {
        oCurrentBuildNode.PutString("BuildNodeFullPathName", strBuildNodeFilename);
        oCurrentBuildNode.PutString("BuildNodeHostFolder", c_strCurrentFolder);
        // Open the file for reading text
        TextFileReader oTextFileReader(strBuildNodeFilename);
        while (false == oTextFileReader.EndOfFileReached())
        {
            // Get the next line of text from the text file
            std::string strLineOfText = oTextFileReader.Read();
            if (0 < strLineOfText.size())
            {
                // Now split the line of text. it should generate two elements only
                std::vector<std::string> stlLineElements{::SplitString(strLineOfText, '=')};
                _ThrowBaseExceptionIf((2 != stlLineElements.size()), "ERROR, unexpected build node line of text = %s in file %s", strLineOfText.c_str(), strBuildNodeFilename.c_str());
                if (::Get64BitHashOfNullTerminatedString("Identifier", false) == ::Get64BitHashOfNullTerminatedString(stlLineElements[0].c_str(), false))
                {
                    oCurrentBuildNode.PutGuid("Identifier", Guid(stlLineElements[1]));
                }
                else if (::Get64BitHashOfNullTerminatedString("Name", false) == ::Get64BitHashOfNullTerminatedString(stlLineElements[0].c_str(), false))
                {
                    oCurrentBuildNode.PutString("Name", stlLineElements[1]);
                }
                else if (::Get64BitHashOfNullTerminatedString("Os", false) == ::Get64BitHashOfNullTerminatedString(stlLineElements[0].c_str(), false))
                {
                    oCurrentBuildNode.PutString("Os", stlLineElements[1]);
                }
                else if (::Get64BitHashOfNullTerminatedString("Type", false) == ::Get64BitHashOfNullTerminatedString(stlLineElements[0].c_str(), false))
                {
                    oCurrentBuildNode.PutString("Type", stlLineElements[1]);
                }
                else if (::Get64BitHashOfNullTerminatedString("Dependency", false) == ::Get64BitHashOfNullTerminatedString(stlLineElements[0].c_str(), false))
                {
                    if (0 < stlLineElements[1].size())
                    {
                        oCurrentBuildNodeDependencies.PutBoolean(stlLineElements[1].c_str(), true);
                    }
                }
                else if (::Get64BitHashOfNullTerminatedString("PublishInclude", false) == ::Get64BitHashOfNullTerminatedString(stlLineElements[0].c_str(), false))
                {
                    if (0 < stlLineElements[1].size())
                    {
                        oCurrentBuildNodePublishIncludes.PutBoolean(stlLineElements[1].c_str(), true);
                    }
                }
                else if (::Get64BitHashOfNullTerminatedString("PublishLibrary", false) == ::Get64BitHashOfNullTerminatedString(stlLineElements[0].c_str(), false))
                {
                    if (0 < stlLineElements[1].size())
                    {
                        oCurrentBuildNodePublishLibraries.PutBoolean(stlLineElements[1].c_str(), true);
                    }
                }
                else
                {
                    _ThrowBaseException("ERROR: Unexpected specification %s found in file %s", strLineOfText, strBuildNodeFilename);
                }
            }
        }
        
        // See if we need to attach the oCurrentBuildNodeDependencies to the oCurrentBuildNode
        if (0 < oCurrentBuildNodeDependencies.GetNamesOfElements().size())
        {
            oCurrentBuildNode.PutStructuredBuffer("Dependencies", oCurrentBuildNodeDependencies);
        }
        
        // See if we need to attach the oCurrentBuildNodePublishIncludes to the oCurrentBuildNode
        if (0 < oCurrentBuildNodePublishIncludes.GetNamesOfElements().size())
        {
            oCurrentBuildNode.PutStructuredBuffer("HeaderFilesToPublish", oCurrentBuildNodePublishIncludes);
        }
        
        // See if we need to attach the oCurrentBuildNodePublishLibraries to the oCurrentBuildNode
        if (0 < oCurrentBuildNodePublishLibraries.GetNamesOfElements().size())
        {
            oCurrentBuildNode.PutStructuredBuffer("LibrariesToPublish", oCurrentBuildNodePublishLibraries);
        }
    }
    
    return oCurrentBuildNode;
}

/********************************************************************************************/

static void __stdcall LoadAllNodes(
    _in const std::string & c_strCurrentFolder
    )
{
    __DebugFunction();
    
    // First, we try and see if we can load a build node in the current foldder
    StructuredBuffer oCurrentBuildNode{::GetNode(c_strCurrentFolder)};
    if (true == oCurrentBuildNode.IsElementPresent("Identifier", GUID_VALUE_TYPE))
    {
        __DebugAssert(true == oCurrentBuildNode.IsElementPresent("Identifier", GUID_VALUE_TYPE));
        __DebugAssert(true == oCurrentBuildNode.IsElementPresent("BuildNodeFullPathName", ANSI_CHARACTER_STRING_VALUE_TYPE));
        __DebugAssert(true == oCurrentBuildNode.IsElementPresent("BuildNodeHostFolder", ANSI_CHARACTER_STRING_VALUE_TYPE));
        __DebugAssert(true == oCurrentBuildNode.IsElementPresent("Name", ANSI_CHARACTER_STRING_VALUE_TYPE));
        __DebugAssert(true == oCurrentBuildNode.IsElementPresent("Os", ANSI_CHARACTER_STRING_VALUE_TYPE));
        __DebugAssert(true == oCurrentBuildNode.IsElementPresent("Type", ANSI_CHARACTER_STRING_VALUE_TYPE));
        
        // Figure out the hash of the identifier of the node
        std::string strBuildNodeIdentifier = oCurrentBuildNode.GetGuid("Identifier").ToString(eHyphensOnly);
        Qword qwHashOfNodeIdentifier = ::Get64BitHashOfNullTerminatedString(strBuildNodeIdentifier.c_str(), false);
        _ThrowBaseExceptionIf((gs_stlListOfNodes.end() != gs_stlListOfNodes.find(qwHashOfNodeIdentifier)), "ERROR: Two build node files share the same identifiers (%s, %s)", oCurrentBuildNode.GetString("BuildNodeFullPathName").c_str(), gs_stlListOfNodes[qwHashOfNodeIdentifier].GetString("BuildNodeFullPathName").c_str());
        gs_stlListOfNodes[qwHashOfNodeIdentifier] = oCurrentBuildNode;
    }
    // Now we iterate through all of the parent folders and recurse into this function
    for (const auto & stlParentFolder: std::filesystem::directory_iterator(c_strCurrentFolder))
    {
        if (true == stlParentFolder.is_directory())
        {
            ::LoadAllNodes(stlParentFolder.path());
        }
    }
}
    
/********************************************************************************************/

static void __stdcall LoadBuildRootFile(
    _in const std::string & c_strRootFolder
    )
{
    __DebugFunction();
    
    std::string strBuildRootNodeFilename = c_strRootFolder + "/build.root";
    // Right now, there really isn't anything in the build.root file to load or parse
    _ThrowBaseExceptionIf((false == std::filesystem::exists(strBuildRootNodeFilename)), "ERROR: Build root file %s failed to load properly", strBuildRootNodeFilename.c_str());
    // Open the file for reading text
    TextFileReader oTextFileReader(strBuildRootNodeFilename);
    while (false == oTextFileReader.EndOfFileReached())
    {
        // Get the next line of text from the text file
        std::string strLineOfText = oTextFileReader.Read();
        if (0 < strLineOfText.size())
        {
            // Now split the line of text. it should generate two elements only
            std::vector<std::string> stlLineElements{::SplitString(strLineOfText, '=')};
            _ThrowBaseExceptionIf((2 != stlLineElements.size()), "ERROR, unexpected build node line of text = %s in file %s", strLineOfText.c_str(), strBuildRootNodeFilename.c_str());
            if (::Get64BitHashOfNullTerminatedString("Version", false) == ::Get64BitHashOfNullTerminatedString(stlLineElements[0].c_str(), false))
            {
                gs_strVersionString = stlLineElements[1];
            }
            else
            {
                _ThrowBaseException("ERROR: Unexpected specification %s found in file %s", strLineOfText, strBuildRootNodeFilename);
            }
        }
    }
    // Now we look into making sure the build folders are make
    std::string strBuildFolder = c_strRootFolder + "/Build";
    std::string strBinariesFolder = strBuildFolder + "/Binaries";
    std::string strIncludeFolder = strBuildFolder + "/Include";
    std::string strLibrariesFolder = strBuildFolder + "/Libraries";
    std::string strArtifactsFolder = strBuildFolder + "/Artifacts";
    
    if (false == std::filesystem::exists(strBuildFolder))
    {
        std::string strCommand = "mkdir " + strBuildFolder + " 2>/dev/null || :";
        ::system(strCommand.c_str());
    }
    _ThrowBaseExceptionIf((false == std::filesystem::exists(strBuildFolder)), "UNEXPECTED ERROR: The folder %s failed to be created.", strBuildFolder.c_str());
    if (false == std::filesystem::exists(strBinariesFolder))
    {
        std::string strCommand = "mkdir " + strBinariesFolder + " 2>/dev/null || :";
        ::system(strCommand.c_str());
    }
    _ThrowBaseExceptionIf((false == std::filesystem::exists(strBinariesFolder)), "UNEXPECTED ERROR: The folder %s failed to be created.", strBinariesFolder.c_str());
    if (false == std::filesystem::exists(strIncludeFolder))
    {
        std::string strCommand = "mkdir " + strIncludeFolder + " 2>/dev/null || :";
        ::system(strCommand.c_str());
    }
    _ThrowBaseExceptionIf((false == std::filesystem::exists(strIncludeFolder)), "UNEXPECTED ERROR: The folder %s failed to be created.", strIncludeFolder.c_str());
    if (false == std::filesystem::exists(strLibrariesFolder))
    {
        std::string strCommand = "mkdir " + strLibrariesFolder + " 2>/dev/null || :";
        ::system(strCommand.c_str());
    }
    _ThrowBaseExceptionIf((false == std::filesystem::exists(strLibrariesFolder)), "UNEXPECTED ERROR: The folder %s failed to be created.", strLibrariesFolder.c_str());
    if (false == std::filesystem::exists(strArtifactsFolder))
    {
        std::string strCommand = "mkdir " + strArtifactsFolder + " 2>/dev/null || :";
        ::system(strCommand.c_str());
    }
    _ThrowBaseExceptionIf((false == std::filesystem::exists(strArtifactsFolder)), "UNEXPECTED ERROR: The folder %s failed to be created.", strArtifactsFolder.c_str());
}

/********************************************************************************************/

static std::string __stdcall RemoveTrailingPathCharacter(
    _in const std::string & c_strFilesystemPath
    )
{
    __DebugFunction();
    
    std::string strFinalFilesystemPath = c_strFilesystemPath;
    // Trim white spaces from the end of the string, just in case
    strFinalFilesystemPath.erase(std::find_if(strFinalFilesystemPath.rbegin(), strFinalFilesystemPath.rend(), std::not1(std::ptr_fun<int, int>(std::isspace))).base(), strFinalFilesystemPath.end());
    // Now check the last character in the string. If it's a '/', erase it
    if ('/' == strFinalFilesystemPath.back())
    {
        strFinalFilesystemPath.erase(std::prev(strFinalFilesystemPath.end()));
    }
    
    return strFinalFilesystemPath;
}

/********************************************************************************************/

static std::string __stdcall FindBuildRootFolder(
    _in const std::string & c_strCurrentFolder
    )
{
    __DebugFunction();

    std::string strRootFolder;
    
    // First we look in the current folder to see if we can spot the 'build.node' file. If
    // so, we load it
    std::string strRootFolderFilename = c_strCurrentFolder + "/build.root";
    if (true == std::filesystem::exists(strRootFolderFilename))
    {
        ::LoadBuildRootFile(c_strCurrentFolder);
        strRootFolder = ::RemoveTrailingPathCharacter(c_strCurrentFolder);
    }
    else
    {
        // Since 'build.root' is not in the current folder, let's recurse into this function
        // by using the parent folder of the current folder. But we are going to fail if
        // the current folder is '/'
        _ThrowBaseExceptionIf(("/" == c_strCurrentFolder), "ERROR: Failed to find the build.root file. Operation failed.", nullptr);
        std::filesystem::path stlCurrentFolder{c_strCurrentFolder};
        std::string strParentFolder = stlCurrentFolder.parent_path().string();
        strRootFolder = ::FindBuildRootFolder(strParentFolder);
    }
    
    return strRootFolder;
}

/********************************************************************************************/

static std::string __stdcall GetCurrentFolder(void)
{
    __DebugFunction();
    
    // Get the current path
    std::string strCurrentFolder = std::filesystem::current_path().string();
    // One of the interesting side-effects of calling std::filesystem::current_path() is that
    // it puts quotation marks around the path. We need to remove that
    strCurrentFolder.erase(std::remove(strCurrentFolder.begin(), strCurrentFolder.end(), '\"'), strCurrentFolder.end());
    
    return ::RemoveTrailingPathCharacter(strCurrentFolder);
}

/********************************************************************************************/

int __cdecl main(
    _in int nNumberOfArguments,
    _in const char ** pszCommandLineArguments
    )
{
    __DebugFunction();

    // By default
    int nReturnValue = -1;
    
    try
    {
        std::cout << "+======================================================================================+" << std::endl;
        std::cout << "| BuildTool, Copyright (C) 2022 Secure AI Labs, Inc., All Rights Reserved.             |" << std::endl;
        std::cout << "| by Luis Miguel Huapaya                                                               |" << std::endl;
        std::cout << "+======================================================================================+" << std::endl;
        // Parse the command line arguments if any exist   
        StructuredBuffer oCommandLineArguments(ParseCommandLineParameters(nNumberOfArguments, pszCommandLineArguments));
        // Figure out the current folder
        gs_strCurrentFolder = ::GetCurrentFolder();
        // Let's figure out where the build root is
        gs_strRootFolder = ::FindBuildRootFolder(gs_strCurrentFolder);
        // Now do some quick checks to see if we want to print usage or just cleanall
        if (true == oCommandLineArguments.IsElementPresent("help", BOOLEAN_VALUE_TYPE))
        {
            ::PrintUsage();
        }
        else if (true == oCommandLineArguments.IsElementPresent("cleanall", BOOLEAN_VALUE_TYPE))
        {
            std::string strBuildFolder = gs_strRootFolder + "/Build";
            std::string strCommandLine = "rm -Rfd " + strBuildFolder + " 2>/dev/null || :";
            ::system(strCommandLine.c_str());
            _ThrowBaseExceptionIf((true == std::filesystem::exists(strBuildFolder)), "UNEXPECTED ERROR: The build folder %s failed to be removed.", strBuildFolder.c_str());
            std::cout << strBuildFolder << " and all subdirectories have been deleted." << std::endl;            
        }
        else
        {    
            std::cout << "Working Folder = " << gs_strCurrentFolder << std::endl;
            std::cout << "Root Folder = " << gs_strRootFolder << std::endl;
            // First thing we do is load up the current node in the current folder, IF it exists.
            // If it doesn't exist, then we will need a '-buildall' flag or else the build
            // fails
            StructuredBuffer oCurrentBuildNode(::GetNode(gs_strCurrentFolder));
            // Load the version number if available
            //::LoadVersionString(gs_strRootFolder);
            // Now that we know where the root is, load up all of the nodes in the build tree
            ::LoadAllNodes(gs_strRootFolder);
            std::cout << "Number of Nodes Loaded = " << std::to_string(gs_stlListOfNodes.size()) << std::endl << std::endl;
            // Do we just want to print the metadata of all the nodes
            if (true == oCommandLineArguments.IsElementPresent("printnodes", BOOLEAN_VALUE_TYPE))
            {
                // Print all the build node metadata
                for (const auto & c_stlElement: gs_stlListOfNodes)
                {
                    std::cout << "----------------------------------------------------------------------------------------" << std::endl;
                    std::cout << c_stlElement.second.ToString() << std::endl;
                }
            }
            else
            {
                // Now let's figure out if we are looking to clean things first
                if ((true == oCommandLineArguments.IsElementPresent("clean", BOOLEAN_VALUE_TYPE))||(true == oCommandLineArguments.IsElementPresent("cleanonly", BOOLEAN_VALUE_TYPE)))
                {
                    // Are we looking to clean only the stuff relating to building the current folder, or everything?
                    if (true == oCommandLineArguments.IsElementPresent("all", BOOLEAN_VALUE_TYPE))
                    {
                        // nReturnValue = 0 if no errors or warnings, -2 otherwise
                        ::CleanAll();
                        // If we get here, we were completely successful
                        nReturnValue = 0;
                    }
                    else if (true == oCommandLineArguments.IsElementPresent("this", BOOLEAN_VALUE_TYPE))
                    {
                        // There's a chance that the current folder didn't have a build.node file, in which_open_mode
                        // case, specifying 'this' does nothing.
                        if (false == oCurrentBuildNode.IsElementPresent("Identifier", GUID_VALUE_TYPE))
                        {
                            std::cout << "No build.node in current folder. Nothing to clean!" << std::endl;
                            nReturnValue = -2;
                        }
                        else
                        {
                            // nReturnValue = 0 if no errors or warnings, -2 otherwise
                            ::CleanNode(oCurrentBuildNode);
                            // If we get here, we were completely successful
                            nReturnValue = 0;
                        }
                    }
                }
                
                // Now let's figure out if we want to build. It 'cleanonly' is specified, the we are not looking to build
                if (false == oCommandLineArguments.IsElementPresent("cleanonly", BOOLEAN_VALUE_TYPE))
                {
                    // By default
                    nReturnValue = -1;
                    // Are we building everything or just the current folder? To determine, look
                    // for the boolean value "buildall" within the command line arguments
                    if (true == oCommandLineArguments.IsElementPresent("all", BOOLEAN_VALUE_TYPE))
                    {
                        // nReturnValue = 0 if no errors or warnings, -2 otherwise
                        ::BuildAll();
                        // If we get here, we were completely successful
                        nReturnValue = 0;
                    }
                    else if (true == oCommandLineArguments.IsElementPresent("this", BOOLEAN_VALUE_TYPE))
                    {
                        // There's a chance that the current folder didn't have a build.node file, in which_open_mode
                        // case, specifying 'this' does nothing.
                        if (false == oCurrentBuildNode.IsElementPresent("Identifier", GUID_VALUE_TYPE))
                        {
                            std::cout << "No build.node in current folder. Nothing to clean!" << std::endl;
                            nReturnValue = -2;
                        }
                        else
                        {
                            // nReturnValue = 0 if no errors or warnings, -2 otherwise
                            ::BuildNode(oCurrentBuildNode);
                            // If we get here, we were completely successful
                            nReturnValue = 0;
                        }
                    }
                }
            }
        }
    }
    
    catch (const BaseException & c_oBaseException)
    {
        // Detect to see if an exception was thrown because of a build error. If it
        // was, we do not want to register an exception, we just want to exit
        if (0 != ::StringCompare("CRAP", c_oBaseException.GetExceptionMessage(), true, 4))
        {
            ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        }
        else
        {
            std::cout << "BUILD ERROR ENCOUNTERED: Stopping." << std::endl;
        }
    }
    
    catch (const std::exception & c_oException)
    {
        ::RegisterStandardException(c_oException, __func__, __FILE__, __LINE__);
    }
    
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    
    // Print out any lingered exceptions before exiting
    while (0 < ::GetRegisteredExceptionsCount())
    {
        std::string strRegisteredException = ::GetNextRegisteredException();
        std::cout << strRegisteredException << std::endl << std::endl;
    }
    
    return nReturnValue;
}
