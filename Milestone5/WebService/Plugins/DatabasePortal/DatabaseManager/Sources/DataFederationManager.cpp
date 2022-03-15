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
 * @brief Save a Dataset family in the database
 * @param[in] c_oRequest contains the information for the new dataset
 * @throw BaseException Error StructuredBuffer element not found
 * @returns Serialized StructuredBuffer containing the response
 *
 ********************************************************************************************/
// Register a dataset family
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
        << "DataFederationOwnerOrganizationIdentifier" << oObject.GetGuid("DataFederationOwnerIdentifier").ToString(eHyphensAndCurlyBraces)
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
