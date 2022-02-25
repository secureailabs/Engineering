/*********************************************************************************************
 *
 * @file TextFileHandlers.h
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "CoreTypes.h"
#include "Object.h"

#include <fstream>
#include <string>
#include <vector>


//////////////////////////////////////////////////////////////////////////////////////////

class TextFileReader: public Object
{
    public:
    
        TextFileReader(
            _in const std::string & c_strTargetFilename
            );
        TextFileReader(
            _in const char * c_szTargetFilename
            );
        virtual ~TextFileReader(void);

        std::string __thiscall GetFilename(void) const throw();
        uint64_t __thiscall GetSizeInBytes(void) const throw();
        bool __thiscall EndOfFileReached(void) const throw();
        
        std::string __thiscall Read(void);

    private:
    
        // Private shared loading functions for the two constructors
        void __thiscall Load(void);
            
        // Private data members
        std::string m_strFilename;
        uint64_t m_un64SizeInBytes;
        mutable std::ifstream m_stlFileStream;
};