/*********************************************************************************************
 *
 * @file DatasetVersionReInitializer.cpp
 * @author Luis Miguel Huapaya
 * @date 23 March 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "BinaryFileHandlers.h"
#include "DatasetVersion.h"
#include "DatasetVersionReInitializer.h"
#include "DateAndTime.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"

#include <filesystem>
#include <iostream>

/********************************************************************************************/

DatasetVersionReInitializer::DatasetVersionReInitializer(
    _in const std::string & c_strDatasetVersionFilename
    )
{
    __DebugFunction();
    _ThrowBaseExceptionIf((false == std::filesystem::exists(c_strDatasetVersionFilename)), "ERROR: DatasetVersion file %s not found", c_strDatasetVersionFilename);

    DatasetVersion oDatasetVersion(c_strDatasetVersionFilename.c_str());
    m_strOriginalDatasetVersionFilename = c_strDatasetVersionFilename;
    m_oOriginalDatasetVersionMetadata = oDatasetVersion.GetSerializedDatasetVersionMetadata();
    m_oUpdatedDatasetVersionMetadata = oDatasetVersion.GetSerializedDatasetVersionMetadata();
}

/********************************************************************************************/

DatasetVersionReInitializer::~DatasetVersionReInitializer(void)
{
    __DebugFunction();
}

/********************************************************************************************/

void __thiscall DatasetVersionReInitializer::SetDatasetVersionIdentifier(
    _in const Guid & c_oDatasetVersionIdentifier
    )
{
    __DebugFunction();

    m_oUpdatedDatasetVersionMetadata.PutGuid("id", c_oDatasetVersionIdentifier);
}

/********************************************************************************************/

void __thiscall DatasetVersionReInitializer::SetCorporateIdentifier(
    _in const Guid & c_oCorporateIdentifier
    )
{
    __DebugFunction();

    m_oUpdatedDatasetVersionMetadata.PutGuid("organization_id", c_oCorporateIdentifier);
}

/********************************************************************************************/

void __thiscall DatasetVersionReInitializer::ResetUtcEpochPublishDate(void)
{
    __DebugFunction();

    m_oUpdatedDatasetVersionMetadata.PutUnsignedInt64("publish_date", ::GetEpochTimeInSeconds());
}

/********************************************************************************************/

void __thiscall DatasetVersionReInitializer::SetDatasetVersionName(
    _in const std::string c_strDatasetVersionTitle
    )
{
    __DebugFunction();

    m_oUpdatedDatasetVersionMetadata.PutString("name", c_strDatasetVersionTitle);
}

/********************************************************************************************/

void __thiscall DatasetVersionReInitializer::SetDatasetVersionDescription(
    _in const std::string c_strDatasetVersionDescription
    )
{
    __DebugFunction();

    m_oUpdatedDatasetVersionMetadata.PutString("description", c_strDatasetVersionDescription);
}

/********************************************************************************************/

void __thiscall DatasetVersionReInitializer::SetDatasetVersionKeywords(
    _in const std::string c_strDatasetVersionKeywords
    )
{
    __DebugFunction();

    m_oUpdatedDatasetVersionMetadata.PutString("keywords", c_strDatasetVersionKeywords);
}

/********************************************************************************************/

void __thiscall DatasetVersionReInitializer::SetDatasetFamily(
    _in const std::string c_strDatasetFamily
    )
{
    __DebugFunction();

    m_oUpdatedDatasetVersionMetadata.PutString("dataset_id", c_strDatasetFamily);
}

/********************************************************************************************/

void __thiscall DatasetVersionReInitializer::RemoveDatasetFamily(void)
{
    __DebugFunction();

    m_oUpdatedDatasetVersionMetadata.RemoveElement("dataset_id");
}

/********************************************************************************************/

Guid __thiscall DatasetVersionReInitializer::GetDatasetVersionIdentifier(void) const
{
    __DebugFunction();

    return m_oUpdatedDatasetVersionMetadata.GetGuid("id");
}

/********************************************************************************************/

