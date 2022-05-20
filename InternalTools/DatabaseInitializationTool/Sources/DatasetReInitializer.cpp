/*********************************************************************************************
 *
 * @file DatasetReInitializer.cpp
 * @author Luis Miguel Huapaya
 * @date 23 March 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include "BinaryFileHandlers.h"
#include "Dataset.h"
#include "DatasetReInitializer.h"
#include "DateAndTime.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"

#include <filesystem>
#include <iostream>

/********************************************************************************************/

DatasetReInitializer::DatasetReInitializer(
    _in const std::string & c_strDatasetFilename
    )
{
    __DebugFunction();
    _ThrowBaseExceptionIf((false == std::filesystem::exists(c_strDatasetFilename)), "ERROR: Dataset file %s not found", c_strDatasetFilename);

    Dataset oDataset(c_strDatasetFilename.c_str());
    m_strOriginalDatasetFilename = c_strDatasetFilename;
    m_oOriginalDatasetMetadata = oDataset.GetSerializedDatasetMetadata();
    m_oUpdatedDatasetMetadata = oDataset.GetSerializedDatasetMetadata();
}

/********************************************************************************************/

DatasetReInitializer::~DatasetReInitializer(void)
{
    __DebugFunction();
}

/********************************************************************************************/

void __thiscall DatasetReInitializer::SetDatasetIdentifier(
    _in const Guid & c_oDatasetIdentifier
    )
{
    __DebugFunction();

    m_oUpdatedDatasetMetadata.PutGuid("DatasetGuid", c_oDatasetIdentifier);
}

/********************************************************************************************/

void __thiscall DatasetReInitializer::SetCorporateIdentifier(
    _in const Guid & c_oCorporateIdentifier
    )
{
    __DebugFunction();

    m_oUpdatedDatasetMetadata.PutGuid("OrganizationGuid", c_oCorporateIdentifier);
}

/********************************************************************************************/

void __thiscall DatasetReInitializer::ResetUtcEpochPublishDate(void)
{
    __DebugFunction();

    m_oUpdatedDatasetMetadata.PutUnsignedInt64("PublishDate", ::GetEpochTimeInSeconds());
}

/********************************************************************************************/

void __thiscall DatasetReInitializer::SetDatasetTitle(
    _in const std::string c_strDatasetTitle
    )
{
    __DebugFunction();

    m_oUpdatedDatasetMetadata.PutString("Title", c_strDatasetTitle);
}

/********************************************************************************************/

void __thiscall DatasetReInitializer::SetDatasetDescription(
    _in const std::string c_strDatasetDescription
    )
{
    __DebugFunction();

    m_oUpdatedDatasetMetadata.PutString("Description", c_strDatasetDescription);
}

/********************************************************************************************/

void __thiscall DatasetReInitializer::SetDatasetKeywords(
    _in const std::string c_strDatasetKeywords
    )
{
    __DebugFunction();

    m_oUpdatedDatasetMetadata.PutString("Tags", c_strDatasetKeywords);
}

/********************************************************************************************/

void __thiscall DatasetReInitializer::SetDatasetFamily(
    _in const std::string c_strDatasetFamily
    )
{
    __DebugFunction();

    m_oUpdatedDatasetMetadata.PutString("DataFamilyIdentifier", c_strDatasetFamily);
}

/********************************************************************************************/

void __thiscall DatasetReInitializer::RemoveDatasetFamily(void)
{
    __DebugFunction();

    m_oUpdatedDatasetMetadata.RemoveElement("DataFamilyIdentifier");
}

/********************************************************************************************/

Guid __thiscall DatasetReInitializer::GetDatasetIdentifier(void) const
{
    __DebugFunction();

    return m_oUpdatedDatasetMetadata.GetGuid("DatasetGuid");
}

/********************************************************************************************/

std::vector<Byte> __thiscall DatasetReInitializer::GetSerializedDatasetMetadata(void) const
{
    __DebugFunction();

    return m_oUpdatedDatasetMetadata.GetSerializedBuffer();
}

/********************************************************************************************/

void __thiscall DatasetReInitializer::SaveDatasetUpdates(void) const
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
    std::vector<Byte> stlSerializedUpdatedDatasetMetadata{m_oUpdatedDatasetMetadata.GetSerializedBuffer()};
    // Select a temporary filename for the new dataset file
    Guid oNewGuid;
    std::string strTemporaryDatasetFilename = oNewGuid.ToString(eHyphensAndCurlyBraces) + ".csvp";
    // Figure out the starting offset in the original file
    unsigned int unSerializedOriginalDatasetSizeInBytes = m_oOriginalDatasetMetadata.GetSerializedBuffer().size();
    unsigned int unStartingTableDataOffsetInSourceFile = 12 + unSerializedOriginalDatasetSizeInBytes;
    // Let's put the following code in a nested scope so that the BinaryFileReader
    // and BinaryFileWriter can close their underlying file handlers when the stack
    // unwinds. We need to do this in order to be able to turn around and rename the
    // file and delete the file, etc...
    {
        // Open the original file for reading and set the starting offset where the
        // table data starts
        BinaryFileReader oSourceFile(m_strOriginalDatasetFilename);
        oSourceFile.Seek(eFromBeginningOfFile, unStartingTableDataOffsetInSourceFile);
        // Open the destination file for writing
        BinaryFileWriter oDestinationFile(strTemporaryDatasetFilename);
        // Add a marker at the beginning of the destination file.
        Qword qwFileMarker = 0xEE094CBA1B48A123;
        oDestinationFile.Write((const void *) &qwFileMarker, sizeof(qwFileMarker));
        // Now we write the dataset metadata size in bytes to file
        unsigned int unSerializedDatasetMetadataBufferSizeInBytes = stlSerializedUpdatedDatasetMetadata.size();
        oDestinationFile.Write((const void *) &unSerializedDatasetMetadataBufferSizeInBytes, sizeof(unSerializedDatasetMetadataBufferSizeInBytes));
        // Now we write the updated dataset metadata to file
        oDestinationFile.Write(stlSerializedUpdatedDatasetMetadata);
        // At this point, we will loop in 256 Mb chunks and copy the source file table
        // data to the destination file
        unsigned int unAmountOfDataToCopyInBytes = oSourceFile.GetSizeInBytes() - (sizeof(uint64_t) + sizeof(unsigned int) + unSerializedOriginalDatasetSizeInBytes);
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
    std::filesystem::remove(m_strOriginalDatasetFilename);
    // Rename the new dataset file to the old dataset file
    std::filesystem::rename(strTemporaryDatasetFilename, m_strOriginalDatasetFilename);
}
