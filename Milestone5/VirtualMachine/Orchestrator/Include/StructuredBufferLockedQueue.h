/*********************************************************************************************
 *
 * @file StructuredBufferLockedQueue.h
 * @author David Gascon
 * @date 18 Jan, 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#include <condition_variable>
#include <memory>
#include <queue>

class StructuredBuffer;

class StructuredBufferLockedQueue
{
    public:
        explicit StructuredBufferLockedQueue();

        virtual ~StructuredBufferLockedQueue();
        std::shared_ptr<StructuredBuffer> __thiscall WaitForMessage(
            _in int nTimeoutInMilliseconds
            );

        void __thiscall CopyAndPushMessage(
            _in const StructuredBuffer& oMessageToPush
            );

        void __thiscall ClearAllMessages(void);
    private:

        mutable std::mutex m_stlLock{};
        std::condition_variable m_stlQueueWaitCondition{};
        std::queue<std::shared_ptr<StructuredBuffer>> m_stlMessageQueue{};
};
