#pragma once
#include <iostream>
#include <filesystem>
#include <array>
#include <vector>
#include <cstring>

enum BuildType { eRoot, eNode };

std::string BoolToString(bool c_b);

char* StringToChar(std::string c_strString);

char* GetAbsolutePathFromRelativePath(std::string c_strRelativePath);

std::array<std::string,2> SplitFilenameFromAbsolutePath(std::string c_strAbsolutePathOfFile);

std::vector<std::array<std::string,2>> parseConfigFile(std::string c_strAbsolutePath);
