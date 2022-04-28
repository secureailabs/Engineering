/*********************************************************************************************
 *
 * @file EosbRotationManager.h
 * @author David Gascon
 * @date 18 Nov 2021
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2021 Secure AI Labs, Inc. All Rights Reserved.
 *
 ********************************************************************************************/

#pragma once

#include "CoreTypes.h"
#include "Object.h"
#include "StructuredBuffer.h"

#include <condition_variable>
#include <mutex>
#include <string>
#include <thread>

/********************************************************************************************/

class SailPlatformServicesSession : public Object
{
    public:
    
        // The ip address and port number must be specified here instead of during Login(),
        // since it's possible to call RegisterOrganization() without login. So we need
        // a way to keep track of the ip address and port number here
        SailPlatformServicesSession(
            _in const std::string & c_strServerIpAddress,
            _in Word wServerPort
            );
        SailPlatformServicesSession(
            _in const SailPlatformServicesSession &
            ) = delete;
        SailPlatformServicesSession & operator= (
            _in const SailPlatformServicesSession &
            ) = delete;
        virtual ~SailPlatformServicesSession(void);
        
        // Methods used to retrieve information about the running session
        std::string __thiscall GetServerIpAddress(void) const throw();
        Word __thiscall GetServerPortNumber(void) const throw();
        std::string __thiscall GetEosb(void) const throw();
        // Method called when an API call gets a refreshed EOSB and we
        // need to register it here.
        void __thiscall SetEosb(
            _in const std::string & c_strEosb
            ) throw();
            
        // This is the only method which can be called before logging in
        void __thiscall RegisterOrganization(
            _in const StructuredBuffer & c_oRegistrationParameters
            );
        // This is the login function. Calling it the first time will cause the update
        // thread to start. Calling login again will simply replace the EOSB
        void __thiscall Login(
            _in const std::string & c_strEmail,
            _in const std::string & c_strUserPassword
            );
        void __thiscall Logout(void) throw();
        // Methods used to handle various API calls after login
        StructuredBuffer __thiscall GetBasicUserInformation(void);
        void __thiscall RegisterUser(
            _in const StructuredBuffer & c_oRegistrationParameters
            );
        void __thiscall RegisterDatasetFamily(
            _in const StructuredBuffer & c_oRegistrationParameters
            );
        void __thiscall RegisterDataset(
            _in const StructuredBuffer & c_oRegistrationParameters
            );
        std::string __thiscall ApplyForDigitalContract(
            _in const StructuredBuffer & c_oRegistrationParameters
            );
        void __thiscall ApproveDigitalContract(
            _in const StructuredBuffer & c_oRegistrationParameters
            );
        void __thiscall ActivateDigitalContract(
            _in const StructuredBuffer & c_oRegistrationParameters
            );
            
    private:
    
        bool __thiscall IsRunning(void) const throw();
        void __thiscall StartSession(
            _in const std::string & c_strEosb
            );
            
        // This method runs continuously until m_fIsRunning is
        // set back to false
        void __thiscall EosbMaintenanceFunction(void) throw();

        // Private data members
        volatile bool m_fIsRunning{false};
        mutable std::mutex m_oLock{};
        std::string m_strEosb{};
        std::string m_strServerIpAddress{};
        Word m_wServerPortNumber{0};
        std::condition_variable m_oTimedWait{};
        std::unique_ptr<std::thread> m_oEosbMaintenanceThread{nullptr};
};
