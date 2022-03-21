#include <iostream>
#include <filesystem>
#include <array>
#include <cstring>
#include <CoreTypes.h>
#include <vector>
#include <stdio.h>
#include <fstream>
#include <stdexcept>
#include <algorithm>
#include "Helper.h"
namespace fs = std::filesystem;

/********************************************************************************************/

std::vector<std::array<std::string,2>> parseConfigFile(
      _in std::string c_strAbsolutePath
      )
{
    std::vector<std::array<std::string,2>>  parsedConfigFile;
    std::ifstream cFile (c_strAbsolutePath);
    if (cFile.is_open())
    {
        std::string line;
        while(getline(cFile, line)){
            line.erase(std::remove_if(line.begin(), line.end(), isspace), line.end());
            if('#' == line[0]  || line.empty()){
                continue;
            }
            auto delimiterPos = line.find("=");
            auto name = line.substr(0, delimiterPos);
            auto value = line.substr(delimiterPos + 1);
            parsedConfigFile.push_back({name, value});
        }            
    } else {
        std::cerr << "Couldn't open config file for reading.\n";
    } 
    return parsedConfigFile;
}

/********************************************************************************************/
// Prints true or false depending on the value boolean value 
std::string __thiscall BoolToString(
      _in const bool c_b
      )
{
  return c_b ? "true" : "false";
}

/********************************************************************************************/

// Function to return a char * based on the value of a string
char* __thiscall StringToChar(
      _in const std::string c_strString
      )
{
      char * newValue = new char [c_strString.length()+1];
      strcpy (newValue, c_strString.c_str());
      return newValue;
}

/********************************************************************************************/

// Function to return the absolute path from a relative path
char* __thiscall GetAbsolutePathFromRelativePath(
      _in const std::string c_strRelativePath
      )
{
      char* absolutePath = realpath(StringToChar(c_strRelativePath), NULL);
      return absolutePath;
}

/********************************************************************************************/


std::array<std::string,2> __thiscall SplitFilenameFromAbsolutePath(
      _in const std::string c_strAbsolutePathOfFile
      )
{
   std::array<std::string,2> path_array;
   path_array[0] = fs::path(c_strAbsolutePathOfFile).parent_path();
   path_array[1] = fs::path(c_strAbsolutePathOfFile).filename();
   return path_array;
};
