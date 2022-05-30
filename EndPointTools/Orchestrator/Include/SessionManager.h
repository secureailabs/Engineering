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
#include "Object.h"

#include <condition_variable>
#include <mutex>
#include <string>
#include <thread>

/********************************************************************************************/

class SessionManager : public Object
{
    public:

        SessionManager(void);
        SessionManager(
            _in const SessionManager &
            ) = delete;
        SessionManager & operator= (
            _in const SessionManager &
            ) = delete;
        virtual ~SessionManager(void);

        // This is the login function. Calling it the first time will cause the update
        // thread to start. Calling login again will simply replace the EOSB
        bool __thiscall Login(
            _in const std::string & c_strEmail,
            _in const std::string & c_strUserPassword,
            _in const std::string & c_strServerIpAddress,
            _in Word wServerPort
            ) throw();
        void __thiscall Logout(void) throw();

        // Methods used to retrieve information about the running session
        std::string __thiscall GetServerIpAddress(void) const throw();
        Word __thiscall GetServerPortNumber(void) const throw();
        std::string __thiscall GetAccessToken(void) const throw();
        // Method called when an API call gets a refreshed EOSB and we
        // need to register it here.
        void __thiscall SetAccessTokens(
            _in const std::string & c_strAccessToken,
            _in const std::string & c_strRefreshToken
            ) throw();

    private:

        bool __thiscall IsRunning(void) const throw();
        void __thiscall SetSessionParameters(
            _in const std::string & c_strServerIpAddress,
            _in Word wServerPortNumber,
            _in const std::string & c_strAccessToken,
            _in const std::string & c_strRefreshToken
            );

        // This method runs continuously until m_fIsRunning is
        // set back to false
        void __thiscall AccessTokenMaintenanceFunction(void) throw();

        // Private data members
        volatile bool m_fIsRunning{false};
        mutable std::mutex m_oLock{};
        std::string m_strAccessToken{};
        std::string m_strRefreshToken{};
        std::string m_strServerIpAddress{};
        Word m_wServerPortNumber{0};
        std::condition_variable m_oTimedWait{};
        std::unique_ptr<std::thread> m_oAccessTokenMaintenanceThread{nullptr};
};
