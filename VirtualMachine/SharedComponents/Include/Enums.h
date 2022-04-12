/*********************************************************************************************
 *
 * @file Enums.h
 * @author Prawal Gangwar
 * @date 2 April 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

const std::string gc_strCommunicationPortalAddress = "{3d14320b-c7bd-4496-81b3-90a4a703af93}";

enum CSVRequest
{
    eGetRowRange,
    eGetColumnRange,
    eGetTable,
    eGetDatasetMetadata,
    eGetTableMetadata,
    eCloseFile,
    eGetUuids
};
