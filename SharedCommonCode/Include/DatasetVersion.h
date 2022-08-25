/*********************************************************************************************
 *
 * @file DatasetVersion.h
 * @author Luis Miguel Huapaya
 * @date 30 Sep 2020
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2020 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "CoreTypes.h"
#include "Object.h"
#include "StructuredBuffer.h"

#include <map>
#include <string>
#include <vector>

//////////////////////////////////////////////////////////////////////////////////////////

class DatasetVersionTableColumn: public Object
{
    public:
    
        DatasetVersionTableColumn(
            _in const std::vector<Byte> & c_stlSerializedColumnMetadataBuffer
            );
        virtual ~DatasetVersionTableColumn(void);
        
        std::string __thiscall GetColumnIdentifier(void) const throw();
        std::string __thiscall GetTitle(void) const throw();
        std::string __thiscall GetDescription(void) const throw();
        std::string __thiscall GetTags(void) const throw();
        std::string __thiscall GetUnits(void) const throw();
        std::string __thiscall GetType(void) const throw();
        std::string __thiscall GetUnitCategories(void) const;
        
    private:
    
        StructuredBuffer m_oDatasetVersionTableColumnMetadata;
};

//////////////////////////////////////////////////////////////////////////////////////////

class DatasetVersionTable: public Object
{
    public:
    
        DatasetVersionTable(
            _in const std::string & c_strFilename,
            _in const std::vector<Byte> & c_stlSerializedTableMetadataBuffer,
            _in uint64_t un64OffsetInBytesToTableDataInFile
            );
        virtual ~DatasetVersionTable(void);
        
        std::string __thiscall GetTableIdentifier(void) const throw();
        std::string __thiscall GetTitle(void) const throw();
        std::string __thiscall GetDescription(void) const throw();
        std::string __thiscall GetTags(void) const throw();
        uint64_t __thiscall GetRowCount(void) const throw();
        unsigned int __thiscall GetColumnCount(void) const throw();
        std::vector<std::string> __thiscall GetColumnIdentifiers(void) const throw();
        DatasetVersionTableColumn __thiscall GetTableColumn(
            _in const char * c_szColumnIdentifier
            ) const;
        StructuredBuffer __thiscall GetInformationForDataAccess(void) const throw();
        
    private:
    
        std::string m_strFilename;
        StructuredBuffer m_oTableMetadata;
        std::vector<std::string> m_stlColumnIdentifiers;
        std::map<Qword, unsigned int> m_stlColumnIndexByIdentifier;
        uint64_t m_un64OffsetInBytesToTableDataInFile;
};

//////////////////////////////////////////////////////////////////////////////////////////

class DatasetVersion : public Object
{
    public:

        DatasetVersion(
            _in const char * c_szFullFilename
            );
        DatasetVersion(
            _in const std::vector<Byte> & c_stlSerializedMetadata
            );
        virtual ~DatasetVersion(void) throw();

        std::string __thiscall GetDatasetVersionIdentifier(void) const throw();
        std::string __thiscall GetDatasetIdentifier(void) const throw();
        std::string __thiscall GetPublisherIdentifier(void) const throw();
        std::string __thiscall GetTitle(void) const throw();
        std::string __thiscall GetDescription(void) const throw();
        std::string __thiscall GetKeywords(void) const throw();
        uint64_t __thiscall GetPublishDate(void) const throw();
        unsigned int __thiscall GetNumberOfTables(void) const throw();
        std::vector<std::string> __thiscall GetTableIdentifiers(void) const throw();
        DatasetVersionTable __thiscall GetDatasetVersionTable(
            _in const char * c_szTableIdentifier
            ) const;

        std::vector<Byte> __thiscall GetSerializedDatasetVersionMetadata(void) const throw();
        
    private:

        // Variable used to track whether or not this object instance is just metadata or
        // is the full file (i.e. metadata + data)
        bool m_fIsMetadataOnly;
        // Name of the file containing the dataset
        std::string m_strFilename;
        // StructuredBuffer containing the metadata for the datasets, all of the tables and all of the columns
        StructuredBuffer m_oDatasetVersionMetadata;
        // List of all of the table identifiers found in the file
        std::unordered_map<std::string, int> m_stlMapOfTableIdentifiers;
        // List of all the offsets into the file which point to the 'table marker' (64 bit value making the start of a table data)
        std::map<Qword, uint64_t> m_stlListOfTableMarkerOffsets;
};
