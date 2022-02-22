#pragma once
#include<string>
#include<vector>
#include<array>
#include<iostream>
#include "Helper.h"
#include <fstream>
#include <map>
#include <algorithm>
#include <stdexcept>
#include <stdio.h>
#include <Object.h>


class Node : public Object
{
    public:
        __thiscall Node(
            std::string relativeNodePath,
            std::vector<std::array<std::string, 2>> rootConfigurations
            );
        std::string __thiscall toString(
            void
            );
        void __thiscall Build(
            std::map<std::string, Node *> allAvailableNodes 
            );
        std::string __thiscall getUUID(
            void
            );
    private:
        std::string m_strAbsolutePathOfNodeFile;
        std::string m_strUUID;
        std::vector<std::string> m_stlDependencies_UUID;
        std::vector<std::array<std::string, 2>> m_vecRootConfigurations;
        bool m_fBuilt = false;
        void __thiscall BuildFile(
            std::string m_strAbsolutePathOfNodeFile
            );
        std::string __thiscall PraseMakeOutputToJsonString(
            std::string c_strOriginalOutput
            );
        void __thiscall ReadConfig(
            void
            );
        void __thiscall AddDependencyUUID(
            std::string dependency
            );
        std::string __thiscall DependenciesToString(
            void
        );
        void __thiscall SetEnvironmentVariables(
            void
        );
};
