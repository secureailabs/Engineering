/*********************************************************************************************
 *
 * @file JobEngineConnection.h
 * @author David Gascon
 * @date 23 Feb, 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include <memory>
#include <thread>

class StructuredBuffer;
class StructuredBufferLockedQueue;
class TlsNode;

class JobEngineConnection
{
    public:
        JobEngineConnection(
            std::shared_ptr<TlsNode> stlConnectionPointer,
            StructuredBufferLockedQueue& oQueueToOrchestrator
            );

        JobEngineConnection() = delete;

        virtual ~JobEngineConnection();

        bool __thiscall SendStructuredBufferToJobEngine(
            _in const StructuredBuffer& c_oBufferToSend
            );

        void __thiscall StartJobEngineListenerThread();
        std::shared_ptr<TlsNode> __thiscall GetConnection() const;

        bool __thiscall IsRunning() const;

    private:
        void JobEngineConnectionThread();


        std::shared_ptr<TlsNode> m_stlConnectionPointer;
        bool m_fStopRequest{false};
        StructuredBufferLockedQueue& m_oStructuredBufferQueue;
        std::unique_ptr<std::thread> m_pstlListenerThread{nullptr};
};
