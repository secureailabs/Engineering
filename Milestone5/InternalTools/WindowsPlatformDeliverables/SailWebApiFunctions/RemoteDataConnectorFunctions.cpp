#include <Windows.h>

#include "64BitHashes.h"
#include "Base64Encoder.h"
#include "CoreTypes.h"
#include "DebugLibrary.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"
#include "JsonParser.h"
#include "JsonValue.h"
#include "RestApiHelperFunctions.h"
#include "SailApiBaseServices.h"
#include "SharedUtilityFunctions.h"
#include "StructuredBuffer.h"

#include <mutex>
#include <set>
#include <thread>

static bool gs_fIsRemoteDataConnectorRegistered = false;
static Guid gs_oRemoteDataConnectorIdentifier;
static std::map<Qword, std::string> gs_stlListOfRegisteredDatasetFilenames;
static std::map<Qword, std::string> gs_stlListOfRegisteredDatasetFiles;
static std::map<Qword, std::string> gs_stlListOfNewDatasetFiles;
static std::mutex gs_stlVirtualMachineUploadMutex;
static std::set<Qword> gs_stlListOfCurrentlyRunningUploads;

/// <summary>
/// 
/// </summary>
/// <param name="c_poUploadParameters"></param>
static Dword __stdcall UploadDatasetToVirtualMachine(
    _in void * pParameters
    )
{
    __DebugFunction();

    bool fSuccess = false;
    std::string strVirtualMachineIpAddress = "";
    std::string strDatasetFilename = "";
    Qword qw64BitHashOfConcatenatedIdentifiers = 0;

    try
    {
        // Deserialize the incoming base64 string into the target StructuredBuffer
        StructuredBuffer oVirtualMachineInformation((char *) pParameters);
        // Extract some basic information
        qw64BitHashOfConcatenatedIdentifiers = oVirtualMachineInformation.GetQword("64BitHashOfConcatenatedIdentifiers");
        strVirtualMachineIpAddress = oVirtualMachineInformation.GetString("IPAddress");
        strDatasetFilename = oVirtualMachineInformation.GetString("DatasetFilename");
        oVirtualMachineInformation.RemoveElement("64BitHashOfConcatenatedIdentifiers");
        oVirtualMachineInformation.RemoveElement("IPAddress");
        oVirtualMachineInformation.RemoveElement("DatasetFilename");
        // Load the file into a binary buffer and add it to the StructuredBuffer
        std::vector<Byte> stlDatasetFiledata = ::GetBinaryFileBuffer(strDatasetFilename.c_str());
        std::string strEncoded = ::Base64Encode(stlDatasetFiledata.data(), (unsigned int)stlDatasetFiledata.size());
        oVirtualMachineInformation.PutString("Base64EncodedDataset", strEncoded);
        // Prepare the JSON blob
        auto oJsonBody = JsonValue::ParseStructuredBufferToJson(oVirtualMachineInformation);
        std::string strJsonBody = oJsonBody->ToString();
        oJsonBody->Release();
        // Add notification to mark the beginning of the upload transaction
        ::RegisterExceptionalMessage("Began uploading dataset %s to %s", strDatasetFilename.c_str(), strVirtualMachineIpAddress.c_str());
        // Execute the upload transaction
        auto stlRestResponse = ::RestApiCall(strVirtualMachineIpAddress, (Word) 6200, "GET", "/something", strJsonBody, false);
        // Parse the returning value.
        fSuccess = true;
    }

    catch (BaseException oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    // Add notification to mark the end of the upload transaction. This is done regardless
    // of how the transaction pans out
    if (true == fSuccess)
    {
        ::RegisterExceptionalMessage("Successfully finished uploading dataset %s to %s", strDatasetFilename.c_str(), strVirtualMachineIpAddress.c_str());
    }
    else
    {
        ::RegisterExceptionalMessage("Failed to upload dataset %s to %s", strDatasetFilename.c_str(), strVirtualMachineIpAddress.c_str());
    }

    // No matter what happens, always remove gs_stlListOfCurrentlyRunningUploads entry
    const std::lock_guard<std::mutex> stlVirtualMachineUploadMutexLock(gs_stlVirtualMachineUploadMutex);
    if (gs_stlListOfCurrentlyRunningUploads.end() != gs_stlListOfCurrentlyRunningUploads.find(qw64BitHashOfConcatenatedIdentifiers))
    {
        gs_stlListOfCurrentlyRunningUploads.erase(qw64BitHashOfConcatenatedIdentifiers);
    }

    return 0;
}

/// <summary>
/// 
/// </summary>
/// <param name=""></param>
/// <returns></returns>
extern "C" __declspec(dllexport) int __cdecl RemoteDataConnectorHeartbeat(void)
{
    __DebugFunction();

    int nReturnCode = 0;    // Return code used to denote that there is no heartbeat to give yet

    try
    {
        if (true == gs_fIsRemoteDataConnectorRegistered)
        {
            // Return code used to denote that the heatbeat has failed
            nReturnCode = -1;
            // Build API packet
            StructuredBuffer oHeartbeatRequest;
            oHeartbeatRequest.PutString("RemoteDataConnectorGuid", gs_oRemoteDataConnectorIdentifier.ToString(eHyphensAndCurlyBraces));
            // Send the ping to the REST portal and get a response stating if any
            // Virtual Machine is waiting for this dataset
            std::string strVerb = "PUT";
            std::string strApiUrl = "/SAIL/RemoteDataConnectorManager/HeartBeat?Eosb=" + ::GetSailPlatformServicesEosb();
            auto oJsonBody = JsonValue::ParseStructuredBufferToJson(oHeartbeatRequest);
            std::string strJsonBody = oJsonBody->ToString();
            oJsonBody->Release();
            std::vector<Byte> stlRestResponse = ::RestApiCall(::GetSailPlatformServicesIpAddress(), (Word) 6200, strVerb, strApiUrl, strJsonBody, true);
            // Parse the returning value.
            StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
            float64_t fl64Response = oResponse.GetFloat64("Status");
            if (200 == fl64Response)
            {
                // The heartbeat was a success
                nReturnCode = 1;
                // Check if any Virtual Machine is waiting for the dataset, if yes new threads
                // are created to upload data into those Virutal Machines
                if (true == oResponse.IsElementPresent("VirtualMachines", INDEXED_BUFFER_VALUE_TYPE))
                {
                    StructuredBuffer oVirtualMachinesWaiting = oResponse.GetStructuredBuffer("VirtualMachines");
                    for (auto strVirtualMachineIdentifier : oVirtualMachinesWaiting.GetNamesOfElements())
                    {
                        // There is a Virtual Machine waiting for data, a new thread is created
                        // to connect to the Virutal Machine and upload the data
                        StructuredBuffer oVirtualMachineInformation = oVirtualMachinesWaiting.GetStructuredBuffer(strVirtualMachineIdentifier.c_str());
                        std::string strDatasetIdentifier = oVirtualMachineInformation.GetString("DatasetGuid");
                        // Figure out if we are already dealing with uploading this dataset to the target virtual machine
                        bool fIsNewRequest = true;
                        {
                            std::string strConcatenatedIdentifiers = strVirtualMachineIdentifier + "<--" + strDatasetIdentifier;
                            Qword qw64BitHashOfConcatenatedIdentifiers = ::Get64BitHashOfNullTerminatedString(strConcatenatedIdentifiers.c_str(), false);
                            const std::lock_guard<std::mutex> stlVirtualMachineUploadMutexLock(gs_stlVirtualMachineUploadMutex);
                            if (gs_stlListOfCurrentlyRunningUploads.end() != gs_stlListOfCurrentlyRunningUploads.find(qw64BitHashOfConcatenatedIdentifiers))
                            {
                                // There is already a running thread dedicated to uploading the requested dataset
                                // to the target virtual machine. So we ignore it.
                                fIsNewRequest = false;
                            }
                            else
                            {
                                // Insert the request now
                                gs_stlListOfCurrentlyRunningUploads.insert(qw64BitHashOfConcatenatedIdentifiers);
                            }
                            oVirtualMachineInformation.PutQword("64BitHashOfConcatenatedIdentifiers", qw64BitHashOfConcatenatedIdentifiers);
                        }
                        // Only create a new thread if this is a new request.
                        if (true == fIsNewRequest)
                        {
                            std::string strDatasetFilename;
                            for (auto strDatasetFile : gs_stlListOfRegisteredDatasetFiles)
                            {
                                if (strDatasetIdentifier == strDatasetFile.second)
                                {
                                    strDatasetFilename = gs_stlListOfRegisteredDatasetFilenames[strDatasetFile.first];
                                }
                            }
                            _ThrowBaseExceptionIf((0 == strDatasetFilename.size()), "Invalid dataset request from VM %s", strVirtualMachineIdentifier.c_str());
                            oVirtualMachineInformation.PutString("DatasetFilename", strDatasetFilename);
                            oVirtualMachineInformation.PutString("SailWebApiPortalIpAddress", ::GetSailPlatformServicesIpAddress());
                            oVirtualMachineInformation.PutString("DataOwnerAccessToken", ::GetSailPlatformServicesEosb());
                            oVirtualMachineInformation.PutString("DataOwnerUserIdentifier", ::GetSailPlatformServicesUserIdentifier());
                            oVirtualMachineInformation.PutString("DataOwnerOrganizationIdentifier", ::GetSailPlatformServicesUserOrganizationIdentifier());
                            std::string strBase64EncodedSerializedBuffer = oVirtualMachineInformation.GetBase64SerializedBuffer();
                            char * c_szBased64EncodedSerializedBuffer = (char *) ::malloc(strBase64EncodedSerializedBuffer.size() + 1);
                            _ThrowOutOfMemoryExceptionIfNull(c_szBased64EncodedSerializedBuffer);
                            ::memcpy((void *) c_szBased64EncodedSerializedBuffer, (const void *) strBase64EncodedSerializedBuffer.c_str(), strBase64EncodedSerializedBuffer.size() + 1);
                            strBase64EncodedSerializedBuffer.clear();
                            ::CreateThread(nullptr, 0, (LPTHREAD_START_ROUTINE) UploadDatasetToVirtualMachine, (void *) c_szBased64EncodedSerializedBuffer, 0, nullptr);
                        }
                    }
                }
            }
        }
    }

    catch (BaseException oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return nReturnCode;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szSourceFolder"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) int __cdecl RemoteDataConnectorUpdateDatasets(void)
{
    __DebugFunction();

    int nNumberOfNewDatasets = 0;

    try
    {
        // Only run this function if we have new datasets to register
        if (0 < gs_stlListOfNewDatasetFiles.size())
        {
            // First we need to build a StructuredBuffer of StructuredBuffers which contain
            // dataset information
            StructuredBuffer oListOfDatasets;
            for (auto strNewDataset : gs_stlListOfNewDatasetFiles)
            {
                StructuredBuffer oDatasetInformation;

                oDatasetInformation.PutString("DatasetUuid", strNewDataset.second);
                oListOfDatasets.PutStructuredBuffer(strNewDataset.second.c_str(), oDatasetInformation);
                gs_stlListOfRegisteredDatasetFiles[strNewDataset.first] = strNewDataset.second;
                __DebugAssert(gs_stlListOfRegisteredDatasetFilenames.end() != gs_stlListOfRegisteredDatasetFilenames.find(strNewDataset.first));
            }
            // Now we upload the new dataset information to the API Portal
            // First, we need to determine if this is the first time since there is difference
            std::string strVerb = "";
            std::string strApiUrl = "";
            if (false == gs_fIsRemoteDataConnectorRegistered)
            {
                // Register the DatasetConnector on finding the first valid dataset
                strVerb = "POST";
                strApiUrl = "/SAIL/RemoteDataConnectorManager/RegisterConnector?Eosb=" + ::GetSailPlatformServicesEosb();
                gs_fIsRemoteDataConnectorRegistered = true;
            }
            else
            {
                // Register the DatasetConnector on finding the first valid dataset
                strVerb = "PUT";
                strApiUrl = "/SAIL/RemoteDataConnectorManager/UpdateConnector?Eosb=" + ::GetSailPlatformServicesEosb();
            }

            StructuredBuffer oUpdateDataConnector;
            oUpdateDataConnector.PutString("RemoteDataConnectorGuid", gs_oRemoteDataConnectorIdentifier.ToString(eHyphensAndCurlyBraces));
            oUpdateDataConnector.PutStructuredBuffer("Datasets", oListOfDatasets);
            oUpdateDataConnector.PutString("Version", "0.0.1");
            auto oJsonBody = JsonValue::ParseStructuredBufferToJson(oUpdateDataConnector);
            std::string strJsonBody = oJsonBody->ToString();
            oJsonBody->Release();
            std::vector<Byte> stlRestResponse = ::RestApiCall(::GetSailPlatformServicesIpAddress(), (Word) 6200, strVerb, strApiUrl, strJsonBody, true);
            // Parse the returning value.
            StructuredBuffer oResponse = ::ConvertJsonStringToStructuredBuffer((const char *) stlRestResponse.data());
            _ThrowBaseExceptionIf(((201 != oResponse.GetFloat64("Status")) && (200 != oResponse.GetFloat64("Status"))), "Failed to upload datasets to Platform Services", nullptr);
            // To mark our success, initialize the return value unNumberOfNewDatasets
            nNumberOfNewDatasets = (int) gs_stlListOfNewDatasetFiles.size();
            // Make sure to reset gs_stlListOfNewDatasetFiles
            gs_stlListOfNewDatasetFiles.clear();
        }
    }

    catch (BaseException oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }

    return nNumberOfNewDatasets;
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szSourceFolder"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) void __cdecl RemoteDataConnectorAddDataset(
    _in const char * c_szDatasetFilename
)
{
    __DebugFunction();

    try
    {
        // Get the has of the dataset filename
        Qword qwHashOfDatasetFilename = ::Get64BitHashOfNullTerminatedString(c_szDatasetFilename, false);
        // Check to make sure we haven't registed the file already
        if ((gs_stlListOfRegisteredDatasetFiles.end() == gs_stlListOfRegisteredDatasetFiles.find(qwHashOfDatasetFilename)) && (gs_stlListOfNewDatasetFiles.end() == gs_stlListOfNewDatasetFiles.find(qwHashOfDatasetFilename)))
        {
            unsigned int unNumberOfRetries = 0;
            bool fSuccess = false;

            // Because it is possible for this function to fire when someone is still writing to the
            // dataset, there are a series of race conditions that we must deal with in order for
            // the process not to crash.
            while ((false == fSuccess) && (5 > unNumberOfRetries))
            {
                try
                {
                    // Load the contents of the dataset file into a binary buffer
                    std::vector<Byte> stlBinaryFile = ::GetBinaryFileBuffer(c_szDatasetFilename);
                    _ThrowBaseExceptionIf((0 == stlBinaryFile.size()), "Failed to open file %s", c_szDatasetFilename);
                    // Read the header marker of the file to make sure it's the expected value
                    const Byte * c_pbBinaryBuffer = (Byte *) stlBinaryFile.data();
                    uint64_t un64Header = *((uint64_t *) c_pbBinaryBuffer);
                    _ThrowBaseExceptionIf((0xDEADBEEFDEADBEEF != un64Header), "Expected header to be [0xDEADBEEFDEADBEEF] but found [%xul]", un64Header);
                    c_pbBinaryBuffer += sizeof(un64Header);
                    // Read the size in bytes of the header information structure
                    uint32_t un32SizeOfHeaderStructure = *((uint32_t *) c_pbBinaryBuffer);
                    _ThrowBaseExceptionIf(((un32SizeOfHeaderStructure + sizeof(un64Header) + sizeof(un32SizeOfHeaderStructure)) >= stlBinaryFile.size()), "Unrealistic size of header structure = %d", un32SizeOfHeaderStructure);
                    c_pbBinaryBuffer += sizeof(un32SizeOfHeaderStructure);
                    // Read in the header information structure into a StructuredBuffer
                    StructuredBuffer oHeaderInformation(c_pbBinaryBuffer, un32SizeOfHeaderStructure);
                    uint64_t un64MetaDataOffset = oHeaderInformation.GetUnsignedInt64("MetaDataOffset");
                    int32_t un32MetaDataSizeInBytes = oHeaderInformation.GetInt32("MetaDataSize");
                    _ThrowBaseExceptionIf(((un64MetaDataOffset + un32MetaDataSizeInBytes) > stlBinaryFile.size()), "Unrealistic offset (%ul) and size (%d) of metadata structure = %d", un64MetaDataOffset, un32SizeOfHeaderStructure);
                    // Reset the c_pbBinaryBuffer pointer and then extract the metadata
                    c_pbBinaryBuffer = (Byte *) stlBinaryFile.data();
                    c_pbBinaryBuffer += un64MetaDataOffset;
                    StructuredBuffer oMetadataInformation(c_pbBinaryBuffer, un32MetaDataSizeInBytes);
                    // Get the identifier of the dataset
                    std::string strDatasetIdentifier = oMetadataInformation.GetString("UUID");
                    // Add the new dataset now that we know that the identifier of the dataset is
                    gs_stlListOfNewDatasetFiles[qwHashOfDatasetFilename] = strDatasetIdentifier;
                    gs_stlListOfRegisteredDatasetFilenames[qwHashOfDatasetFilename] = c_szDatasetFilename;
                    fSuccess = true;
                }

                catch (BaseException oBaseException)
                {
                    ::RegisterException(oBaseException, __func__, __LINE__);
                    // Sleep for 5 seconds to give time for the dataset file to be fully copied to the folder
                    ::Sleep(5000);
                    unNumberOfRetries++;
                }

                catch (...)
                {
                    ::RegisterUnknownException(__func__, __LINE__);
                    // Sleep for 5 seconds to give time for the dataset file to be fully copied to the folder
                    ::Sleep(5000);
                    unNumberOfRetries++;
                }
            }
        }
    }

    catch (BaseException oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }
}

/// <summary>
/// 
/// </summary>
/// <param name="c_szSourceFolder"></param>
/// <returns></returns>
extern "C" __declspec(dllexport) void __cdecl RemoteDataConnectorRemoveDataset(
    _in const char * c_szDatasetFilename
)
{
    __DebugFunction();

    try
    {
        // Get the has of the dataset filename
        Qword qwHashOfDatasetFilename = ::Get64BitHashOfNullTerminatedString(c_szDatasetFilename, false);
        // Now remove the entries relating to that filename
        if (gs_stlListOfRegisteredDatasetFiles.end() != gs_stlListOfRegisteredDatasetFiles.find(qwHashOfDatasetFilename))
        {
            gs_stlListOfRegisteredDatasetFiles.erase(qwHashOfDatasetFilename);
        }
        if (gs_stlListOfNewDatasetFiles.end() != gs_stlListOfNewDatasetFiles.find(qwHashOfDatasetFilename))
        {
            gs_stlListOfNewDatasetFiles.erase(qwHashOfDatasetFilename);
        }
        if (gs_stlListOfRegisteredDatasetFilenames.end() != gs_stlListOfRegisteredDatasetFilenames.find(qwHashOfDatasetFilename))
        {
            gs_stlListOfRegisteredDatasetFilenames.erase(qwHashOfDatasetFilename);
        }
    }

    catch (BaseException oBaseException)
    {
        ::RegisterException(oBaseException, __func__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __LINE__);
    }
}