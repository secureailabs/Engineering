/*********************************************************************************************
 *
 * @file DataFederationManager.cpp
 * @author David Gascon
 * @date 14 March 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 * @brief
 ********************************************************************************************/

#include "DataFederation.h"
#include "DatabaseManager.h"

/********************************************************************************************
 *
 * @class DatabaseManager
 * @function RegisterDataFederation
 * @brief Save a Data Federation in the database
 * @param[in] c_oRequest contains the information for the new data federation
 * @throw BaseException Error StructuredBuffer element not found
 * @returns Serialized StructuredBuffer containing the response
 *
 ********************************************************************************************/
std::vector<Byte> __thiscall DatabaseManager::RegisterDataFederation(
    _in const StructuredBuffer & c_oRequest
    )
{
    __DebugFunction();

    StructuredBuffer oResponse;

    Dword dwStatus = 204;
    try
    {
        // Get the object to write to the database
        StructuredBuffer oObject = c_oRequest.GetStructuredBuffer("DataFederation");

        Guid oObjectGuid, oPlainTextObjectBlobGuid;

        bsoncxx::document::value oDataFederationDocumentView = bsoncxx::builder::stream::document{}
        << "PlainTextObjectBlobGuid" << oPlainTextObjectBlobGuid.ToString(eHyphensAndCurlyBraces)
        << "DataFederationIdentifier" << oObject.GetGuid("DataFederationIdentifier").ToString(eHyphensAndCurlyBraces)
        << "DataFederationOwnerOrganizationIdentifier" << oObject.GetGuid("DataFederationOwnerOrganizationIdentifier").ToString(eHyphensAndCurlyBraces)
        << finalize;

        // Create a blob for the serialized structured buffer
        bsoncxx::types::b_binary oObjectBlob
        {
            bsoncxx::binary_sub_type::k_binary,
            uint32_t(oObject.GetSerializedBufferRawDataSizeInBytes()),
            oObject.GetSerializedBufferRawDataPtr()
        };

        // Create a document that has our object's GUID and its serialized data
        bsoncxx::document::value oObjectDocumentValue = bsoncxx::builder::stream::document{}
        << "ObjectGuid" << oObjectGuid.ToString(eHyphensAndCurlyBraces)
        << "ObjectBlob" << oObjectBlob
        << finalize;

        // Create a plain text object document - telling us this GUID is a dataset family
        bsoncxx::document::value oPlainTextObjectDocumentValue = bsoncxx::builder::stream::document{}
        << "PlainTextObjectBlobGuid" << oPlainTextObjectBlobGuid.ToString(eHyphensAndCurlyBraces)
        << "ObjectGuid" << oObjectGuid.ToString(eHyphensAndCurlyBraces)
        << "ObjectType" << GuidObjectType::eDatasetFamily
        << finalize;

        // Each client and transaction can only be used in a single thread
        mongocxx::pool::entry oClient = m_poMongoPool->acquire();
        // Access SailDatabase
        mongocxx::database oSailDatabase = (*oClient)["SailDatabase"];
        // Access Dataset Family collection
        mongocxx::collection oDataFederationCollection = oSailDatabase["DataFederation"];

        // Create a transaction callback
        mongocxx::client_session::with_transaction_cb oCallback = [&](mongocxx::client_session * poSession) 
        {
            // Insert document in the Dataset family collection
            auto oResult = oDataFederationCollection.insert_one(*poSession, oDataFederationDocumentView.view());
            if (!oResult) {
                std::cout << "Error while writing to the database." << std::endl;
            }
            else
            {
                // Access Object collection
                mongocxx::collection oObjectCollection = oSailDatabase["Object"];
                // Insert document in the Object collection
                oResult = oObjectCollection.insert_one(*poSession, oObjectDocumentValue.view());
                if (!oResult) {
                    std::cout << "Error while writing to the database." << std::endl;
                }
                else
                {
                    // Access PlainTextObjectBlob collection
                    mongocxx::collection oPlainTextObjectCollection = oSailDatabase["PlainTextObjectBlob"];
                    // Insert document in the PlainTextObjectBlob collection
                    oResult = oPlainTextObjectCollection.insert_one(*poSession, oPlainTextObjectDocumentValue.view());
                    if (!oResult) {
                        std::cout << "Error while writing to the database." << std::endl;
                    }
                    else
                    {
                        dwStatus = 201;
                    }
                }
            }
        };

        // Create a session and start the transaction
        mongocxx::client_session oSession = oClient->start_session();
        try
        {
            oSession.with_transaction(oCallback);
        }
        catch (mongocxx::exception& e)
        {
            std::cout << "Collection transaction exception: " << e.what() << std::endl;
        }

    }
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    // Send back the status of the transaction
    oResponse.PutDword("Status", dwStatus);

    return oResponse.GetSerializedBuffer();
}

