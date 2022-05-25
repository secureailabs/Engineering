#pragma once

#include "CoreTypes.h"
#include "Guid.h"

#include <map>
#include <mutex>
#include <set>
#include <string>

extern "C" __declspec(dllexport) bool __stdcall IsLoggedOn(void) throw();
extern std::string __stdcall GetSailPlatformServicesIpAddress(void);
extern std::string __stdcall GetSailPlatformServicesAccessToken(void);
extern std::string __stdcall GetSailPlatformServicesUserIdentifier(void);
extern std::string __stdcall GetSailPlatformServicesUserOrganizationIdentifier(void);
