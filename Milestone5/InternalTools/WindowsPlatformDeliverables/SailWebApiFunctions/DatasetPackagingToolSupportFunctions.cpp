#include <Windows.h>

#include "64BitHashes.h"
#include "CompressionHelperFunctions.h"
#include "DateAndTime.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "StructuredBuffer.h"
#include "JsonValue.h"
#include "SailApiBaseServices.h"
#include "SharedUtilityFunctions.h"

#include <map>
#include <vector>

// Global variables used when writing a table to file
static std::string gs_strTargetTablePackageFilename;
static std::vector<Byte> gs_stlTablePackageRecordsBuffer;
static Byte * gs_pbWriteTarget = nullptr;
static uint64_t gs_un64TotalSizeWritten;
// Global variables used to store column metadata
static std::map<unsigned int, StructuredBuffer *> gs_stlColumnProperties;
// Global variables used for storing table metadata when reading from file
static std::string gs_strDatasetFilename;
static unsigned int gs_unTableIndex = 0;
static std::map<unsigned int, StructuredBuffer *> gs_ImportedTableMetadata;
static std::map<unsigned int, std::string> gs_ImportedTableFilename;

/// <summary>
/// 
/// </summary>
/// <param name="c_szTargetFilename"></param>
/// <param name="un64TargetFileSizeInBytes"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) void __cdecl OpenTablePackageFileForWriting(
    _in const char * c_szTargetFilename,
    _in uint64_t un64TargetFileSizeInBytes
    )
{
    __DebugFunction();

    try
    {
        gs_strTargetTablePackageFilename = c_szTargetFilename;
        gs_stlTablePackageRecordsBuffer.resize((size_t) (un64TargetFileSizeInBytes * 1.3));
        gs_pbWriteTarget = (Byte *) gs_stlTablePackageRecordsBuffer.data();
        gs_un64TotalSizeWritten = 0;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szRawRecord"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) void __cdecl AddColumnToTablePackageFile(
    _in const char * c_szColumnIdentifier,
    _in const char * c_szColumnName,
    _in const char * c_szColumnDescription,
    _in const char * c_szColumnTags,
    _in const char * c_szColumnUnits,
    _in const char * c_szColumnType,
    _in const char * c_szColumnUnitCategories
    )
{
    __DebugFunction();

    try
    {
        unsigned int unColumnIndex = (unsigned int) gs_stlColumnProperties.size();
        gs_stlColumnProperties[unColumnIndex] = new StructuredBuffer();
        gs_stlColumnProperties[unColumnIndex]->PutString("Identifier", c_szColumnIdentifier);
        gs_stlColumnProperties[unColumnIndex]->PutString("Name", c_szColumnName);
        gs_stlColumnProperties[unColumnIndex]->PutString("Description", c_szColumnDescription);
        gs_stlColumnProperties[unColumnIndex]->PutString("Tags", c_szColumnTags);
        gs_stlColumnProperties[unColumnIndex]->PutString("Units", c_szColumnUnits);
        gs_stlColumnProperties[unColumnIndex]->PutString("Type", c_szColumnType);
        if (0 != c_szColumnUnitCategories[0])
        {
            gs_stlColumnProperties[unColumnIndex]->PutString("UnitCategories", c_szColumnUnitCategories);
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }
}

/// <summary>
/// 
/// </summary>
/// <param name="c_aszCellValues"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) void __cdecl AddRecordToTablePackageFile(
    _in const char * c_szRawRecord
    )
{
    __DebugFunction();

    try
    {
        // Create the raw record using OUR settings
        std::string strOutputRecord = c_szRawRecord;
        strOutputRecord += '\n';
        // Now write the record to destination buffer
        ::memcpy((void *) gs_pbWriteTarget, (const void *) strOutputRecord.c_str(), strOutputRecord.length());
        gs_un64TotalSizeWritten += strOutputRecord.length();
        gs_pbWriteTarget += strOutputRecord.length();
    }
        
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szTableIdentifier"></param>
/// <param name="c_szTableTitle"></param>
/// <param name="c_szTableDescription"></param>
/// <param name="c_szTableTags"></param>
/// <param name="nNumberOfColumns"></param>
/// <param name="nNumberOfRows"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) void __cdecl CompleteTablePackageFile(
    _in const char * c_szTableIdentifier,
    _in const char * c_szTableTitle,
    _in const char * c_szTableDescription,
    _in const char * c_szTableTags,
    _in int nNumberOfColumns,
    _in int nNumberOfRows
    )
{
    __DebugFunction();

    HANDLE hFileHandle = INVALID_HANDLE_VALUE;

    try
    {
        // Make sure to adjust the size of the data to fit precisely what was written
        gs_stlTablePackageRecordsBuffer.resize(gs_un64TotalSizeWritten);
        // Now create the output StructuredBuffer and compressed data buffer
        StructuredBuffer oTableProperties;
        StructuredBuffer oColumnProperties;
        StructuredBuffer oCompressedData = ::CompressToStructuredBuffer((const void *) gs_stlTablePackageRecordsBuffer.data(), (uint64_t) gs_stlTablePackageRecordsBuffer.size());
        // Build the StructuredBuffer containing table properties
        oTableProperties.PutGuid("Identifier", Guid(c_szTableIdentifier));
        oTableProperties.PutString("Title", c_szTableTitle);
        oTableProperties.PutString("Description", c_szTableDescription);
        oTableProperties.PutString("Tags", c_szTableTags);
        oTableProperties.PutUnsignedInt32("NumberOfColumns", nNumberOfColumns);
        oTableProperties.PutUnsignedInt64("NumberOfRows", nNumberOfRows);
        oTableProperties.PutUnsignedInt64("DataSizeInBytes", oCompressedData.GetUnsignedInt64("OriginalSize"));
        oTableProperties.PutUnsignedInt64("CompressedDataSizeInBytes", oCompressedData.GetUnsignedInt64("CompressedSize"));
        // Build the StructuredBuffer containing column properties
        __DebugAssert(nNumberOfColumns == gs_stlColumnProperties.size());
        for (auto const & columnProperties : gs_stlColumnProperties)
        {
            // Generate the 'name' of the column, which is basically the string literal of a column index
            char columnIndexAsString[12];
            ::sprintf_s(columnIndexAsString, sizeof(columnIndexAsString), "%d", columnProperties.first);
            __DebugAssert(nullptr != columnProperties.second);
            oColumnProperties.PutStructuredBuffer(columnIndexAsString, *(columnProperties.second));
        }
        // Add the column properties to the table properties
        oTableProperties.PutStructuredBuffer("ColumnProperties", oColumnProperties);
        //
        // Prepare to write everything to file. We need to figure out the size of both of the sections
        // Format is
        //                        +---------------------------------------------------------+
        // Offset 0               | 64 bit marker = 0xEE094CBA1B48A123                      |
        //                        +---------------------------------------------------------+
        // Offset 8               | 32 bit size in bytes (n) of table serialized buffer     |
        //                        +---------------------------------------------------------+
        // Offset 12              | Table serialized buffer                                 |
        //                        +---------------------------------------------------------+
        // Offset 12 + n          | 64 bit marker = 0xEE094CBA1B48A123                      |
        //                        +---------------------------------------------------------+
        // Offset 20 + n          | Size in Bytes (m) of the compressed table data          |
        //                        +---------------------------------------------------------+
        // Offset 28 + n          | Serialized Compressed table data                        |
        //                        +---------------------------------------------------------+
        // Offset 28 + n + m      | 64 bit marker = 0xEE094CBA1B48A123                      |
        //                        +---------------------------------------------------------+
        //
        // Where (m) is the size of the compressed data as specified within the serialized
        // StructuredBuffer at Offet 12
        //
        // Total size in bytes of file will be 28 + n + m
        //
        const Byte * c_pbSerializedTableProperties = oTableProperties.GetSerializedBufferRawDataPtr();
        unsigned int unSerializedTablePropertiesSizeInBytes = oTableProperties.GetSerializedBufferRawDataSizeInBytes();
        const Byte * c_pbSerializedCompressedTableData = oCompressedData.GetSerializedBufferRawDataPtr();
        uint64_t un64SerializedCompressedTableDataSizeInBytes = oCompressedData.GetSerializedBufferRawDataSizeInBytes();
        // Write everything to file. This is done in two chunks. The first is the table properties, the second is the table data.
        unsigned int unNumberOfBytesWritten = 0;
        unsigned int unTotalNumberOfBytesWritten = 0;
        hFileHandle = ::CreateFileA(gs_strTargetTablePackageFilename.c_str(), GENERIC_WRITE, 0, nullptr, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
        _ThrowBaseExceptionIf((INVALID_HANDLE_VALUE == hFileHandle), "Failed to open file %s with GetLastError() = %d", gs_strTargetTablePackageFilename.c_str(), ::GetLastError());
        // First we write a special marker
        Qword qwFileMarker = 0xEE094CBA1B48A123;
        (void) ::WriteFile(hFileHandle, (const void *) &qwFileMarker, (DWORD) sizeof(qwFileMarker), (DWORD *) &unNumberOfBytesWritten, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesWritten != sizeof(qwFileMarker)), "Failed to write the special header to file", nullptr);
        unTotalNumberOfBytesWritten += unNumberOfBytesWritten;
        // Now we write the size of the table properties serialized StructuredBuffer size in bytes
        (void) ::WriteFile(hFileHandle, (const void *) &unSerializedTablePropertiesSizeInBytes, (DWORD) sizeof(unSerializedTablePropertiesSizeInBytes), (DWORD *) &unNumberOfBytesWritten, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesWritten != sizeof(unSerializedTablePropertiesSizeInBytes)), "Failed to write the table properties header size in bytes to file", nullptr);
        unTotalNumberOfBytesWritten += unNumberOfBytesWritten;
        // Now we write the serialized table metadata
        (void) ::WriteFile(hFileHandle, (const void *) c_pbSerializedTableProperties, (DWORD) unSerializedTablePropertiesSizeInBytes, (DWORD *) &unNumberOfBytesWritten, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesWritten != unSerializedTablePropertiesSizeInBytes), "Failed to write the serialized table metadata to file", nullptr);
        unTotalNumberOfBytesWritten += unNumberOfBytesWritten;
        // Now we write a special marker before writing the data
        (void) ::WriteFile(hFileHandle, (const void *) &qwFileMarker, (DWORD) sizeof(qwFileMarker), (DWORD *) &unNumberOfBytesWritten, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesWritten != sizeof(qwFileMarker)), "Failed to write the special header to file", nullptr);
        unTotalNumberOfBytesWritten += unNumberOfBytesWritten;
        // Write out the size in bytes of the serialized compressed data
        (void) ::WriteFile(hFileHandle, (const void *) &un64SerializedCompressedTableDataSizeInBytes, (DWORD) sizeof(un64SerializedCompressedTableDataSizeInBytes), (DWORD *) &unNumberOfBytesWritten, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesWritten != sizeof(un64SerializedCompressedTableDataSizeInBytes)), "Failed to write the special header to file", nullptr);
        // Now we write the data itself to file.
        // BUGBUG: This might need to be done in multiple write operations
        (void) ::WriteFile(hFileHandle, (const void *) c_pbSerializedCompressedTableData, (DWORD) un64SerializedCompressedTableDataSizeInBytes, (DWORD *) &unNumberOfBytesWritten, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesWritten != un64SerializedCompressedTableDataSizeInBytes), "Failed to write the special header to file", nullptr);
        unTotalNumberOfBytesWritten += unNumberOfBytesWritten;
        // Now we write a special marker before writing the data
        (void) ::WriteFile(hFileHandle, (const void *) &qwFileMarker, (DWORD) sizeof(qwFileMarker), (DWORD *) &unNumberOfBytesWritten, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesWritten != sizeof(qwFileMarker)), "Failed to write the special header to file", nullptr);
        unTotalNumberOfBytesWritten += unNumberOfBytesWritten;
        // Do our reality check to make sure the total bytes written is as expected
        __DebugAssert(unTotalNumberOfBytesWritten == (28 + unSerializedTablePropertiesSizeInBytes + un64SerializedCompressedTableDataSizeInBytes));
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    // Make sure to close the file. We have to put it here in case an exception gets thrown and we have to ensure the file
    // handle gets closed properly
    if (INVALID_HANDLE_VALUE != hFileHandle)
    {
        ::CloseHandle(hFileHandle);
        hFileHandle = INVALID_HANDLE_VALUE;
    }
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szTargetFilename"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) unsigned int __cdecl AddTablePackageFromFile(
    _in const char * c_szTargetFilename
    )
{
    __DebugFunction();

    unsigned int unReturnValue = 0xFFFFFFFF;
    HANDLE hFileHandle = INVALID_HANDLE_VALUE;

    try
    {
        //
        // Prepare to read everything from file. Format is:
        // 
        //                        +---------------------------------------------------------+
        // Offset 0               | 64 bit marker = 0xEE094CBA1B48A123                      |
        //                        +---------------------------------------------------------+
        // Offset 8               | 32 bit size in bytes (n) of table serialized buffer     |
        //                        +---------------------------------------------------------+
        // Offset 12              | Table serialized buffer                                 |
        //                        +---------------------------------------------------------+
        // Offset 12 + n          | 64 bit marker = 0xEE094CBA1B48A123                      |
        //                        +---------------------------------------------------------+
        // Offset 20 + n          | Size in Bytes (m) of the compressed table data          |
        //                        +---------------------------------------------------------+
        // Offset 28 + n          | Serialized Compressed table data                        |
        //                        +---------------------------------------------------------+
        // Offset 28 + n + m      | 64 bit marker = 0xEE094CBA1B48A123                      |
        //                        +---------------------------------------------------------+
        //
        // Where (m) is the size of the compressed data as specified within the serialized
        // StructuredBuffer at Offet 12
        //
        // Total size in bytes of file will be 28 + n + m
        //
        unsigned int unNumberOfBytesRead = 0;
        Qword qwMarker;
        // First we try to open the target gile
        hFileHandle = ::CreateFileA(c_szTargetFilename, GENERIC_READ, 0, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
        _ThrowBaseExceptionIf((INVALID_HANDLE_VALUE == hFileHandle), "Failed to open file %s with GetLastError() = %d", gs_strTargetTablePackageFilename.c_str(), ::GetLastError());
        // Read in the header marker from file
        (void) ::ReadFile(hFileHandle, (void *) &qwMarker, sizeof(qwMarker), (DWORD *) &unNumberOfBytesRead, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesRead != sizeof(qwMarker)), "Failed to read in the file header marker", nullptr);
        _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != (qwMarker)), "Invalid file marker (0x%08x%08x) found", HIDWORD(qwMarker), LODWORD(qwMarker));
        // Read in the table metadata size in bytes from file
        unsigned int unSerializedTableMetadateSizeInBytes = 0;
        (void) ::ReadFile(hFileHandle, (void *) &unSerializedTableMetadateSizeInBytes, sizeof(unSerializedTableMetadateSizeInBytes), (DWORD *) &unNumberOfBytesRead, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesRead != sizeof(unSerializedTableMetadateSizeInBytes)), "Failed to read serialized table metadate size in bytes value", nullptr);
        // Now we read in the table metadata
        std::vector<Byte> stlSerializedTableMetadata;
        stlSerializedTableMetadata.resize(unSerializedTableMetadateSizeInBytes);
        (void) ::ReadFile(hFileHandle, (void *) stlSerializedTableMetadata.data(), (DWORD) stlSerializedTableMetadata.size(), (DWORD *) &unNumberOfBytesRead, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesRead != stlSerializedTableMetadata.size()), "Failed to read table metadate", nullptr);
        // Read in the header marker from file
        (void) ::ReadFile(hFileHandle, (void *) &qwMarker, sizeof(qwMarker), (DWORD *) &unNumberOfBytesRead, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesRead != sizeof(qwMarker)), "Failed to read in the file header marker", nullptr);
        _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != qwMarker), "Invalid file marker (0x%08x%08x) found", HIDWORD(qwMarker), LODWORD(qwMarker));
        // Now persist the Table Metadata
        gs_ImportedTableMetadata[gs_unTableIndex] = new StructuredBuffer(stlSerializedTableMetadata);
        gs_ImportedTableFilename[gs_unTableIndex] = c_szTargetFilename;
        unReturnValue = gs_unTableIndex;
        // Reality checks
        __DebugAssert(true == gs_ImportedTableMetadata[gs_unTableIndex]->IsElementPresent("Identifier", GUID_VALUE_TYPE));
        __DebugAssert(true == gs_ImportedTableMetadata[gs_unTableIndex]->IsElementPresent("Title", ANSI_CHARACTER_STRING_VALUE_TYPE));
        __DebugAssert(true == gs_ImportedTableMetadata[gs_unTableIndex]->IsElementPresent("Description", ANSI_CHARACTER_STRING_VALUE_TYPE));
        __DebugAssert(true == gs_ImportedTableMetadata[gs_unTableIndex]->IsElementPresent("NumberOfColumns", UINT32_VALUE_TYPE));
        __DebugAssert(true == gs_ImportedTableMetadata[gs_unTableIndex]->IsElementPresent("NumberOfRows", UINT64_VALUE_TYPE));
        __DebugAssert(true == gs_ImportedTableMetadata[gs_unTableIndex]->IsElementPresent("Tags", ANSI_CHARACTER_STRING_VALUE_TYPE));
        __DebugAssert(true == gs_ImportedTableMetadata[gs_unTableIndex]->IsElementPresent("DataSizeInBytes", UINT64_VALUE_TYPE));
        __DebugAssert(true == gs_ImportedTableMetadata[gs_unTableIndex]->IsElementPresent("CompressedDataSizeInBytes", UINT64_VALUE_TYPE));
        // Increase the table index
        unReturnValue = gs_unTableIndex++;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    // Make sure to close the file. We have to put it here in case an exception gets thrown and we have to ensure the file
    // handle gets closed properly
    if (INVALID_HANDLE_VALUE != hFileHandle)
    {
        ::CloseHandle(hFileHandle);
        hFileHandle = INVALID_HANDLE_VALUE;
    }

    return unReturnValue;
}

