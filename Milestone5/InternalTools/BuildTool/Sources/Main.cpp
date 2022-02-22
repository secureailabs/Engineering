#include <iostream>
#include <CoreTypes.h>
#include <filesystem>
#include <map>

#include "Helper.h"
#include "Node.h"
#include "CommandLine.h"
#include "DebugLibrary.h"

namespace fs = std::filesystem;

static std::map<std::string, Node *> gs_mapAllAvailableNodes;
bool gs_boolBuildAllNodes;
static std::string gs_strSingleNodeToBuildUUID;
static std::string gs_strRegularNodeName = "build.node";
static std::string gs_strRootNodeName = "build.root";
static std::vector<std::array<std::string, 2>> gs_vecRootConfigurations;

/********************************************************************************************/

static bool __thiscall CheckBuild(
   _in const std::string c_strAbsoluteNodePath,
   _in const BuildType type
   )
   // Simple function to check if the node is either a regular node or a root node
{
    __DebugFunction();
    __DebugAssert(c_strAbsoluteNodePath != "");
   //  __DebugAssert(type != type);

   switch(type){
      case eRoot:
         return SplitFilenameFromAbsolutePath(c_strAbsoluteNodePath)[1] == gs_strRootNodeName;
      case eNode:
         return SplitFilenameFromAbsolutePath(c_strAbsoluteNodePath)[1] == gs_strRegularNodeName;
   }
}

/********************************************************************************************/

static void __thiscall SetSingleNodetoBuildUUID(
   void
   )
{
    __DebugFunction();

    auto parsedConfigFile = parseConfigFile("./" + gs_strRegularNodeName);
    for(auto it = std::begin(parsedConfigFile); it != std::end(parsedConfigFile); ++it) 
    {
        std::array<std::string,2 > configurationParamter = *it;
        std::string configurationName = configurationParamter[0];
        std::string configurationValue = configurationParamter[1];
        if(configurationName == "Identifier")
        {
            gs_strSingleNodeToBuildUUID = configurationValue;
        }
    }
}

/********************************************************************************************/

static void __thiscall PrintAllNodes(
   void
   )
{
    __DebugFunction();

   for (auto const& x : gs_mapAllAvailableNodes)
   {
      std::string key = x.first;
      Node * val = x.second;
      std::cout << val->toString() << std::endl;
   }
}

/********************************************************************************************/

static void __thiscall BuildNodes(
   void
)
{
    __DebugFunction();

   if(gs_boolBuildAllNodes)
   // Check if buildAllNodes have been specified. If so, iterate through
   // the map and build all of the nodes
   {
      for (auto const& x : gs_mapAllAvailableNodes)
      {
         Node * p_Node = x.second;
         p_Node->Build(gs_mapAllAvailableNodes);
      }
   }
   else
   // Build all nodes has not been specified. Thus, we utilize the global variable
   // gs_strSingleNodeToBuildUUID as an index to only build that node and it's dependencies
   {
      Node * p_Node = gs_mapAllAvailableNodes.at(gs_strSingleNodeToBuildUUID);
      p_Node->Build(gs_mapAllAvailableNodes);
   }
   PrintAllNodes();

}

/********************************************************************************************/

static void __thiscall NodeFinder(
   _in std::string c_strRootPath
   )
{

    __DebugFunction();

   for (const auto& directoryEntry : fs::recursive_directory_iterator(c_strRootPath)){
      if(gs_strRegularNodeName == SplitFilenameFromAbsolutePath(directoryEntry.path())[1]){
         Node* newNode = new Node(directoryEntry.path(), gs_vecRootConfigurations);
         gs_mapAllAvailableNodes.insert(std::pair<std::string,Node*>(newNode->getUUID(), newNode));
      }  
   }
   PrintAllNodes();
   BuildNodes();
}

/********************************************************************************************/

static void __thiscall ParseRoot(
   _in std::string c_strAbsolutePathOfRootFile
   )
{
    gs_vecRootConfigurations = parseConfigFile(c_strAbsolutePathOfRootFile + "/build.root");
};

/********************************************************************************************/

static std::string __thiscall FindRoot(
   _in std::string c_strCurrentDirectory
   )
{
    __DebugFunction();

   for (const auto & entry : fs::directory_iterator(c_strCurrentDirectory))
   {
      std::string absolutePath = GetAbsolutePathFromRelativePath(entry.path());
      if(CheckBuild(absolutePath, eRoot))
      {
         return SplitFilenameFromAbsolutePath(absolutePath)[0];
      }
   }
   return FindRoot("../"+c_strCurrentDirectory);
};

/********************************************************************************************/

int __cdecl main(
    _in int nNumberOfArguments,
    _in const char ** pszCommandLineArguments
    )
{
   if(nNumberOfArguments > 1){
      gs_boolBuildAllNodes = ParseCommandLineParameters(nNumberOfArguments,pszCommandLineArguments).GetBoolean("all-nodes");
   }
   if(!gs_boolBuildAllNodes){
      SetSingleNodetoBuildUUID();
   }
   std::string rootPath = FindRoot("./");
   ParseRoot(rootPath);
   NodeFinder(rootPath);
   return 1;
};
