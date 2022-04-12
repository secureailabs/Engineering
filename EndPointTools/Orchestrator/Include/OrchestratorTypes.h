/*********************************************************************************************
 *
 * @file OrchestratorTypes.h
 * @author David Gascon
 * @date 20 Jan 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Types related for the orchestrator talking to the job engine
 *
 ********************************************************************************************/

#include <utility>
#include "Guid.h"

#pragma once

enum class EngineRequest
{
    eVmShutdown = 0,
    ePushSafeObject = 1,
    eSubmitJob = 2,
    ePullData = 3,
    ePushdata = 4,
    eSetParameters = 5,
    eHaltAllJobs = 6,
    eJobStatusSignal = 7,
    eConnectVirtualMachine = 8,
    eHeartBeatPong = 9
};

enum class JobStatusSignals
{
    eJobStart = 0,
    eJobDone = 1,
    eJobFail = 2,
    ePostValue = 3,
    eVmShutdown = 4,
    ePrivacyViolation = 5,
    eHeartBeatPing = 6
};
