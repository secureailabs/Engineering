/*********************************************************************************************
 *
 * @file DataFederationManager.cpp
 * @author David Gascon
 * @date 14 March 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 * @brief
 ********************************************************************************************/

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

    // Loop through returned documents and add information to the list
    StructuredBuffer oListOfDataFederations;
    try
    {
        for (auto&& oDocumentView : oDatasetFamilyRecords)
        {
            bsoncxx::document::element oDataFederationIdentifier = oDocumentView["DataFederationIdentifier"];
            bsoncxx::document::element oDataFederationOwnerIdentifier = oDocumentView["DataFederationOwnerOrganizationIdentifier"];
            if ((oDataFederationIdentifier && oDataFederationIdentifier.type() == type::k_utf8) && (oDataFederationOwnerIdentifier && oDataFederationOwnerIdentifier.type() == type::k_utf8) )
            {
                std::string strDataFederationIdentifier = oDataFederationIdentifier.get_utf8().value.to_string();
                std::string strDataFederationOwnerIdentifier = oDataFederationOwnerIdentifier.get_utf8().value.to_string();

                bsoncxx::document::element oPlainTextObjectBlobGuid = oDocumentView["PlainTextObjectBlobGuid"];
                if (oPlainTextObjectBlobGuid && oPlainTextObjectBlobGuid.type() == type::k_utf8)
                {
                    std::string strPlainTextObjectBlobGuid = oPlainTextObjectBlobGuid.get_utf8().value.to_string();
                    bsoncxx::stdx::optional<bsoncxx::document::value> oPlainTextObjectBlobDocument = oSailDatabase["PlainTextObjectBlob"].find_one(document{}
                                                                                                                                                << "PlainTextObjectBlobGuid" << strPlainTextObjectBlobGuid
                                                                                                                                                << finalize);

                    if (bsoncxx::stdx::nullopt != oPlainTextObjectBlobDocument)
                    {
                        bsoncxx::document::element oObjectGuid = oPlainTextObjectBlobDocument->view()["ObjectGuid"];
                        if (oObjectGuid && oObjectGuid.type() == type::k_utf8)
                        {
                            std::string strObjectGuid = oObjectGuid.get_utf8().value.to_string();
                            bsoncxx::stdx::optional<bsoncxx::document::value> oObjectDocument = oSailDatabase["Object"].find_one(document{} << "ObjectGuid" << strObjectGuid << finalize);
                            if (bsoncxx::stdx::nullopt != oObjectDocument)
                            {
                                bsoncxx::document::element oObjectBlob = oObjectDocument->view()["ObjectBlob"];
                                if (oObjectBlob && oObjectBlob.type() == type::k_binary)
                                {
                                    StructuredBuffer oObject(oObjectBlob.get_binary().bytes, oObjectBlob.get_binary().size);
                                    // Only return federations that are active
                                    if ( true == oObject.GetBoolean("DataFederationActive"))
                                    {
                                        StructuredBuffer oDataFederationInformation;
                                        oDataFederationInformation.PutString("Name", oObject.GetString("DataFederationName"));
                                        oDataFederationInformation.PutString("Description", oObject.GetString("DataFederationDescription"));
                                        oDataFederationInformation.PutString("Identifier", oObject.GetGuid("DataFederationIdentifier").ToString(eHyphensAndCurlyBraces));
                                        oDataFederationInformation.PutString("OrganizationIdentifier", oObject.GetGuid("DataFederationOwnerOrganizationIdentifier").ToString(eHyphensAndCurlyBraces));

                                        StructuredBuffer oOrganizationName = this->GetOrganizationName(oDataFederationInformation.GetString("OrganizationIdentifier"));
                                        if ( 200 == oOrganizationName.GetDword("Status") )
                                        {
                                            oDataFederationInformation.PutString("OrganizationName", oOrganizationName.GetString("OrganizationName"));
                                        }
                                        else
                                        {
                                            oDataFederationInformation.PutString("OrganizationName", "");
                                        }
                                        StructuredBuffer oDataFederationSubmitters = oObject.GetStructuredBuffer("DataFederationDataSubmitterList");
                                        StructuredBuffer oNamedSubmitters;
                                        for ( auto strName : oDataFederationSubmitters.GetNamesOfElements() )
                                        {
                                            Guid oOrganizationGuid = oDataFederationSubmitters.GetGuid(strName.c_str());
                                            StructuredBuffer oOrganizationName = this->GetOrganizationName(oOrganizationGuid.ToString(eHyphensAndCurlyBraces));
                                            std::string strOrganizationName{""};
                                            if ( 200 == oOrganizationName.GetDword("Status") )
                                            {
                                                strOrganizationName = oOrganizationName.GetString("OrganizationName");
                                            }
                                            oNamedSubmitters.PutString(oOrganizationGuid.ToString(eHyphensAndCurlyBraces).c_str(), strOrganizationName);
                                        }
                                        oDataFederationInformation.PutStructuredBuffer("DataSubmitterOrganizations", oNamedSubmitters);

                                        StructuredBuffer oDataFederationResearchers = oObject.GetStructuredBuffer("DataFederationResearcherList");
                                        StructuredBuffer oNamedResearchers;
                                        for ( auto strName : oDataFederationResearchers.GetNamesOfElements() )
                                        {
                                            Guid oOrganizationGuid = oDataFederationResearchers.GetGuid(strName.c_str());
                                            StructuredBuffer oOrganizationName = this->GetOrganizationName(oOrganizationGuid.ToString(eHyphensAndCurlyBraces));
                                            std::string strOrganizationName{""};
                                            if ( 200 == oOrganizationName.GetDword("Status") )
                                            {
                                                strOrganizationName = oOrganizationName.GetString("OrganizationName");
                                            }
                                            oNamedResearchers.PutString(oOrganizationGuid.ToString(eHyphensAndCurlyBraces).c_str(), strOrganizationName);
                                        }
                                        oDataFederationInformation.PutStructuredBuffer("ResearcherOrganizations", oNamedResearchers);

                                        StructuredBuffer oDataFederationDatasetFamilies = oObject.GetStructuredBuffer("DataFederationDatasetFamilyList");
                                        StructuredBuffer oNamedDatasetFamilies;
                                        for ( auto strName : oDataFederationDatasetFamilies.GetNamesOfElements() )
                                        {
                                            Guid oDatasetFamiliyIdentifier = oDataFederationDatasetFamilies.GetGuid(strName.c_str());
                                            std::string strDatasetFamilyName = this->GetDatasetFamilyTitle(oDatasetFamiliyIdentifier);
                                            oNamedDatasetFamilies.PutString(oDatasetFamiliyIdentifier.ToString(eHyphensAndCurlyBraces).c_str(), strDatasetFamilyName);
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
    catch(std::exception & e)
    {
        std::cout << "Exception: " << e.what() << '\n';
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
