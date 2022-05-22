/*********************************************************************************************
 *
 * @file DatasetReInitializer.h
 * @author Luis Miguel Huapaya
 * @date 23 March 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "Guid.h"
#include "Object.h"
#include "StructuredBuffer.h"

#include <string>
#include <vector>

class DatasetReInitializer : public Object
{
    public:

        DatasetReInitializer(
            _in const std::string & c_strDatasetFilename
            );
        virtual ~DatasetReInitializer(void);

        void __thiscall SetDatasetIdentifier(
            _in const Guid & c_oDatasetIdentifier
            );
        void __thiscall SetCorporateIdentifier(
            _in const Guid & c_oCorporateIdentifier
            );
        void __thiscall ResetUtcEpochPublishDate(void);
        void __thiscall SetDatasetName(
            _in const std::string c_strDatasetTitle
            );
        void __thiscall SetDatasetDescription(
            _in const std::string c_strDatasetDescription
            );
        void __thiscall SetDatasetKeywords(
            _in const std::string c_strDatasetKeywords
            );
        void __thiscall SetDatasetFamily(
            _in const std::string c_strDatasetFamily
            );
        void __thiscall RemoveDatasetFamily(void);

        Guid __thiscall GetDatasetIdentifier(void) const;
        std::vector<Byte> __thiscall GetSerializedDatasetMetadata(void) const;

        void __thiscall SaveDatasetUpdates(void) const;

    private:

        std::string m_strOriginalDatasetFilename;
        StructuredBuffer m_oOriginalDatasetMetadata;
        StructuredBuffer m_oUpdatedDatasetMetadata;
};
