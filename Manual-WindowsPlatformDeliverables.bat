ECHO OFF
SET script_dir=%cd%
SET buildlist=WindowsRemoteDataConnector.exe SailTablePackagerForCsv.exe SailDatasetPackager.exe
SET copylist=libcurl.dll libcurl-d.dll zlib1.dll zlibd1.dll

ECHO ----------------------------------------------------------------------------------------------
ECHO ----------------------------------------------------------------------------------------------
ECHO ----------------------------------------------------------------------------------------------
ECHO SCRIPT BUILD and TARBALL: WindowsPlatformDeliverables at (HOME) of Current Script Directory
ECHO SCRIPT CREATES output.txt at (HOME) of Current Script Directory
ECHO THE Current Script Directory (HOME): %script_dir%
ECHO ----------------------------------------------------------------------------------------------
ECHO ----------------------------------------------------------------------------------------------
ECHO ----------------------------------------------------------------------------------------------
ECHO.
ECHO.

ECHO ----------------------------------------------------------------------------------------------
ECHO LIST of DEFAULT VALUES for this script
ECHO ----------------------------------------------------------------------------------------------
ECHO - PATH to vcvars64.bat:
ECHO C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build
ECHO.
ECHO - PATH to WindowsPlatformDeliverables:
ECHO C:\Users\StanleyLin\REPO\Engineering\InternalTools\WindowsPlatformDeliverables
ECHO.
ECHO.


ECHO ----------------------------------------------------------------------------------------------
ECHO STEP SPECIFY UNIQUE PATHS with NO (Leading OR Trailing) SPACES in your PATH
ECHO ----------------------------------------------------------------------------------------------
SET "vcvars64_path=C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build"
SET "windows_deliverables_path=C:\Users\StanleyLin\REPO\Engineering\InternalTools\WindowsPlatformDeliverables"
SET "version_management_path=C:\Users\StanleyLin\REPO\Engineering\VersionManagement"
SET /p vcvars64_path=Specify your UNIQUE path to vcvars64.bat or just ENTER for default: 
set /p windows_deliverables_path=Specify your UNIQUE path to WindowsPlatformDeliverables or just ENTER for default: 
SET /p version_management_path=Specify your UNIQUE path to version_management_path or just ENTER for default:
ECHO.

ECHO SPECIFIED PATH of vcvars64.bat:
ECHO %vcvars64_path%
ECHO.
ECHO SPECIFIED PATH of WindowsPlatformDeliverables: 
ECHO %windows_deliverables_path%
ECHO.
ECHO SPECIFIED PATH of VersionManagement
ECHO %version_management_path%
ECHO.

ECHO ---------------------------------------------------------------------------------------------- > output.txt
ECHO STEP CLEANUP: START >> output.txt
ECHO ---------------------------------------------------------------------------------------------- >> output.txt
ECHO ----------------------------------------------------------------------------------------------
ECHO STEP CLEANUP: START 
START /WAIT "VERIFY" cmd.exe /c DIR && CD "%windows_deliverables_path%\Binaries\x64\" && DEL /F /Q Debug && RMDIR /S /Q Debug && DEL /F /Q WindowsPlatformDeliverables.tar && CD "%script_dir%"

echo.
ECHO ----------------------------------------------------------------------------------------------
ECHO STEP CLEANUP: COMPLETED
ECHO Current Script Directory: %cd%
ECHO ----------------------------------------------------------------------------------------------
echo.


ECHO ---------------------------------------------------------------------------------------------- >> output.txt
ECHO STEP BUILDING WINDOWS DELIVERABLES: START >> output.txt
ECHO ---------------------------------------------------------------------------------------------- >> output.txt
ECHO ----------------------------------------------------------------------------------------------
ECHO BUILDING WINDOWS DELIVERABLES: START 
START /WAIT "VERSION_MANAGEMENT" "%version_management_path%\WindowsBuildVersionGenerator.exe"
START /WAIT "VERSION_MANAGEMENT" "%version_management_path%\WindowsAssemblyInfoVersionUpdater.exe" "%windows_deliverables_path%\SailDatasetPackager\Properties\AssemblyInfo.cs"
START /WAIT "VERSION_MANAGEMENT" "%version_management_path%\WindowsAssemblyInfoVersionUpdater.exe" "%windows_deliverables_path%\SailTablePackagerForCvs\Properties\AssemblyInfo.cs"
START /WAIT "BUILDS" cmd.exe /c ""%vcvars64_path%\vcvars64.bat" && msbuild  "%windows_deliverables_path%\Windows Platform Deliverables.sln" >> output.txt && ECHO %errorlevel%"
ECHO BUILD COMMAND EXIT CODE: %errorlevel%

echo.
ECHO ----------------------------------------------------------------------------------------------
ECHO STEP BUILDING WINDOWS DELIVERABLES: COMPLETED
ECHO Current Script Directory: %cd%
ECHO ----------------------------------------------------------------------------------------------
echo.


