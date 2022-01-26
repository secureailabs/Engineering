/*********************************************************************************************
 *
 * @file frontend.h
 * @author Jingwei Zhang
 * @date 15 Jan 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "EntityTypes.h"
#include "EosbRotationManager.h"
#include "JobInformation.h"
#include "SecureNodeInformation.h"
#include "StructuredBuffer.h"
#include "StructuredBufferLockedQueue.h"
#include "SafeObject.h"
#include "TableInformation.h"
#include "TlsNode.h"
#include "TlsServer.h"
#include <string>
#include <stack>
#include <map>
#include <unordered_map>
#include <memory>
#include <future>
#include <unordered_set>

/********************************************************************************************/


class Frontend : public Object{

    public:

        Frontend(void);
        Frontend(
            _in const Frontend& c_oFrontend
        ) = delete;
        Frontend& operator= (
            _in const Frontend&
        ) = delete;
        virtual ~Frontend(void);

        void __thiscall SetFrontend
        (
            _in std::string& strServerIP, 
            _in Word wPort,
            _in std::string& strVMID
        );
        void __thiscall Listener(
            _in std::string strVMID
        );
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

        void __thiscall HandleSubmitJob
        (
            _in std::string& strVMID,
            _in std::string& strFNID,
            _in std::string& strJobID
        );
        // void __thiscall HandleInspect
        // (
        //     _in std::string& strVMID,
        //     _inout std::string& strJobs
        // );
        // void __thiscall HandleGetTable
        // (
        //     _in std::string& strVMID,
        //     _in std::string& strTables
        // );
        void __thiscall HandleQuit
        (
            void
        );
        // void __thiscall HandleCheck
        // (
        //     _in std::string& strVMID
        // );
        void __thiscall HandlePushData
        (
            _in std::string& strVMID,
            _in std::vector<std::string>& stlInputIds,
            _in std::vector<std::vector<Byte>> & stlInputVars
        );
        void __thiscall HandleSetParameters
        (
            _in std::string& strVMID,
            _in std::string& strFNID,
            _in std::string& strJobID,
            _in std::vector<std::string>stlParams
        );
        void __thiscall HandlePullData
        (
            _in std::string& strVMID,
            _in std::string& strJobID,
            _in std::string & strFNID
        );
        void __thiscall QueryResult
        (
            _in std::string& strJobID,
            _in std::string& strFNID,
            _inout std::map<std::string, int>& stlOutput
        );
        JobStatusSignals __thiscall QueryJobStatus(
            _in std::string& strJobID
        );
        std::map<std::string, std::string> __thiscall QueryDataset(
            _in std::string& strVMID
        );
        // void __thiscall HandleDeleteData
        // (
        //     _in std::string& strVMID,
        //     _in std::vector<std::string>& stlvarID
        // );
        void __thiscall HandlePushSafeObject
        (
            _in std::string& strVMID,
            _in std::string& strFNID
        );
        void __thiscall RegisterSafeObject
        (
            _in std::string& strFilePath
        );
        void __thiscall SaveBuffer(
            _in std::string& strDataID,
            _in std::vector<Byte>& stlVars
        );
        void __thiscall SendDataToJobEngine(
            _in const std::string& strVMID,
            _in StructuredBuffer & c_oStructuredBuffer
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

        DigitalContractProvisiongStatus __thiscall GetProvisionStatus(
            const Guid& c_strDigitalContractGUID
            );

        std::string __thiscall GetIPServingDataset(
            _in const Guid& oDatasetGuid
            ) const;

       std::string __thiscall GetIPServingTable(
            _in const Guid& oDatasetGuid
            ) const;

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

        EosbRotationManager m_oEosbRotator{};
        std::unordered_map<std::string, StructuredBuffer> m_stlAvailableSafeFunctions{};
        std::unordered_map<std::string, StructuredBuffer> m_stlDigitalContracts{};
        std::unordered_map<std::string, StructuredBuffer> m_stlAvailableDatasets{};
        std::unordered_map<std::string, TableInformation> m_stlAvailableTables{};
        std::unordered_map<std::string, SecureNodeInformation> m_stlProvisionInformation{};
        std::unordered_map<std::string, std::unique_ptr<JobInformation> > m_stlJobInformation{};
        std::unordered_map<std::string, std::vector<Byte>> m_stlPushedData{};
        StructuredBufferLockedQueue m_oJobMessageQueue{};

        std::map<std::string, std::shared_ptr<TlsNode>> m_stlConnectionMap;
        std::map<std::string, std::shared_ptr<std::mutex>> m_stlConnectionMutexMap;
        std::map<std::string, JobStatusSignals> m_stlJobStatusMap;
        std::map<std::string, std::map<std::string, std::string>> m_stlDataTableMap;

        std::map<std::string, std::unique_ptr<SafeObject>> m_stlFNTable;

        std::unordered_set<std::string> m_stlResultSet;
        std::string m_strUsername;
        std::mutex m_stlResultMapMutex;
        std::mutex m_stlJobStatusMapMutex;
        std::mutex m_stlFlagMutex;
        bool m_fStop;
};