/// <summary>
/// 
/// </summary>
/// <param name="unTableIndex"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) void __cdecl RemoveTablePackageByIndex(
    _in unsigned int unTableIndex
    )
{
    __DebugFunction();

    try
    {
        // Quick reality check
        _ThrowBaseExceptionIf((gs_ImportedTableMetadata.end() == gs_ImportedTableMetadata.find(unTableIndex)), "Table index not found %d (Exclusive Max = %d)", unTableIndex, gs_unTableIndex);
        __DebugAssert(gs_ImportedTableFilename.end() != gs_ImportedTableFilename.find(unTableIndex));
        // Now delete the related metadata first
        gs_ImportedTableMetadata[unTableIndex]->Release();
        gs_ImportedTableMetadata[unTableIndex] = nullptr;
        gs_ImportedTableMetadata.erase(unTableIndex);
        gs_ImportedTableFilename.erase(unTableIndex);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }
}

/// <summary>
/// 
/// </summary>
/// <param name="unTableIndex"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl GetTablePackageIdentifierByIndex(
    _in unsigned int unTableIndex
    )
{
    __DebugFunction();

    std::string strTablePackageIdentifier = "";

    try
    {
        // Quick reality check
        _ThrowBaseExceptionIf((gs_ImportedTableMetadata.end() == gs_ImportedTableMetadata.find(unTableIndex)), "Table index not found %d (Exclusive Max = %d)", unTableIndex, gs_unTableIndex);
        __DebugAssert(gs_ImportedTableFilename.end() != gs_ImportedTableFilename.find(unTableIndex));
        // Fetch the identifier
        strTablePackageIdentifier = gs_ImportedTableMetadata[unTableIndex]->GetGuid("Identifier").ToString(eHyphensOnly);
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return ::ConvertToBSTR(strTablePackageIdentifier);
}

/// <summary>
/// 
/// </summary>
/// <param name="unTableIndex"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl GetTablePackageTitleByIndex(
    _in unsigned int unTableIndex
    )
{
    __DebugFunction();

    std::string strTablePackageTitle = "";

    try
    {
        // Quick reality check
        _ThrowBaseExceptionIf((gs_ImportedTableMetadata.end() == gs_ImportedTableMetadata.find(unTableIndex)), "Table index not found %d (Exclusive Max = %d)", unTableIndex, gs_unTableIndex);
        __DebugAssert(gs_ImportedTableFilename.end() != gs_ImportedTableFilename.find(unTableIndex));
        // Fetch the title
        strTablePackageTitle = gs_ImportedTableMetadata[unTableIndex]->GetString("Title");
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return ::ConvertToBSTR(strTablePackageTitle);
}

/// <summary>
/// 
/// </summary>
/// <param name="unTableIndex"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl GetTablePackageDescriptionByIndex(
    _in unsigned int unTableIndex
    )
{
    __DebugFunction();

    std::string strTablePackageDescription = "";

    try
    {
        // Quick reality check
        _ThrowBaseExceptionIf((gs_ImportedTableMetadata.end() == gs_ImportedTableMetadata.find(unTableIndex)), "Table index not found %d (Exclusive Max = %d)", unTableIndex, gs_unTableIndex);
        __DebugAssert(gs_ImportedTableFilename.end() != gs_ImportedTableFilename.find(unTableIndex));
        // Fetch the title
        strTablePackageDescription = gs_ImportedTableMetadata[unTableIndex]->GetString("Description");
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return ::ConvertToBSTR(strTablePackageDescription);
}

/// <summary>
/// 
/// </summary>
/// <param name="unTableIndex"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) BSTR __cdecl GetTablePackageFilenameByIndex(
    _in unsigned int unTableIndex
    )
{
    __DebugFunction();

    std::string strTablePackageFilename = "";

    try
    {
        // Quick reality check
        _ThrowBaseExceptionIf((gs_ImportedTableMetadata.end() == gs_ImportedTableMetadata.find(unTableIndex)), "Table index not found %d (Exclusive Max = %d)", unTableIndex, gs_unTableIndex);
        __DebugAssert(gs_ImportedTableFilename.end() != gs_ImportedTableFilename.find(unTableIndex));
        // Fetch the table filename
        strTablePackageFilename = gs_ImportedTableFilename[unTableIndex];
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return ::ConvertToBSTR(strTablePackageFilename);
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szDatasetFilename"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) bool __cdecl GenerateDataset(
    _in const char * c_szDatasetFilename,
    _in const char * c_szDatasetIdentifier,
    _in const char * c_szDatasetTitle,
    _in const char * c_szDatasetDescription,
    _in const char * c_szDatasetTags,
    _in const char * c_szDatasetFamilyIdentifier
    )
{
    __DebugFunction();

    bool fSuccess = false;
    HANDLE hFileHandle = INVALID_HANDLE_VALUE;

    try
    {
        // The first part of generating a dataset is to build the StructuredBuffer which contains the dataset metadata
        StructuredBuffer oDatasetMetadata;
        // STEP 1: Generic dataset level metadata
        oDatasetMetadata.PutGuid("Identifier", Guid(c_szDatasetIdentifier));
        oDatasetMetadata.PutString("Title", c_szDatasetTitle);
        oDatasetMetadata.PutString("Description", c_szDatasetDescription);
        oDatasetMetadata.PutString("Tags", c_szDatasetTags);
        oDatasetMetadata.PutGuid("Organization", Guid(::GetSailPlatformServicesUserOrganizationIdentifier().c_str()));
        oDatasetMetadata.PutUnsignedInt64("EpochCreationTime", ::GetEpochTimeInSeconds());
        oDatasetMetadata.PutUnsignedInt32("TableCount", (unsigned int) gs_ImportedTableMetadata.size());
        if (0 < ::strnlen(c_szDatasetFamilyIdentifier, 2))
        {
            oDatasetMetadata.PutGuid("DataFamilyIdentifier", Guid(c_szDatasetFamilyIdentifier));
        }
        // STEP 2: Tables information
        StructuredBuffer oTablePackageMetadata;
        for (std::pair<unsigned int, StructuredBuffer *> tablePackageEntry : gs_ImportedTableMetadata)
        {
            std::string tableIdentifier = tablePackageEntry.second->GetGuid("Identifier").ToString(eHyphensAndCurlyBraces);
            oTablePackageMetadata.PutStructuredBuffer(tableIdentifier.c_str(), *tablePackageEntry.second);
        }
        oDatasetMetadata.PutStructuredBuffer("Tables", oTablePackageMetadata);
        //
        // Prepare to write everything to file. Format is:
        // 
        //                        +----------------------------------------------------------------+
        // Offset 0               | 64 bit marker = 0xEE094CBA1B48A123                             |
        //                        +----------------------------------------------------------------+
        // Offset 8               | 32 bit size in bytes (n) of dataset metadata serialized buffer |
        //                        +----------------------------------------------------------------+
        // Offset 12              | Dataset metadata serialized buffer                             |
        //                        +----------------------------------------------------------------+
        // Offset 12 + n          | 64 bit marker = 0xEE094CBA1B48A123                             |
        //                        +----------------------------------------------------------------+
        // Offset 20 + n          | UUID of table for next chunk of table data                     |
        //                        +----------------------------------------------------------------+
        // Offset 36 + n          | Size in Bytes of compressed table data                         |
        //                        +----------------------------------------------------------------+
        // Offset 42 + n          | Compressed table data                                          |
        //                        +----------------------------------------------------------------+
        //                                         Repeat for the number of tables
        //                        +----------------------------------------------------------------+
        //                        | 64 bit marker = 0xEE094CBA1B48A123                             |
        //                        +----------------------------------------------------------------+
        // Where (z) = (total size of all compressed table data) + (number of tables * 16)
        //
 
        // Serialize the dataset/table metadata so we can write it to disk
        const Byte * c_pbSerializedDatasetMetadataBuffer = (const Byte *) oDatasetMetadata.GetSerializedBufferRawDataPtr();
        unsigned int unSerializedDatasetMetadataBufferSizeInBytes = oDatasetMetadata.GetSerializedBufferRawDataSizeInBytes();
        // Now open the file and write the metadata into it
        unsigned int unNumberOfBytesWritten = 0;
        hFileHandle = ::CreateFileA(c_szDatasetFilename, GENERIC_WRITE, 0, nullptr, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
        _ThrowBaseExceptionIf((INVALID_HANDLE_VALUE == hFileHandle), "Failed to open file %s with GetLastError() = %d", c_szDatasetFilename, ::GetLastError());
        // Add a marker at the beginning of the file. This is used as a reality check
        Qword qwFileMarker = 0xEE094CBA1B48A123;
        (void) ::WriteFile(hFileHandle, (const void *) &qwFileMarker, (DWORD) sizeof(qwFileMarker), (DWORD *) &unNumberOfBytesWritten, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesWritten != sizeof(qwFileMarker)), "Failed to write the special header to file", nullptr);
        // Now we write the dataset metadata size in bytes to file
        (void) ::WriteFile(hFileHandle, (const void *) &unSerializedDatasetMetadataBufferSizeInBytes, (DWORD) sizeof(unSerializedDatasetMetadataBufferSizeInBytes), (DWORD *) &unNumberOfBytesWritten, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesWritten != sizeof(unSerializedDatasetMetadataBufferSizeInBytes)), "Failed to write the dataset metadata size in bytes to file", nullptr);
        // Now we write the dataset metadata to file
        (void) ::WriteFile(hFileHandle, (const void *) c_pbSerializedDatasetMetadataBuffer, (DWORD) unSerializedDatasetMetadataBufferSizeInBytes, (DWORD *) &unNumberOfBytesWritten, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesWritten != unSerializedDatasetMetadataBufferSizeInBytes), "Failed to write the dataset metadata to file", nullptr);
        // Now write the table data to file, one at a time
        for (const std::pair<unsigned int, StructuredBuffer *> c_stlTablePackageEntry : gs_ImportedTableMetadata)
        {
            // Variables required to read data from the table package in order to extract compressed data
            unsigned int unNumberOfBytesRead = 0;
            Qword qwTableFileMarker;
            std::vector<Byte> stlBuffer;
            // Read in the compressed data from the original file
            __DebugAssert(gs_ImportedTableFilename.end() != gs_ImportedTableFilename.find(c_stlTablePackageEntry.first));
            HANDLE hTableFileHandle = ::CreateFileA(gs_ImportedTableFilename[c_stlTablePackageEntry.first].c_str(), GENERIC_READ, 0, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
            _ThrowBaseExceptionIf((INVALID_HANDLE_VALUE == hTableFileHandle), "Failed to open file %s with GetLastError() = %d", gs_ImportedTableFilename[c_stlTablePackageEntry.first].c_str(), ::GetLastError());
            // Read in the header marker from file
            (void) ::ReadFile(hTableFileHandle, (void *) &qwTableFileMarker, sizeof(qwTableFileMarker), (DWORD *) &unNumberOfBytesRead, nullptr);
            _ThrowBaseExceptionIf((unNumberOfBytesRead != sizeof(qwTableFileMarker)), "Failed to read in the file header marker", nullptr);
            _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != (qwTableFileMarker)), "Invalid file marker (0x%08x%08x) found", HIDWORD(qwTableFileMarker), LODWORD(qwTableFileMarker));
            // Read in the table metadata size in bytes from file
            unsigned int unSerializedTableMetadateSizeInBytes = 0;
            (void) ::ReadFile(hTableFileHandle, (void *) &unSerializedTableMetadateSizeInBytes, sizeof(unSerializedTableMetadateSizeInBytes), (DWORD *) &unNumberOfBytesRead, nullptr);
            _ThrowBaseExceptionIf((unNumberOfBytesRead != sizeof(unSerializedTableMetadateSizeInBytes)), "Failed to read serialized table metadate size in bytes value", nullptr);
            // Now we read in the table metadata
            stlBuffer.resize(unSerializedTableMetadateSizeInBytes);
            (void) ::ReadFile(hTableFileHandle, (void *) stlBuffer.data(), (DWORD) stlBuffer.size(), (DWORD *) &unNumberOfBytesRead, nullptr);
            _ThrowBaseExceptionIf((unNumberOfBytesRead != stlBuffer.size()), "Failed to read table metadate", nullptr);
            // Make sure the file we are reading is the same as the table we are expecting
            StructuredBuffer oTableMetadata(stlBuffer);
            // Read in the header marker from file
            (void) ::ReadFile(hTableFileHandle, (void *) &qwTableFileMarker, sizeof(qwTableFileMarker), (DWORD *) &unNumberOfBytesRead, nullptr);
            _ThrowBaseExceptionIf((unNumberOfBytesRead != sizeof(qwTableFileMarker)), "Failed to read in the file header marker", nullptr);
            _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != (qwTableFileMarker)), "Invalid file marker (0x%08x%08x) found", HIDWORD(qwTableFileMarker), LODWORD(qwTableFileMarker));
            // We need to read in the size in bytes of the serialized compressed data
            uint64_t un64SerializedSizeInBytesOfCompressedData = 0;
            (void) ::ReadFile(hTableFileHandle, (void *) &un64SerializedSizeInBytesOfCompressedData, sizeof(un64SerializedSizeInBytesOfCompressedData), (DWORD *) &unNumberOfBytesRead, nullptr);
            _ThrowBaseExceptionIf((unNumberOfBytesRead != sizeof(un64SerializedSizeInBytesOfCompressedData)), "Failed to read in the file header marker", nullptr);
            // Read in the compressed data from the file. There are a lot of reality checks here to ensure that
            // the table we are reading in is the correct table
            __DebugAssert(true == c_stlTablePackageEntry.second->IsElementPresent("Identifier", GUID_VALUE_TYPE));
            __DebugAssert(true == c_stlTablePackageEntry.second->IsElementPresent("CompressedDataSizeInBytes", UINT64_VALUE_TYPE));
            std::string tableIdentifier = oTableMetadata.GetGuid("Identifier").ToString(eHyphensAndCurlyBraces);
            uint64_t un64CompressedDataSizeInBytes = oTableMetadata.GetUnsignedInt64("CompressedDataSizeInBytes");
            _ThrowBaseExceptionIf((tableIdentifier != c_stlTablePackageEntry.second->GetGuid("Identifier").ToString(eHyphensAndCurlyBraces)), "ERROR: Table identifiers do not match %s != %s", tableIdentifier.c_str(), c_stlTablePackageEntry.second->GetGuid("Identifier").ToString(eHyphensAndCurlyBraces).c_str());
            _ThrowBaseExceptionIf((un64CompressedDataSizeInBytes != c_stlTablePackageEntry.second->GetUnsignedInt64("CompressedDataSizeInBytes")), "ERROR: Table compressed data sizes do not match %ld != %ld", un64CompressedDataSizeInBytes, c_stlTablePackageEntry.second->GetUnsignedInt64("CompressedDataSizeInBytes"));
            stlBuffer.resize(un64SerializedSizeInBytesOfCompressedData);
            (void) ::ReadFile(hTableFileHandle, (void *) stlBuffer.data(), (unsigned int) stlBuffer.size(), (DWORD *) &unNumberOfBytesRead, nullptr);
            _ThrowBaseExceptionIf((unNumberOfBytesRead != stlBuffer.size()), "Failed to read table metadate", nullptr);
            // Read in the header marker from file
            (void) ::ReadFile(hTableFileHandle, (void *) &qwTableFileMarker, sizeof(qwTableFileMarker), (DWORD *) &unNumberOfBytesRead, nullptr);
            _ThrowBaseExceptionIf((unNumberOfBytesRead != sizeof(qwTableFileMarker)), "Failed to read in the file header marker", nullptr);
            _ThrowBaseExceptionIf((0xEE094CBA1B48A123 != (qwTableFileMarker)), "Invalid file marker (0x%08x%08x) found", HIDWORD(qwTableFileMarker), LODWORD(qwTableFileMarker));
            // Make sure to close the input file
            ::CloseHandle(hTableFileHandle);
            hTableFileHandle = INVALID_HANDLE_VALUE;
            // Write a marker to file
            (void) ::WriteFile(hFileHandle, (const void *) &qwFileMarker, (DWORD) sizeof(qwFileMarker), (DWORD *) &unNumberOfBytesWritten, nullptr);
            _ThrowBaseExceptionIf((unNumberOfBytesWritten != sizeof(qwFileMarker)), "Failed to write the special header to file", nullptr);
            // Write the table identifier to file
            (void) ::WriteFile(hFileHandle, (const void *) c_stlTablePackageEntry.second->GetGuid("Identifier").GetRawDataPtr(), (DWORD) 16, (DWORD *) &unNumberOfBytesWritten, nullptr);
            _ThrowBaseExceptionIf((unNumberOfBytesWritten != 16), "Failed to write the table identifier to file", nullptr);
            // Write the compressed table data size in bytes to file
            (void) ::WriteFile(hFileHandle, (const void *) &un64SerializedSizeInBytesOfCompressedData, (DWORD) sizeof(un64SerializedSizeInBytesOfCompressedData), (DWORD *) &unNumberOfBytesWritten, nullptr);
            _ThrowBaseExceptionIf((unNumberOfBytesWritten != sizeof(un64SerializedSizeInBytesOfCompressedData)), "Failed to write the table compressed data size in bytes to file", nullptr);
            // Write the compressed table data to file
            (void) ::WriteFile(hFileHandle, (const void *) stlBuffer.data(), (DWORD) stlBuffer.size(), (DWORD *) &unNumberOfBytesWritten, nullptr);
            _ThrowBaseExceptionIf((unNumberOfBytesWritten != stlBuffer.size()), "Failed to write the table compressed data to file", nullptr);
        }
        // Add a marker at the end of the file. This is used as a reality check
        (void) ::WriteFile(hFileHandle, (const void *) &qwFileMarker, (DWORD) sizeof(qwFileMarker), (DWORD *) &unNumberOfBytesWritten, nullptr);
        _ThrowBaseExceptionIf((unNumberOfBytesWritten != sizeof(qwFileMarker)), "Failed to write the special header to file", nullptr);
        fSuccess = true;
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    // Make sure to close the file. We have to put it here in case an exception gets thrown and we have to ensure the file
    // handle gets closed properly
    if (INVALID_HANDLE_VALUE != hFileHandle)
    {
        ::CloseHandle(hFileHandle);
        hFileHandle = INVALID_HANDLE_VALUE;
    }

    return fSuccess;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szDatasetFilename"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) bool __cdecl PublishDataset(
    _in const char * c_szDatasetFilename
    )
{
    __DebugFunction();

    bool fSuccess = true;

    try
    {
        // The first part required is to load up the metadata portion of the dataset

    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return fSuccess;
}