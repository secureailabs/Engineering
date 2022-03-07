/*********************************************************************************************
 *
 * @file StructuredBufferLockedQueue.cpp
 * @author David Gascon
 * @date 18 Jan, 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/
#include <iostream>

#include "StructuredBuffer.h"
#include "StructuredBufferLockedQueue.h"

/********************************************************************************************
 *
 * @class StructuredBufferLockedQueue
 * @function StructuredBufferLockedQueue
 * @brief Default constructor
 *
 ********************************************************************************************/
StructuredBufferLockedQueue::StructuredBufferLockedQueue(void)
{

}

/********************************************************************************************
 *
 * @class StructuredBufferLockedQueue
 * @function ~StructuredBufferLockedQueue
 * @brief Default destructor
 *
 ********************************************************************************************/
StructuredBufferLockedQueue::~StructuredBufferLockedQueue(void)
{

}

/********************************************************************************************
 *
 * @class StructuredBufferLockedQueue
 * @function CopyAndPushMessage
 * @brief Take a copy of a StructuredBuffer and push it to our queue as a shared pointer
 *
 ********************************************************************************************/
void __thiscall StructuredBufferLockedQueue::CopyAndPushMessage(
    _in const StructuredBuffer& oMessageToPush
    )
{

    std::cout << "Before Pushed message " << m_stlMessageQueue.size() << std::endl;
    std::shared_ptr<StructuredBuffer> oMessageCopy{new StructuredBuffer(oMessageToPush)};
    {
        std::lock_guard<std::mutex> stlLock(m_stlLock);
        m_stlMessageQueue.push(oMessageCopy);
        std::cout << "Pushed message " << m_stlMessageQueue.size() << std::endl;
    }

    // Notify the conditional variable outside of the lock so the conditional doesn't
    // wake up with a still locked mutex
    m_stlQueueWaitCondition.notify_one();
}

/********************************************************************************************
 *
 * @class StructuredBufferLockedQueue
 * @function WaitForMessage
 * @brief Return a message from a queue if there is one, and we didn't timeout waiting
 *
 ********************************************************************************************/
std::shared_ptr<StructuredBuffer> __thiscall StructuredBufferLockedQueue::WaitForMessage(
    _in int unTimeoutInMilliseconds
    )
{
    std::shared_ptr<StructuredBuffer> oReturn{nullptr};

    {
        std::unique_lock<std::mutex> stlLock(m_stlLock);
        // Is there a message immediately available?
        if ( false == m_stlMessageQueue.empty() )
        {
            oReturn = m_stlMessageQueue.front();
            m_stlMessageQueue.pop();
        }
        else
        {
            // Wait for one to come in
            auto stlAcquiredLock = m_stlQueueWaitCondition.wait_for(stlLock, std::chrono::milliseconds(unTimeoutInMilliseconds));
            if ( std::cv_status::no_timeout == stlAcquiredLock )
            {
                if ( false == m_stlMessageQueue.empty() )
                {
                    oReturn = m_stlMessageQueue.front();
                    m_stlMessageQueue.pop();
                }
            }
            else
            {
                std::cout << "Timed out waiting for condition variable " << std::endl;
            }
        }
    }
    return oReturn;
}

/********************************************************************************************
 *
 * @class StructuredBufferLockedQueue
 * @function ClearAllMessages
 * @brief Clear the queue of its current messages
 *
 ********************************************************************************************/
void StructuredBufferLockedQueue::ClearAllMessages(void)
{
    std::lock_guard<std::mutex> stlLock(m_stlLock);
    while ( false == m_stlMessageQueue.empty() )
    {
        m_stlMessageQueue.pop();
    }
}
