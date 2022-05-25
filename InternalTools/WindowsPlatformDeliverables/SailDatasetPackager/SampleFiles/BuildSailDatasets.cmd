@echo off

REM =============================================================================
REM Print starting messages and info
REM =============================================================================

// Print out the application header
@echo ===========================================================================================================
@echo SAIL Dataset Packager v1.0
@echo by Luis Miguel Huapaya
@echo Copyright (C) 2021 Secure AI Labs Inc., All Rights Reserved.
@echo -----------------------------------------------------------------------------------------------------------
@echo Building and publishing all datasets
@echo Working folder is: %~dp0
@echo Date and time: %date% %time%
@echo SAIL Platform Services IP address: %1

REM =============================================================================
REM Check to make sure that all the needed files are there
REM =============================================================================

IF NOT EXIST igr_001.saildataset (
    echo File igr_001.saildataset is missing from the current folder
    GOTO END
)
IF NOT EXIST igr_002.saildataset (
    echo File igr_002.saildataset is missing from the current folder
    GOTO END
)
IF NOT EXIST mgr_001.saildataset (
    echo File mgr_001.saildataset is missing from the current folder
    GOTO END
)

REM =============================================================================
REM Now build all the saildataset files from template
REM =============================================================================

start /W /B "" SailDatasetPackager.exe --template igr_001.saildataset --datasetFilename igr_001.csvp --sailplatformaddress %1 --username "lbart@igr.com" --password "SailPassword@123"
if %ERRORLEVEL% NEQ 0 GOTO BADEND
start /W /B "" SailDatasetPackager.exe --template igr_002.saildataset --datasetFilename igr_002.csvp --sailplatformaddress %1 --username "lbart@igr.com" --password "SailPassword@123"
if %ERRORLEVEL% NEQ 0 GOTO BADEND
start /W /B "" SailDatasetPackager.exe --template mgr_001.saildataset --datasetFilename mgr_001.csvp --sailplatformaddress %1 --username "nadams@mghl.com" --password "SailPassword@123"
if %ERRORLEVEL% NEQ 0 GOTO BADEND

GOTO END

:BADEND

@echo SailDatasetPackager has exited abnormally with %ERRORLEVEL%

:END
@echo on