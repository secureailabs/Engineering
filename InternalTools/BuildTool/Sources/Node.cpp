#include<string>
#include<vector>
#include<iostream>
#include "Helper.h"
#include <fstream>
#include <map>
#include <algorithm>
#include <stdexcept>
#include <stdio.h>
#include "Utils.h"
#include "Node.h"
#include "Exceptions.h"
#include "JsonValue.h"


/********************************************************************************************/

__thiscall Node::Node(
    _in std::string c_strRelativePathOfNodeFile,
    _in std::vector<std::array<std::string, 2>> c_strRootConfigurations
    )
{
    m_strAbsolutePathOfNodeFile = GetAbsolutePathFromRelativePath(c_strRelativePathOfNodeFile);
    m_vecRootConfigurations = c_strRootConfigurations;
    ReadConfig();
}

/********************************************************************************************/

std::string __thiscall Node::toString(
    void
    )
{
    const std::string seperator = "\n====================================\n";
    return seperator + "NODE:\n\tLocation: " + 
    m_strAbsolutePathOfNodeFile + 
    "\n\tUUID: " + 
    m_strUUID + 
    "\n\tDEPENDENCIES: " + 
    DependenciesToString() + 
    "\n\tBUILT: " + 
    BoolToString(m_fBuilt) +
    seperator;
}

/********************************************************************************************/

std::string __thiscall Node::getUUID(
    void
    ){
    return m_strUUID;
}

/********************************************************************************************/

void __thiscall Node::Build(
    std::map<std::string, Node *> allAvailableNodes
    )
{
    SetEnvironmentVariables();
    if(!m_fBuilt){
        for(auto it = std::begin(m_stlDependencies_UUID); it != std::end(m_stlDependencies_UUID); ++it) {
            Node* dependency = allAvailableNodes.at(*it);
            dependency->Build(allAvailableNodes);
        }
        BuildFile(SplitFilenameFromAbsolutePath(m_strAbsolutePathOfNodeFile)[0]);
        m_fBuilt = true;
    }
}


/********************************************************************************************/

void __thiscall Node::BuildFile(
    _in std::string m_strAbsolutePathOfNodeFile
    )
{
    char buffer[128];
    std::string result = "";
    FILE* pipe = popen(StringToChar("make -C "+ m_strAbsolutePathOfNodeFile + " 2>&1"), "r");
    if (!pipe){
      throw std::runtime_error("popen() failed!");  
    } 
    try {
        while (fgets(buffer, sizeof buffer, pipe) != NULL) {
            result += buffer;
        }
    } catch (...) {
        pclose(pipe);
        throw;
    }
    pclose(pipe);
    std::string strUnEscapedJsonString = ::UnEscapeJsonString(PraseMakeOutputToJsonString(result));

    if(strUnEscapedJsonString != ""){
    try{

        std::vector<Byte> stlSerializedResponse = JsonValue::ParseDataToStructuredBuffer(strUnEscapedJsonString.c_str());
        StructuredBuffer oOutputBuffer(stlSerializedResponse);
        for (std::string strElement : oOutputBuffer.GetDescriptionOfElements())
        {
            std::cout << strElement << std::endl;
        }
        std::cout << "ERROR: ";
        std::cout <<   oOutputBuffer.GetString("message") << std::endl;

        
    } catch(BaseException oException){
        std::cout << oException.GetExceptionMessage() << std::endl;
        std::cout << oException.GetLineNumber() << std::endl;
        std::cout << oException.GetFilename() << std::endl;
    }
    }


}
/********************************************************************************************/

std::string __thiscall Node::PraseMakeOutputToJsonString(
    _in std::string c_strOriginalOutput
    )
{
    std::string parsedResult = "";
    std::string STARTDELIMITER = "{\"kind\":";
    std::string STOPDELIMITER = "\"}]\n";
    std::string STOPDELIMITER2 = "\"}\n";
    if (c_strOriginalOutput.find(STARTDELIMITER) != std::string::npos && c_strOriginalOutput.find(STOPDELIMITER)) {
        unsigned first = c_strOriginalOutput.find(STARTDELIMITER);
        unsigned last = c_strOriginalOutput.find(STOPDELIMITER);
        parsedResult = c_strOriginalOutput.substr(first,last-first) + STOPDELIMITER2;
    }
    return parsedResult;
}

/********************************************************************************************/

void __thiscall Node::ReadConfig(
    void
    )
{
    auto parsedConfigFile = parseConfigFile(m_strAbsolutePathOfNodeFile);
    for(auto it = std::begin(parsedConfigFile); it != std::end(parsedConfigFile); ++it) 
    {
        std::array<std::string,2 > configurationParamter = *it;
        std::string configurationName = configurationParamter[0];
        std::string configurationValue = configurationParamter[1];
        if(configurationName == "Identifier")
        {
            m_strUUID = configurationValue;
        } else if(configurationName == "Dependency")
        {
            AddDependencyUUID(configurationValue);
        }
    }
};

/********************************************************************************************/

void __thiscall Node::AddDependencyUUID(
    _in std::string c_strDependencyUUIDValue
    )
{
    m_stlDependencies_UUID.push_back(c_strDependencyUUIDValue);
}

/********************************************************************************************/

std::string __thiscall Node::DependenciesToString(
    void
    )
{
    std::string dependenciesString = "";
    for(auto it = std::begin(m_stlDependencies_UUID); it != std::end(m_stlDependencies_UUID); ++it) {
        if("" == dependenciesString){
            dependenciesString = *it;
        } else{
            dependenciesString= dependenciesString + ", " + *it;
        }
    }
    return dependenciesString;
}

/********************************************************************************************/

void __thiscall Node::SetEnvironmentVariables(
    void
    )
{
    for(auto it = std::begin(m_vecRootConfigurations); it != std::end(m_vecRootConfigurations); ++it) 
    {
        std::array<std::string,2 > configurationParamter = *it;
        std::string configurationName = configurationParamter[0];
        std::string configurationValue = configurationParamter[1];
        std::string commandToRun = "export " + configurationName + "=" + '"' + configurationValue + '"';
        system(StringToChar(commandToRun));
    }
}