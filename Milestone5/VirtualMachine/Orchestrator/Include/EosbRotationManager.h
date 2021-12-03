/*********************************************************************************************
 *
 * @file EosbRotationManager.h
 * @author David Gascon
 * @date 18 Nov 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/
#include "CoreTypes.h"

#include <condition_variable>
#include <mutex>
#include <string>
#include <thread>

/********************************************************************************************/
class EosbRotationManager
{
    public:
        explicit EosbRotationManager(
            void
            );

        virtual ~EosbRotationManager(void);

        // No copying allowed
        EosbRotationManager (
            const EosbRotationManager&
            ) = delete;
        EosbRotationManager& operator= (
            const EosbRotationManager&
            ) = delete;

        void __thiscall Stop();
        void __thiscall Start(
            _in const std::string& c_strServerIp,
            _in unsigned int c_unServerPort
        );
        std::string __thiscall GetEosb() const;
        void __thiscall SetEosb(const std::string& strEosb);

        bool __thiscall IsRunning() const;
    private:
        void __thiscall PeriodicEosbUpdate();

        mutable std::mutex m_oLock{};
        std::condition_variable m_oTimedWait{};
        std::unique_ptr<std::thread> m_oRotatingThread{nullptr};
        std::string m_strEosb{};
        std::string m_strServerIp;
        unsigned int m_unServerPort;
        bool fStopRequest{false};
};
