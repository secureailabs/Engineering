/*********************************************************************************************
 *
 * @file pyapi.cpp
 * @author Jingwei Zhang
 * @date 14 Jan 2022
 * @License Private and Confidential. Internal Use Only.
 * @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
 * @brief Interop functions between C++ and python
 *
 ********************************************************************************************/

#include <Python.h>
#include <string>
#include <vector>
#include <map>
#include <fstream>
#include <sstream>
#include <iterator>
#include <iostream>
#include "Guid.h"
#include "frontend.h"
#include "JsonValue.h"
#include "ExceptionRegister.h"

static Orchestrator& getFrontend()
{
    static Orchestrator oFrontend;
    return oFrontend;
}

static PyObject* login(PyObject* self, PyObject* args)
{
    char* email;
    char* password;
    int serverPort;
    char* serverIP;

    if(!PyArg_ParseTuple(args, "ssis", &email, &password, &serverPort, &serverIP))
    {
        return nullptr;
    }

    std::string strEmail(email);
    std::string strPassword(password);
    std::string strServerIP(serverIP);

    unsigned int unLoginStatus = getFrontend().Login(strEmail, strPassword, serverPort, strServerIP);

    return Py_BuildValue("I", unLoginStatus);
}

static PyObject* get_current_eosb(PyObject * self, PyObject * args)
{
    std::string strEosb = getFrontend().GetCurrentEosb();
    PyObject* poPythonReturn;
    if ( !strEosb.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strEosb.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }
    return poPythonReturn;
}

static PyObject* exit_current_session(PyObject * self, PyObject * args)
{
    getFrontend().ExitCurrentSession();

    return Py_BuildValue("s", "exited");
}

static PyObject* get_safe_functions(PyObject* self, PyObject* args)
{
    std::string strSafeFunctions = getFrontend().GetSafeFunctions();
    PyObject* poPythonReturn;
    if ( !strSafeFunctions.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strSafeFunctions.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }
    return poPythonReturn;
}

static PyObject* get_tables(PyObject* self, PyObject* args)
{
    std::string strTables = getFrontend().GetTables();
    PyObject* poPythonReturn;
    if ( !strTables.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strTables.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }
    return poPythonReturn;
}

static PyObject* load_safe_objects(PyObject* self, PyObject* args)
{
    const char* c_szDirectory;
    if(!PyArg_ParseTuple(args, "s", &c_szDirectory))
    {
        return nullptr;
    }

    const std::string strDirectory(c_szDirectory);

    return Py_BuildValue("i", getFrontend().LoadSafeObjects(strDirectory));
}

static PyObject* get_digital_contracts(
    _in PyObject* self,
    _in PyObject* args
    )
{
    std::string strDigitalContracts = getFrontend().GetDigitalContracts().c_str();
    PyObject* poPythonReturn;
    if ( !strDigitalContracts.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strDigitalContracts.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }
    return poPythonReturn;
}

static PyObject* get_datasets(
    _in PyObject* self,
    _in PyObject* args
    )
{
    std::string strDatasets = getFrontend().GetDatasets().c_str();
    PyObject* poPythonReturn;
    if ( !strDatasets.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strDatasets.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }
    return poPythonReturn;
}

static PyObject* provision_secure_computational_node(
    _in PyObject* self,
    _in PyObject* args
    )
{
    char* pszDigitalContractGuid;
    char* pszDatasetGuid;
    char* pszVirtualMachineType;

    if(!PyArg_ParseTuple(args, "sss", &pszDigitalContractGuid, &pszDatasetGuid, &pszVirtualMachineType))
    {
        return nullptr;
    }

    std::string strDigitalContractGuid(pszDigitalContractGuid);
    std::string strDatasetGuid(pszDatasetGuid);
    std::string strVirtualMachineType(pszVirtualMachineType);
    std::string strProvisionStatus = getFrontend().ProvisionSecureComputationalNode(strDigitalContractGuid, strDatasetGuid, strVirtualMachineType);
    PyObject* poPythonReturn;
    if ( !strProvisionStatus.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strProvisionStatus.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }

    return poPythonReturn;
}

static PyObject* run_job(
    _in PyObject* self,
    _in PyObject* args
    )
{
    char* pszSafeObjectGuid;

    if(!PyArg_ParseTuple(args, "s", &pszSafeObjectGuid))
    {
        return nullptr;
    }

    std::string strSafeObjectGuid(pszSafeObjectGuid);

    std::string strJobId = getFrontend().RunJob(strSafeObjectGuid);
    PyObject* poPythonReturn;

    if ( !strJobId.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strJobId.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }
    return poPythonReturn;
}

static PyObject* wait_for_all_secure_nodes_to_be_provisioned(
    _in PyObject * self,
    _in PyObject * args
    )
{
    int nTimeoutMs;
 
    if(!PyArg_ParseTuple(args, "i", &nTimeoutMs))
    {
        return nullptr;
    }
    std::string strProvisionStatus = getFrontend().WaitForAllSecureNodesToBeProvisioned(nTimeoutMs);
    PyObject* poPythonReturn;
    if ( !strProvisionStatus.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strProvisionStatus.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }

    return poPythonReturn;
 }