std::vector<Byte> __thiscall DatasetVersionReInitializer::GetSerializedDatasetVersionMetadata(void) const
{
    __DebugFunction();

    return m_oUpdatedDatasetVersionMetadata.GetSerializedBuffer();
}

/********************************************************************************************/

void __thiscall DatasetVersionReInitializer::SaveDatasetVersionUpdates(void) const
{
    __DebugFunction();

    // This is a complex operation. We will:
    // 1. Write the updated dataset metadata to a new dataset file with a temp filename
    // 2. Figure out the offset of the first table in the original dataset file
    // 3. Copy the tables from the original dataset file to the new dataset file. Do this in
    //    chunks
    // 4. Close the new dataset file.
    // 5. Delete the original dataset file.
    // 6. Rename the new dataset file to the name of the old dataset file.

    // Serialize the updated dataset metadata
    std::vector<Byte> stlSerializedUpdatedDatasetVersionMetadata{m_oUpdatedDatasetVersionMetadata.GetSerializedBuffer()};
    // Select a temporary filename for the new dataset file
    Guid oNewGuid;
    std::string strTemporaryDatasetVersionFilename = oNewGuid.ToString(eHyphensOnly) + ".csvp";
    // Figure out the starting offset in the original file
    unsigned int unSerializedOriginalDatasetVersionSizeInBytes = m_oOriginalDatasetVersionMetadata.GetSerializedBuffer().size();
    unsigned int unStartingTableDataOffsetInSourceFile = 12 + unSerializedOriginalDatasetVersionSizeInBytes;
    // Let's put the following code in a nested scope so that the BinaryFileReader
    // and BinaryFileWriter can close their underlying file handlers when the stack
    // unwinds. We need to do this in order to be able to turn around and rename the
    // file and delete the file, etc...
    {
        // Open the original file for reading and set the starting offset where the
        // table data starts
        BinaryFileReader oSourceFile(m_strOriginalDatasetVersionFilename);
        oSourceFile.Seek(eFromBeginningOfFile, unStartingTableDataOffsetInSourceFile);
        // Open the destination file for writing
        BinaryFileWriter oDestinationFile(strTemporaryDatasetVersionFilename);
        // Add a marker at the beginning of the destination file.
        Qword qwFileMarker = 0xEE094CBA1B48A123;
        oDestinationFile.Write((const void *) &qwFileMarker, sizeof(qwFileMarker));
        // Now we write the dataset metadata size in bytes to file
        unsigned int unSerializedDatasetVersionMetadataBufferSizeInBytes = stlSerializedUpdatedDatasetVersionMetadata.size();
        oDestinationFile.Write((const void *) &unSerializedDatasetVersionMetadataBufferSizeInBytes, sizeof(unSerializedDatasetVersionMetadataBufferSizeInBytes));
        // Now we write the updated dataset metadata to file
        oDestinationFile.Write(stlSerializedUpdatedDatasetVersionMetadata);
        // At this point, we will loop in 256 Mb chunks and copy the source file table
        // data to the destination file
        unsigned int unAmountOfDataToCopyInBytes = oSourceFile.GetSizeInBytes() - (sizeof(uint64_t) + sizeof(unsigned int) + unSerializedOriginalDatasetVersionSizeInBytes);
        while (0 < unAmountOfDataToCopyInBytes)
        {
            unsigned int unMaxChunkSizeInBytes = (256*1024*1024);
            unsigned int unChunkSizeInBytes = (unAmountOfDataToCopyInBytes < unMaxChunkSizeInBytes) ? unAmountOfDataToCopyInBytes : unMaxChunkSizeInBytes;
            std::vector<Byte> stlChunkOfDataToCopy = oSourceFile.Read(unChunkSizeInBytes);
            oDestinationFile.Write(stlChunkOfDataToCopy);
            unAmountOfDataToCopyInBytes -= unChunkSizeInBytes;
        }
        // Eventually, we will persist a digital signature here at the end of the file.
    }
    // Now, delete the original file
    std::filesystem::remove(m_strOriginalDatasetVersionFilename);
    // Rename the new dataset file to the old dataset file
    std::filesystem::rename(strTemporaryDatasetVersionFilename, m_strOriginalDatasetVersionFilename);
}