/********************************************************************************************
 *
 * @class DatabaseManager
 * @function ListDataFederations
 * @brief List the data federations that are active in the database
 * @param[in] c_oRequest contains the information for the new data federation
 * @throw BaseException Error StructuredBuffer element not found
 * @returns Serialized StructuredBuffer containing the response
 *
 ********************************************************************************************/
std::vector<Byte> __thiscall DatabaseManager::ListActiveDataFederations(
    _in const StructuredBuffer & c_oRequest
    )
{
    __DebugFunction();

    StructuredBuffer oResponse;
    Dword dwStatus;

    // Each client and transaction can only be used in a single thread
    mongocxx::pool::entry oClient = m_poMongoPool->acquire();
    // Access SailDatabase
    mongocxx::database oSailDatabase = (*oClient)["SailDatabase"];
    // Fetch all digital contract records associated with a researcher's or data owner's organization
    mongocxx::cursor oDatasetFamilyRecords = oSailDatabase["DataFederation"].find({});
    Guid oRequestingUserOrganization = c_oRequest.GetGuid("RequestingUserOrganizationIdentifier");
    // Loop through returned documents and add information to the list
    StructuredBuffer oListOfDataFederations;
    try
    {
        for (auto&& oDocumentView : oDatasetFamilyRecords)
        {
            bsoncxx::document::element oDataFederationIdentifier = oDocumentView["DataFederationIdentifier"];
            bsoncxx::document::element oDataFederationOwnerIdentifier = oDocumentView["DataFederationOwnerOrganizationIdentifier"];
            if ((oDataFederationIdentifier && (type::k_utf8 == oDataFederationIdentifier.type()))
                && (oDataFederationOwnerIdentifier && (type::k_utf8 == oDataFederationOwnerIdentifier.type())))
            {
                std::string strDataFederationIdentifier = oDataFederationIdentifier.get_utf8().value.to_string();
                std::string strDataFederationOwnerIdentifier = oDataFederationOwnerIdentifier.get_utf8().value.to_string();

                bsoncxx::document::element oPlainTextObjectBlobGuid = oDocumentView["PlainTextObjectBlobGuid"];
                if (oPlainTextObjectBlobGuid && (type::k_utf8 == oPlainTextObjectBlobGuid.type()))
                {
                    std::string strPlainTextObjectBlobGuid = oPlainTextObjectBlobGuid.get_utf8().value.to_string();
                    bsoncxx::stdx::optional<bsoncxx::document::value> oPlainTextObjectBlobDocument = oSailDatabase["PlainTextObjectBlob"].find_one(document{}
                                                                                                                                                << "PlainTextObjectBlobGuid" << strPlainTextObjectBlobGuid
                                                                                                                                                << finalize);

                    if (bsoncxx::stdx::nullopt != oPlainTextObjectBlobDocument)
                    {
                        bsoncxx::document::element oObjectGuid = oPlainTextObjectBlobDocument->view()["ObjectGuid"];
                        if (oObjectGuid && (type::k_utf8 == oObjectGuid.type()))
                        {
                            std::string strObjectGuid = oObjectGuid.get_utf8().value.to_string();
                            bsoncxx::stdx::optional<bsoncxx::document::value> oObjectDocument = oSailDatabase["Object"].find_one(document{} << "ObjectGuid" << strObjectGuid << finalize);
                            if (bsoncxx::stdx::nullopt != oObjectDocument)
                            {
                                bsoncxx::document::element oObjectBlob = oObjectDocument->view()["ObjectBlob"];
                                if (oObjectBlob && oObjectBlob.type() == type::k_binary)
                                {
                                    StructuredBuffer oFederationObject(oObjectBlob.get_binary().bytes, oObjectBlob.get_binary().size);
                                    // Only return federations that are active, and the user belongs to or created
                                    DataFederation oDataFederation(oFederationObject);
                                    if ( (true == oDataFederation.IsActive()) && 
                                        (true == oDataFederation.IsOrganizationInFederation(oRequestingUserOrganization)) )
                                    {
                                        StructuredBuffer oDataFederationInformation;
                                        oDataFederationInformation.PutString("Name", oDataFederation.Name());
                                        oDataFederationInformation.PutString("Description", oDataFederation.Description());
                                        oDataFederationInformation.PutString("Identifier", oDataFederation.Identifier().ToString(eHyphensAndCurlyBraces));
                                        oDataFederationInformation.PutString("OrganizationIdentifier", oDataFederation.OrganizationOwnerIdentifier().ToString(eHyphensAndCurlyBraces));

                                        StructuredBuffer oOrganizationName = this->GetOrganizationName(oDataFederation.OrganizationOwnerIdentifier().ToString(eHyphensAndCurlyBraces));
                                        if ( 200 == oOrganizationName.GetDword("Status") )
                                        {
                                            oDataFederationInformation.PutString("OrganizationName", oOrganizationName.GetString("OrganizationName"));
                                        }
                                        else
                                        {
                                            oDataFederationInformation.PutString("OrganizationName", "");
                                        }
                                        // Build a list of submitter names + guids for readability
                                        StructuredBuffer oNamedSubmitters;
                                        for ( auto oSubmitterIdentifier : oDataFederation.DataSubmitterOrganizations() )
                                        {
                                            StructuredBuffer oOrganizationName = this->GetOrganizationName(oSubmitterIdentifier.ToString(eHyphensAndCurlyBraces));
                                            std::string strOrganizationName{""};
                                            if ( 200 == oOrganizationName.GetDword("Status") )
                                            {
                                                strOrganizationName = oOrganizationName.GetString("OrganizationName");
                                            }
                                            oNamedSubmitters.PutString(oSubmitterIdentifier.ToString(eHyphensAndCurlyBraces).c_str(), strOrganizationName);
                                        }
                                        oDataFederationInformation.PutStructuredBuffer("DataSubmitterOrganizations", oNamedSubmitters);

                                        // Build a list of submitter names + guids for readability
                                        StructuredBuffer oNamedResearchers;
                                        for ( auto oResearcherIdentifier : oDataFederation.ResearchOrganizations() )
                                        {
                                            StructuredBuffer oOrganizationName = this->GetOrganizationName(oResearcherIdentifier.ToString(eHyphensAndCurlyBraces));
                                            std::string strOrganizationName{""};
                                            if ( 200 == oOrganizationName.GetDword("Status") )
                                            {
                                                strOrganizationName = oOrganizationName.GetString("OrganizationName");
                                            }
                                            oNamedResearchers.PutString(oResearcherIdentifier.ToString(eHyphensAndCurlyBraces).c_str(), strOrganizationName);
                                        }
                                        oDataFederationInformation.PutStructuredBuffer("ResearcherOrganizations", oNamedResearchers);

                                        StructuredBuffer oNamedDatasetFamilies;
                                        for ( auto oDatasetFamilyIdentifier : oDataFederation.DatasetFamilies() )
                                        {
                                            oNamedDatasetFamilies.PutString(oDatasetFamilyIdentifier.ToString(eHyphensAndCurlyBraces).c_str(), this->GetDatasetFamilyTitle(oDatasetFamilyIdentifier));
                                        }
                                        oDataFederationInformation.PutStructuredBuffer("DatasetFamilies", oNamedDatasetFamilies);
                                        oListOfDataFederations.PutStructuredBuffer(strDataFederationIdentifier.c_str(), oDataFederationInformation);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oResponse.Clear();
    }
    catch(std::exception & c_oException)
    {
        std::cout << "Exception: " << c_oException.what() << '\n';
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }
    oResponse.PutStructuredBuffer("DataFederations", oListOfDataFederations);
    dwStatus = 200;
    oResponse.PutDword("Status", dwStatus);

    return oResponse.GetSerializedBuffer();
}

/********************************************************************************************
 *
 * @class DatabaseManager
 * @function PullDataFederation
 * @brief Pull a data federation object based on its identifier
 * @param[in] Guid - the identifier for the data federation
 * @throw BaseException Error StructuredBuffer element not found
 * @returns Serialized StructuredBuffer containing the response
 *
 ********************************************************************************************/
std::optional<DataFederation> __thiscall DatabaseManager::PullDataFederationObject(
    _in const Guid& c_oIdentifier
    )
{
    __DebugFunction();
    std::optional<DataFederation> oDataFederation;

    Dword dwStatus{404};
    StructuredBuffer oResponse;

    try
    {

        // Each client and transaction can only be used in a single thread
        mongocxx::pool::entry oClient = m_poMongoPool->acquire();
        // Access SailDatabase
        mongocxx::database oSailDatabase = (*oClient)["SailDatabase"];
        bsoncxx::stdx::optional<bsoncxx::document::value> oDataFederationDocument = oSailDatabase["DataFederation"].find_one(document{}
                                                                                                                << "DataFederationIdentifier" << c_oIdentifier.ToString(eHyphensAndCurlyBraces)
                                                                                                                << finalize);

        if (bsoncxx::stdx::nullopt != oDataFederationDocument)
        {
            bsoncxx::document::element oPlainTextObjectBlobGuid = oDataFederationDocument->view()["PlainTextObjectBlobGuid"];
            if ( oPlainTextObjectBlobGuid && (type::k_utf8 == oPlainTextObjectBlobGuid.type()))
            {
                std::string strPlainTextObjectBlobGuid = oPlainTextObjectBlobGuid.get_utf8().value.to_string();
                bsoncxx::stdx::optional<bsoncxx::document::value> oPlainTextObjectBlobDocument = oSailDatabase["PlainTextObjectBlob"].find_one(document{}
                                                                                                                                               << "PlainTextObjectBlobGuid" << strPlainTextObjectBlobGuid
                                                                                                                                               << finalize);
                if (bsoncxx::stdx::nullopt != oPlainTextObjectBlobDocument)
                {
                    bsoncxx::document::element oObjectGuid = oPlainTextObjectBlobDocument->view()["ObjectGuid"];
                    if (oObjectGuid && (type::k_utf8 == oObjectGuid.type()))
                    {
                        std::string strObjectGuid = oObjectGuid.get_utf8().value.to_string();
                        bsoncxx::stdx::optional<bsoncxx::document::value> oObjectDocument = oSailDatabase["Object"].find_one(document{} << "ObjectGuid" << strObjectGuid << finalize);
                        if (bsoncxx::stdx::nullopt != oObjectDocument)
                        {
                            mongocxx::client_session::with_transaction_cb oCallback = [&](mongocxx::client_session * poSession)
                            {
                                bsoncxx::document::element oObjectBlob = oObjectDocument->view()["ObjectBlob"];
                                if (oObjectBlob && (type::k_binary == oObjectBlob.type()))
                                {
                                    StructuredBuffer oObject(oObjectBlob.get_binary().bytes, oObjectBlob.get_binary().size);
                                    oDataFederation.emplace(DataFederation{oObject});
                                }
                            };

                            mongocxx::client_session oSession = oClient->start_session();
                            try
                            {
                                oSession.with_transaction(oCallback);
                            }
                            catch (mongocxx::exception &e)
                            {
                                std::cout << "Collection transaction exception: " << e.what() << std::endl;
                            }
                        }
                    }
                }
            }
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    catch(std::exception & c_oException)
    {
        std::cout << "Exception: " << c_oException.what() << '\n';
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    return oDataFederation;
}

/********************************************************************************************
 *
 * @class DatabaseManager
 * @function SoftDeleteDataFederation
 * @brief Soft Delete the data federation from the database
 * @param[in] c_oRequest contains dataset guid
 * @throw BaseException Error StructuredBuffer element not found
 * @returns Status of the transaction
 *
 ********************************************************************************************/
std::vector<Byte> __thiscall DatabaseManager::SoftDeleteDataFederation(
    _in const StructuredBuffer & c_oRequest
    )
{
    __DebugFunction();

    StructuredBuffer oResponse;
    Dword dwStatus = 404;

    try 
    {
        std::optional<DataFederation> oDataFederation = this->PullDataFederationObject(c_oRequest.GetGuid("DataFederationIdentifier"));

        if (true == oDataFederation.has_value())
        {
            // The requesting user owns this federation
            if ( c_oRequest.GetGuid("RequestingUserOrganizationIdentifier") == oDataFederation.value().OrganizationOwnerIdentifier() )
            {
                oDataFederation.value().SetInactive();
                std::cout << "Set federation " << oDataFederation.value().Identifier().ToString(eHyphensAndCurlyBraces) << " to inactive " << std::endl;
                // Save this federation back to the database
                UpdateDataFederationObject(oDataFederation.value());
                dwStatus = 200;
            }
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    catch(std::exception & c_oException)
    {
        std::cout << "Exception: " << c_oException.what() << '\n';
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    oResponse.PutDword("Status", dwStatus);

    return oResponse.GetSerializedBuffer();
}

/********************************************************************************************
 *
 * @class DatabaseManager
 * @function UpdateDataFederation
 * @brief Update a data federation object in the database
 * @param[in] DataFederation - The data federation object to update
 * @returns bool - True if we could store the Data Federation, false otherwise
 *
 ********************************************************************************************/
bool __thiscall DatabaseManager::UpdateDataFederationObject(
    _in const DataFederation & c_oDataFederation
    )
{
    __DebugFunction();
    bool fStatus{false};

    try
    {
        StructuredBuffer oDataFederationStructuredBuffer = c_oDataFederation.ToStructuredBuffer();

        // Each client and transaction can only be used in a single thread
        mongocxx::pool::entry oClient = m_poMongoPool->acquire();
        // Access SailDatabase
        mongocxx::database oSailDatabase = (*oClient)["SailDatabase"];
        bsoncxx::stdx::optional<bsoncxx::document::value> oDataFederationDocument = oSailDatabase["DataFederation"].find_one(document{}
                                                                                                                << "DataFederationIdentifier" << c_oDataFederation.Identifier().ToString(eHyphensAndCurlyBraces)
                                                                                                                << finalize);

        if (bsoncxx::stdx::nullopt != oDataFederationDocument)
        {
            bsoncxx::document::element oPlainTextObjectBlobGuid = oDataFederationDocument->view()["PlainTextObjectBlobGuid"];
            if (oPlainTextObjectBlobGuid && (type::k_utf8 == oPlainTextObjectBlobGuid.type()))
            {
                std::string strPlainTextObjectBlobGuid = oPlainTextObjectBlobGuid.get_utf8().value.to_string();
                bsoncxx::stdx::optional<bsoncxx::document::value> oPlainTextObjectBlobDocument = oSailDatabase["PlainTextObjectBlob"].find_one(document{}
                                                                                                                                               << "PlainTextObjectBlobGuid" << strPlainTextObjectBlobGuid
                                                                                                                                               << finalize);
                if (bsoncxx::stdx::nullopt != oPlainTextObjectBlobDocument)
                {
                    bsoncxx::document::element oObjectGuid = oPlainTextObjectBlobDocument->view()["ObjectGuid"];
                    if (oObjectGuid && (type::k_utf8 ==  oObjectGuid.type()))
                    {
                        std::string strObjectGuid = oObjectGuid.get_utf8().value.to_string();
                        bsoncxx::stdx::optional<bsoncxx::document::value> oObjectDocument = oSailDatabase["Object"].find_one(document{} << "ObjectGuid" << strObjectGuid << finalize);
                        if (bsoncxx::stdx::nullopt != oObjectDocument)
                        {
                            mongocxx::client_session::with_transaction_cb oCallback = [&](mongocxx::client_session *poSession)
                            {
                                bsoncxx::document::element oObjectBlob = oObjectDocument->view()["ObjectBlob"];
                                if (oObjectBlob && (type::k_binary ==  oObjectBlob.type()))
                                {
                                    // Write the serialized structured buffer to a blob
                                    bsoncxx::types::b_binary oNewObjectBlob{
                                        bsoncxx::binary_sub_type::k_binary,
                                        uint32_t(oDataFederationStructuredBuffer.GetSerializedBufferRawDataSizeInBytes()),
                                        oDataFederationStructuredBuffer.GetSerializedBufferRawDataPtr()};

                                    // Update the object blob in the database
                                    oSailDatabase["Object"].update_one(*poSession, document{} << "ObjectGuid" << strObjectGuid << finalize,
                                                                    document{} << "$set" << open_document << "ObjectBlob" << oNewObjectBlob << close_document << finalize);
                                }
                            };

                            mongocxx::client_session oSession = oClient->start_session();
                            try
                            {
                                oSession.with_transaction(oCallback);
                                fStatus = true;
                            }
                            catch (mongocxx::exception &e)
                            {
                                std::cout << "Collection transaction exception: " << e.what() << std::endl;
                            }
                        }
                    }
                }
            }
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
    }

    catch(std::exception & c_oException)
    {
        std::cout << "Exception: " << c_oException.what() << '\n';
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    return fStatus;
}

/********************************************************************************************
 *
 * @class DatabaseManager
 * @function PullDataFederation
 * @brief Handle an API request to pull a Data Federation
 * @param[in] Structuredbuffer - the identifier for the data federation
 * @throw BaseException Error StructuredBuffer element not found
 * @returns Serialized StructuredBuffer containing the response
 *
 ********************************************************************************************/
std::vector<Byte> __thiscall DatabaseManager::PullDataFederation(
    _in const StructuredBuffer & c_oRequest
    )
{
    __DebugFunction();

    std::optional<DataFederation> oDataFederation;
    StructuredBuffer oResponse;
    Dword dwStatus{404};

    try
    {
        oDataFederation = this->PullDataFederationObject(c_oRequest.GetGuid("DataFederationIdentifier"));
        if ( true == oDataFederation.has_value() )
        {
            oResponse.PutStructuredBuffer("DataFederation", oDataFederation.value().ToStructuredBuffer());
            dwStatus = 200;
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    catch(std::exception & c_oException)
    {
        std::cout << "Exception: " << c_oException.what() << '\n';
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    oResponse.PutDword("Status", dwStatus);

    return oResponse.GetSerializedBuffer();
}

/********************************************************************************************
 *
 * @class DatabaseManager
 * @function PullDataFederation
 * @brief Handle an API request to pull a Data Federation
 * @param[in] Structuredbuffer - the identifier for the data federation
 * @throw BaseException Error StructuredBuffer element not found
 * @returns Serialized StructuredBuffer containing the response
 *
 ********************************************************************************************/
std::vector<Byte> __thiscall DatabaseManager::UpdateDataFederation(
    _in const StructuredBuffer & c_oRequest
    )
{
    __DebugFunction();

    std::optional<DataFederation> oDataFederation;
    StructuredBuffer oResponse;
    Dword dwStatus{404};

    try
    {
        DataFederation oDataFederation{c_oRequest.GetStructuredBuffer("DataFederation")};
        if ( true == this->UpdateDataFederationObject(oDataFederation) )
        {
            dwStatus = 200;
        }
    }

    catch (const BaseException & c_oBaseException)
    {
        ::RegisterBaseException(c_oBaseException, __func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    catch(std::exception & c_oException)
    {
        std::cout << "Exception: " << c_oException.what() << '\n';
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
    }

    catch (...)
    {
        ::RegisterUnknownException(__func__, __FILE__, __LINE__);
        oResponse.Clear();
    }

    oResponse.PutDword("Status", dwStatus);

    return oResponse.GetSerializedBuffer();
}
