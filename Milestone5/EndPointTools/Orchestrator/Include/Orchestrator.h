/*********************************************************************************************
 *
 * @file Orchestrator.h
 * @author David Gascon & Jingwei Zhang
 * @date 15 Jan 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "EntityTypes.h"
#include "EosbRotationManager.h"
#include "JobEngineConnection.h"
#include "JobInformation.h"
#include "SecureNodeInformation.h"
#include "StructuredBuffer.h"
#include "StructuredBufferLockedQueue.h"
#include "SafeObject.h"
#include "TableInformation.h"
#include "TlsNode.h"
#include "TlsServer.h"
#include <set>
#include <string>
#include <stack>
#include <map>
#include <unordered_map>
#include <memory>
#include <future>
#include <unordered_set>

/********************************************************************************************/


class Orchestrator : public Object{

    public:

        Orchestrator(void);

        Orchestrator(
            _in const Orchestrator& c_oFrontend
        ) = delete;
        Orchestrator& operator= (
            _in const Orchestrator&
        ) = delete;
        virtual ~Orchestrator(void);

        unsigned int __thiscall Login(
            _in const std::string& c_strEmail,
            _in const std::string& c_strUserPassword,
            _in const int c_wordServerPort,
            _in const std::string& c_strServerIPAddress
        );

        std::string __thiscall GetCurrentEosb(void) const;

        void __thiscall ExitCurrentSession(void);

        std::string __thiscall GetSafeFunctions(void) const;

        std::string GetDatasets(void) const;

        int __thiscall LoadSafeObjects(
            _in const std::string& c_strSafeObjectDirectory
        );

        std::string __thiscall GetDigitalContracts(void) const;

        std::string __thiscall GetTables(void) const;

        std::string __thiscall ProvisionSecureComputationalNode(
            _in const std::string & c_strDigitalContractGUID,
            _in const std::string & c_strDatasetGUID,
            _in const std::string & c_strVmType
            );

        std::string __thiscall RunJob(
            _in const std::string & c_strSafeFuncionGUID
            );

        std::string __thiscall GetJobStatus(
            _in const std::string & c_strJobGUID
            ) const;

        std::string __thiscall SetParameter(
            _in const std::string& strJobId,
            _in const std::string& strInputParamId,
            _in const std::string& strParamValue
            );

        std::string __thiscall PushUserData(
            _in const std::vector<Byte>& c_stlIncomingData
            );

        std::string __thiscall WaitForAllSecureNodesToBeProvisioned(
            _in int nTimeoutInMs
            );

        std::string __thiscall PullJobData(
            _in const std::string& c_strOutputParameter
            ) throw();

        std::string __thiscall WaitForData(
            _in int nTimeoutInMs
            ) throw();

        void __thiscall SendDataToJobEngine(
            _in const std::string& strVMID,
            _in StructuredBuffer & c_oStructuredBuffer
        );

        std::string __thiscall GetIPAddressForJob(
            _in const std::string& c_strJobGUID
            );

        bool __thiscall DeprovisionDigitalContract(
            _in const std::string& c_strDigitalContractGUID
            );

    private:
        void __thiscall CacheDigitalContractsFromRemote(
            _in const std::string& c_strServerIpAddress,
            _in unsigned long unServerPort
        );
       void __thiscall CacheDatasetsFromRemote(
            _in const std::string& c_strServerIpAddress,
            _in unsigned long unServerPort
        );

        std::optional<Guid> __thiscall GetSecureComputationalNodeServingDataset(
            _in const Guid& oDatasetGuid
            ) const;

       std::optional<Guid> __thiscall GetSecureComputationalNodeServingTable(
            _in const Guid& oDatasetGuid
            ) const;

        std::optional<Guid> GetSecureComputationalNodeWithoutDataset() const;

        void UpdateJobIPAddressForAnySecureComputationalNode(
            _in JobInformation& oJob
            );

        void __thiscall SendDataToJob(
            _in JobInformation& c_oJob,
            _in const StructuredBuffer& c_oStructuredBuffer
            );

        void __thiscall PushUserDataToJob(
            _in JobInformation& oJob,
            _in Guid& oUserParameter
            );

        void __thiscall SendSafeObjectToJobEngine(
            _in JobInformation& oJob
            );

        void __thiscall SetParameterOnJob(
            _in JobInformation& oJob,
            _in Guid& oParameterGuid,
            _in Guid& oParameterValueGuid
            );

        void __thiscall SetJobParameterForJobOutput(
            _in JobInformation& oJob,
            _in Guid& oParameterGuid,
            _in std::string& strParameterValue
            );

        void __thiscall PushJobOutputParameterToJob(
            _in JobInformation& oJob,
            _in const std::string& strParameterIdentifier,
            _in const std::vector<Byte>& oOutputParameterData
            );

        void __thiscall UpdateJobsWaitingForData(
            _in const StructuredBuffer& oPushDataMessage
            );

        bool __thiscall StartJobRemoteExecution(
            _in JobInformation& oJob
            ) throw();

        void __thiscall UpdateJobIPAddressForParameter(
            _in JobInformation& oJob,
            _in const Guid& oParameterGuid
            );

        VirtualMachineState __thiscall GetSecureComputationNodeInformation(
            _in const Guid& oSecureNodeGuid
            );

        void __thiscall SubmitJob(
            _in JobInformation& oJob
            );


        std::set<std::string> m_stlOutstandingImplicitPullRequests{};
        EosbRotationManager m_oEosbRotator{};
        std::unordered_map<std::string, StructuredBuffer> m_stlAvailableSafeFunctions{};
        std::unordered_map<std::string, StructuredBuffer> m_stlDigitalContracts{};
        std::unordered_map<std::string, StructuredBuffer> m_stlAvailableDatasets{};
        std::unordered_map<std::string, TableInformation> m_stlAvailableTables{};
        std::unordered_map<std::string, SecureNodeInformation> m_stlProvisionInformation{};
        std::unordered_map<std::string, std::unique_ptr<JobInformation> > m_stlJobInformation{};
        std::unordered_map<std::string, std::vector<Byte>> m_stlPushedData{};
        std::unordered_map<std::string, std::vector<Byte>> m_stlJobResults{};
        std::unordered_map<std::string, std::shared_ptr<JobEngineConnection>> m_stlSecureNodeConnections{};
        StructuredBufferLockedQueue m_oJobMessageQueue{};
        const Guid m_oOrchestratorIdentifier{eOrchestratorIdentifier};
};
