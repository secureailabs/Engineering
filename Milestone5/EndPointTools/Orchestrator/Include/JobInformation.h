/*********************************************************************************************
 *
 * @file JobInformation.h
 * @author David Gascon
 * @date 7 Jan, 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/
#include "CoreTypes.h"
#include "OrchestratorTypes.h"
#include "Guid.h"

#include <mutex>
#include <optional>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

class StructuredBuffer;
class StructuredBufferLockedQueue;
class TlsNode;

class JobInformation
{
    public:
        explicit JobInformation(
            const Guid& c_oJobId,
            const Guid& c_oSafeFunctionId,
            const std::vector<std::string>& c_stlInputParameterIds,
            StructuredBufferLockedQueue& oQueueToOrchestrator
        );

        //JobInformation() = delete;
        virtual ~JobInformation();

        bool __thiscall ReadyToExcute() const;

        std::string __thiscall GetJobStatus() const;

        bool __thiscall SetInputParameter(
            _in const std::string& c_strInputParameterId,
            _in const std::string& c_strValue
        );

        void __thiscall  SetTargetIP(
            _in const std::string& c_strTargetIP
        );

        bool __thiscall JobParameterUsesGuid(
            _in const Guid & c_oDatasetGuid
        ) const;

        bool __thiscall JobParameterUsesJobOutputParameter(
            _in const std::string& c_strJobOutputParameter
        ) const;

        const __thiscall Guid& GetJobId() const;

        std::string __thiscall GetTargetIP(void) const;
        std::string __thiscall GetSafeFunctionId(void) const;
        const std::unordered_map<std::string, std::optional<std::string>>& __thiscall GetInputParameterMap() const;
        void __thiscall SetConnection(std::shared_ptr<TlsNode> poTlsConnection);
        std::shared_ptr<TlsNode> __thiscall GetConnection() const;

        void __thiscall StartJobEngineListenerThread();

        bool __thiscall SendStructuredBufferToJobEngine(
            _in const StructuredBuffer& c_oBufferToSend
            );

        void __thiscall SetOutputJobParameterReady(
            _in const std::string& c_strOutputParameterId
            );

        const std::vector<Byte>& GetOutputParameter(
            _in const Guid& oParameterIdentifier
            );

        bool __thiscall IsRunning() const;
        // BasicLockable methods
        void __thiscall lock();
        void __thiscall unlock();

    private:

        void __thiscall JobEngineListener();

        mutable std::recursive_mutex m_stlLock;
        const Guid m_oJobId;
        const Guid m_oSafeFunctionId;
        std::string m_strTargetIP{""};
        std::unordered_map<std::string, std::optional<std::string>> m_stlInputParameterData;
        std::unordered_map<std::string, bool> m_stlOutputJobParameterData;
        std::shared_ptr<TlsNode> m_poTlsConnection{nullptr};
        std::unique_ptr<std::thread> m_pstlListenerThread{nullptr};
        bool m_fStopRequest{false};
        std::optional<JobStatusSignals> m_eJobStatus{};

        StructuredBufferLockedQueue& m_oQueueToOrchestrator;

        std::unordered_map<std::string, std::vector<Byte>> m_stlOutputResults{};
};
