/*********************************************************************************************
 *
 * @file BinaryFileReader.h
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

typedef enum
{
    eFromBeginningOfFile = 0,
    eFromCurrentPositionInFile = 1,
    eFromEndOfFile = 2
}
FileOffsetType;

//////////////////////////////////////////////////////////////////////////////////////////

class BinaryFileReader: public Object
{
    public:
    
        BinaryFileReader(
            _in const std::string & c_strTargetFilename
            );
        BinaryFileReader(
            _in const char * c_szTargetFilename
            );
        virtual ~BinaryFileReader(void);

        std::string __thiscall GetFilename(void) const throw();
        uint64_t __thiscall GetSizeInBytes(void) const throw();
        uint64_t __thiscall GetFilePointer(void) const throw();
        
        void __thiscall Seek(
            _in FileOffsetType eFileOffsetType,
            _in uint64_t un64OffsetInBytes
            );
            
        void __thiscall Read(
            _in void * pDestinationBuffer,
            _in uint64_t un64NumberOfBytesToRead
            );
        std::vector<Byte> __thiscall Read(
            _in uint64_t un64NumberOfBytesToRead
            );

    private:
    
        // Private shared loading functions for the two constructors
        void __thiscall Load(void);
            
        // Private data members
        std::string m_strFilename;
        uint64_t m_un64SizeInBytes;
        mutable std::ifstream m_stlFileStream;
        std::streampos m_stlStartingPosition;
};

//////////////////////////////////////////////////////////////////////////////////////////

class BinaryFileWriter: public Object
{
    public:
    
        BinaryFileWriter(
            _in const std::string & c_strTargetFilename
            );
        BinaryFileWriter(
            _in const char * c_szTargetFilename
            );
        virtual ~BinaryFileWriter(void);
        
        std::string __thiscall GetFilename(void) const throw();
        uint64_t __thiscall GetSizeInBytes(void) const throw();
        uint64_t __thiscall GetFilePointer(void) const throw();
        
        void __thiscall Seek(
            _in FileOffsetType eFileOffsetType,
            _in uint64_t un64OffsetInBytes
            );
            
        void __thiscall Write(
            _in const void * c_pSourceBuffer,
            _in uint64_t un64NumberOfBytesToWrite
            );
        void __thiscall Write(
            _in const std::vector<Byte> & c_pSourceBuffer
            );
            
    private:
    
        // Private shared loading functions for the two constructors
        void __thiscall Load(void);
            
        // Private data members
        std::string m_strFilename;
        uint64_t m_un64SizeInBytes;
        mutable std::ofstream m_stlFileStream;
        std::streampos m_stlStartingPosition;
};