/*********************************************************************************************
 *
 * @file PluginVersion.h
 * @author Shabana Akhtar Baig
 * @date 27 Oct 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 * A plugins version will be represented in the following format:
 *
 *      majorVersionNumberminorVersionNumber
 *
 * If needed, more version numbers can be appended to the format.
 ********************************************************************************************/

#pragma once

#include "DebugLibrary.h"
#include "Exceptions.h"
#include "Object.h"

#include <iostream>
#include <vector>
#include <string>

/********************************************************************************************/

class PluginVersion : public Object
{
    public:

        // Constructors and Destructor
        PluginVersion(void);
        PluginVersion(
            _in Qword qwVersionNumber
            );
        virtual ~PluginVersion(void) throw();

        // Get the plugin version in string format
        std::string __thiscall ToString(void) const throw();

        bool __thiscall RoundDown(
            _in PluginVersion const & c_oPluginVersion
            ) const throw();

        // Operator overloads
        bool __thiscall operator < (
            _in PluginVersion const & c_oPluginVersion
            ) const throw();
        bool __thiscall operator > (
            _in PluginVersion const & c_oPluginVersion
            ) const throw();
        bool __thiscall operator == (
            _in PluginVersion const & c_oPluginVersion
            ) const throw();
        bool __thiscall operator != (
            _in PluginVersion const & c_oPluginVersion
            ) const throw();

    private:

        // Private data members
        Dword m_unMajor, m_unMinor;
};
