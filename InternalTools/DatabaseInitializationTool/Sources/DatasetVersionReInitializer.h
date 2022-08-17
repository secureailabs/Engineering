/*********************************************************************************************
 *
 * @file DatasetVersionReInitializer.h
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

class DatasetVersionReInitializer : public Object
{
    public:

        DatasetVersionReInitializer(
            _in const std::string & c_strDatasetVersionFilename
            );
        virtual ~DatasetVersionReInitializer(void);

        void __thiscall SetDatasetVersionIdentifier(
            _in const Guid & c_oDatasetVersionIdentifier
            );
        void __thiscall SetCorporateIdentifier(
            _in const Guid & c_oCorporateIdentifier
            );
        void __thiscall ResetUtcEpochPublishDate(void);
        void __thiscall SetDatasetVersionName(
            _in const std::string c_strDatasetVersionTitle
            );
        void __thiscall SetDatasetVersionDescription(
            _in const std::string c_strDatasetVersionDescription
            );
        void __thiscall SetDatasetVersionKeywords(
            _in const std::string c_strDatasetVersionKeywords
            );
        void __thiscall SetDatasetFamily(
            _in const std::string c_strDatasetFamily
            );
        void __thiscall RemoveDatasetFamily(void);

        Guid __thiscall GetDatasetVersionIdentifier(void) const;
        std::vector<Byte> __thiscall GetSerializedDatasetVersionMetadata(void) const;

        void __thiscall SaveDatasetVersionUpdates(void) const;

    private:

        std::string m_strOriginalDatasetVersionFilename;
        StructuredBuffer m_oOriginalDatasetVersionMetadata;
        StructuredBuffer m_oUpdatedDatasetVersionMetadata;
};