ECHO ---------------------------------------------------------------------------------------------- >> output.txt
ECHO STEP VERIFY BUILD: START >> output.txt
ECHO ---------------------------------------------------------------------------------------------- >> output.txt
ECHO ----------------------------------------------------------------------------------------------
ECHO STEP VERIFY BUILD: START 
(FOR %%a IN (%buildlist%) DO (
    ECHO SEARCHING FOR %%a
    ECHO SEARCHING FOR %%a >> %script_dir%\output.txt
	cd %windows_deliverables_path%\Binaries\x64\Debug
	ECHO Current DIR: %cd%
	IF EXIST %%a (
	    ECHO %%a Found! >> %script_dir%\output.txt
		ECHO %%a Found!
		ECHO.
	) ELSE (
		ECHO %%a Not Found! >> %script_dir%\output.txt
	    ECHO %%a Not Found! && PAUSE && EXIT /b %errorlevel%
		ECHO.
	)
))
cd %script_dir%

ECHO.
ECHO ----------------------------------------------------------------------------------------------
ECHO STEP VERIFY BUILD: COMPLETED
ECHO Current Script Directory: %cd%
ECHO ----------------------------------------------------------------------------------------------
ECHO.


ECHO ---------------------------------------------------------------------------------------------- >> output.txt
ECHO STEP COPYING COPYLIST [libcurl.dll, libcurl-d.dll, zlib1.dll, zlibd1.dll ] >> output.txt
ECHO ---------------------------------------------------------------------------------------------- >> output.txt
ECHO ----------------------------------------------------------------------------------------------
ECHO COPYING .dll [libcurl.dll, libcurl-d.dll, zlib1.dll, zlibd1.dll ]
copy %windows_deliverables_path%\Libraries\*.dll %windows_deliverables_path%\Binaries\x64\Debug\ >> output.txt && echo %errorlevel%
IF %errorlevel% NEQ 0 (
    ECHO EXIT CODE: %errorlevel%, .dll failed to copy >> output.txt
	ECHO EXIT CODE: %errorlevel%, .dll failed to copy && PAUSE && EXIT /b %errorlevel%
) 


ECHO ---------------------------------------------------------------------------------------------- >> output.txt
ECHO VERIFY COPYLIST >> output.txt
ECHO ---------------------------------------------------------------------------------------------- >> output.txt
ECHO ----------------------------------------------------------------------------------------------
ECHO VERIFY COPYLIST
(for %%a in (%copylist%) do (
    echo SEARCHING FOR %%a
    echo SEARCHING FOR %%a >> output.txt
	cd %windows_deliverables_path%\Binaries\x64\Debug
	ECHO Current DIR: %cd%
	IF EXIST %%a (
	    ECHO %%a Found! >> %script_dir%\output.txt
		ECHO %%a Found!
		ECHO.
	) ELSE (
		ECHO %%a Not Found! >> %script_dir%\output.txt
	    ECHO %%a Not Found! && PAUSE && EXIT /b %errorlevel%
		ECHO.
	)
))
cd %script_dir%

ECHO.
ECHO ----------------------------------------------------------------------------------------------
ECHO STEP COPYING COPYLIST: COMPLETED
ECHO STEP VERIFY COPYLIST: COMPLETED
ECHO Current Script Directory: %cd%
ECHO ----------------------------------------------------------------------------------------------
ECHO.


ECHO ---------------------------------------------------------------------------------------------- >> output.txt
ECHO STEP TARBALL Debug Folder >> output.txt
ECHO ---------------------------------------------------------------------------------------------- >> output.txt
ECHO ----------------------------------------------------------------------------------------------
ECHO STEP TARBALL
CD "%windows_deliverables_path%\Binaries\x64\Debug"
MKDIR WindowsPlatformDeliverables
COPY *.exe WindowsPlatformDeliverables
COPY *.dll WindowsPlatformDeliverables
tar -cvzf WindowsPlatformDeliverables.tar WindowsPlatformDeliverables >> %script_dir%\output.txt 2>&1

IF %errorlevel% NEQ 0 (
    ECHO TARBALL CREATION FAILED! >> %script_dir%\output.txt
    ECHO TARBALL CREATION FAILED! && PAUSE && EXIT /b %errorlevel%
)

ECHO.
COPY WindowsPlatformDeliverables.tar %script_dir%\ /V
IF %errorlevel%==0 (
    ECHO TARBALL COPIED to HOME of BATCH script! >> %script_dir%\output.txt
	ECHO TARBALL COPIED to HOME of BATCH script!
)

ECHO.
ECHO ----------------------------------------------------------------------------------------------
ECHO FINISHED CLOSING PROGRAM
ECHO.
ECHO ----------------------------------------------------------------------------------------------
PAUSE