static PyObject* push_user_data(
    _in PyObject* self,
    _in PyObject* args
    )
{
    PyObject* poUserData;

    std::cout << "Trying to parse" << std::endl;
    if(!PyArg_ParseTuple(args, "O", &poUserData))
    {
        std::cout << "Parse failure" << std::endl;
        return NULL;
    }

    printf("%p\n", poUserData);
    char* pcTempInput;
    long nLen;
    std::string strPushResponse{""};

    if ( nullptr != poUserData)
    {
        std::cout << "Trying to get string and size " << std::endl;
        PyBytes_AsStringAndSize(poUserData, &pcTempInput, &nLen);
        std::cout << "Size " << nLen << std::endl;
        std::vector<Byte> stlByteElement((Byte*)pcTempInput, (Byte*)pcTempInput + nLen);
        strPushResponse = getFrontend().PushUserData(stlByteElement);
    }

    return Py_BuildValue("s", strPushResponse.c_str());
}

static PyObject* set_parameter(
    _in PyObject* self,
    _in PyObject* args
    )
{
    char* pszJobGuid;
    char* pszParameterGuid;
    char* pszParameterValueGuid;

    if(!PyArg_ParseTuple(args, "sss", &pszJobGuid, &pszParameterGuid, &pszParameterValueGuid))
    {
        return nullptr;
    }
    std::string strJobGuid(pszJobGuid);
    std::string strParameterGuid(pszParameterGuid);
    std::string strParameterValueGuid(pszParameterValueGuid);

    std::string strResponse = getFrontend().SetParameter(strJobGuid, strParameterGuid, strParameterValueGuid);

    PyObject* poPythonReturn;
    if ( !strResponse.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strResponse.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }
    return poPythonReturn;
}

static PyObject* get_job_status(
    _in PyObject* self,
    _in PyObject* args
    )
{
    char* pszJobGuid;

    if(!PyArg_ParseTuple(args, "s", &pszJobGuid))
    {
        return nullptr;
    }
    std::string strJobGuid(pszJobGuid);

    std::string strResponse = getFrontend().GetJobStatus(strJobGuid);

    PyObject* poPythonReturn;
    if ( !strResponse.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strResponse.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }
    return poPythonReturn;
}

static PyObject* pull_data(
    _in PyObject* self,
    _in PyObject* args
    )
{
    char* pszDataIdentifier;

    if(!PyArg_ParseTuple(args, "s", &pszDataIdentifier))
    {
        return nullptr;
    }
    std::string strDataIdentifier(pszDataIdentifier);

    std::string strResponse = getFrontend().PullJobData(strDataIdentifier);

    PyObject* poPythonReturn;
    if ( !strResponse.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strResponse.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }
    return poPythonReturn;
}

static PyObject* wait_for_data(
    _in PyObject* self,
    _in PyObject* args
    )
{
    int nTimeoutInMilliseconds;

    if(!PyArg_ParseTuple(args, "i", &nTimeoutInMilliseconds))
    {
        return nullptr;
    }

    std::string strResponse = getFrontend().WaitForData(nTimeoutInMilliseconds);

    PyObject* poPythonReturn;
    if ( !strResponse.empty() )
    {
        poPythonReturn = Py_BuildValue("s", strResponse.c_str());
    }
    else
    {
        poPythonReturn = Py_BuildValue("");
    }
    return poPythonReturn;
}

static PyMethodDef SAILAPIMethods [] =
{
    {"login", (PyCFunction)login, METH_VARARGS, NULL},
    {"get_current_eosb", (PyCFunction)get_current_eosb, METH_NOARGS, NULL},
    {"exit_current_session", (PyCFunction)exit_current_session, METH_NOARGS, NULL},
    {"load_safe_objects", (PyCFunction)load_safe_objects, METH_VARARGS,NULL},
    {"get_safe_functions", (PyCFunction)get_safe_functions, METH_NOARGS, NULL},
    {"get_digital_contracts", (PyCFunction)get_digital_contracts, METH_NOARGS,NULL},
    {"get_datasets", (PyCFunction)get_datasets, METH_NOARGS, NULL},
    {"get_tables", (PyCFunction)get_tables, METH_NOARGS, NULL},
    {"provision_secure_computational_node", (PyCFunction)provision_secure_computational_node, METH_VARARGS, NULL},
    {"run_job", (PyCFunction)run_job, METH_VARARGS, NULL},
    {"set_parameter", (PyCFunction)set_parameter, METH_VARARGS, NULL},
    {"push_user_data", (PyCFunction)push_user_data, METH_VARARGS, NULL},
    {"get_job_status", (PyCFunction)get_job_status, METH_VARARGS, NULL},
    {"wait_for_all_secure_nodes_to_be_provisioned", (PyCFunction)wait_for_all_secure_nodes_to_be_provisioned, METH_VARARGS, NULL},
    {"pull_data", (PyCFunction)pull_data, METH_VARARGS, NULL},
    {"wait_for_data", (PyCFunction)wait_for_data, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef SAILPyAPIModule =
{
    PyModuleDef_HEAD_INIT,
    "SAILPyAPI",
    NULL,
    -1,
    SAILAPIMethods
};

PyMODINIT_FUNC PyInit_SAILPyAPI(void){
    return PyModule_Create(&SAILPyAPIModule);
}
