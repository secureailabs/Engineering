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

static Frontend& getFrontend()
{

    static Frontend oFrontend;
    return oFrontend;
}

static PyObject* createguid(PyObject* self, PyObject* args)
{
    Guid oGuid;
    std::string strGuid = oGuid.ToString(eHyphensAndCurlyBraces);
    return Py_BuildValue("s", strGuid.c_str());
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

static PyObject* vmconnect(PyObject* self, PyObject* args)
{
    char* serverIP;
    unsigned int port;
    std::string strVMID;

    if(!PyArg_ParseTuple(args, "sI", &serverIP, &port))
    {
        return NULL;
    }

    std::string strIP(serverIP);
    getFrontend().SetFrontend(strIP, port, strVMID);

    return Py_BuildValue("s", strVMID.c_str());
}

static PyObject* pulldata(PyObject* self, PyObject* args)
{
    char* vmID;
    char* jobID;
    char* fnID;

    if(!PyArg_ParseTuple(args, "sss", &vmID, &jobID, &fnID))
    {
        return NULL;
    }
    
    std::string strVMID(vmID);
    std::string strJobID(jobID);
    std::string strFNID(fnID);

    getFrontend().HandlePullData(strVMID, strJobID, strFNID);
    return Py_BuildValue("");
}

static PyObject* pushdata(PyObject* self, PyObject* args)
{
    char* vmID;
    PyObject* InputId;
    PyObject* InputList;

    if(!PyArg_ParseTuple(args, "sOO", &vmID, &InputId, &InputList))
    {
        return NULL;
    }
    
    std::string strVMID(vmID);


    PyObject *iter = PyObject_GetIter(InputList);
    std::vector<std::vector<Byte>> stlInputs;

    while (true) 
    {
        char* tmpInputs;
        long int len;

        PyObject *next = PyIter_Next(iter);
        if (!next) {
            break;
        }

        PyBytes_AsStringAndSize(next, &tmpInputs, &len);

        std::vector<Byte> stlByteElement((Byte*)tmpInputs, (Byte*)tmpInputs+len);
        stlInputs.push_back(stlByteElement);
   }

    iter = PyObject_GetIter(InputId);
    std::vector<std::string> stlInputId;

    while (true) 
    {
        PyObject *next = PyIter_Next(iter);
        if (!next) {
            break;
        }

        const char* tmpParam = PyUnicode_AsUTF8(next);
        stlInputId.push_back(std::string(tmpParam));
    }

    getFrontend().HandlePushData(strVMID, stlInputId, stlInputs);

    return Py_BuildValue("");
}

static PyObject* setparameter(PyObject* self, PyObject* args)
{
    char* vmID;
    char* jobID;
    char* fnID;
    PyObject* ParamsList;

    if(!PyArg_ParseTuple(args, "sssO", &vmID, &jobID, &fnID, &ParamsList))
    {
        return NULL;
    }
    std::string strVMID(vmID);
    std::string strJobID(jobID);
    std::string strFNID(fnID);

    PyObject *iter = PyObject_GetIter(ParamsList);
    
    std::vector<std::string> stlParams;

    while (true) 
    {
        PyObject *next = PyIter_Next(iter);
        
        if (!next) {
            break;
        }

        const char* tmpParam = PyUnicode_AsUTF8(next);
        std::string strParam = tmpParam;
        std::cout<<"set param: "<<strParam<<std::endl;
        stlParams.push_back(strParam);
    }

    getFrontend().HandleSetParameters(strVMID, strFNID, strJobID, stlParams);
    return Py_BuildValue("");
}

static PyObject* pushsafeobj(PyObject* self, PyObject* args)
{
    char* vmID;
    char* fnID;

    if(!PyArg_ParseTuple(args, "ss", &vmID, &fnID))
    {
        return NULL;
    }
    
    std::string strVMID(vmID);
    std::string strFNID(fnID);

    getFrontend().HandlePushSafeObject(strVMID, strFNID);

    return Py_BuildValue("");
}

static PyObject* submitjob(PyObject* self, PyObject* args)
{
    char* vmID;
    char* fnID;
    char* jobID;

    if(!PyArg_ParseTuple(args, "sss", &vmID, &fnID, &jobID))
    {
        return NULL;
    }
    
    std::string strVMID(vmID);
    std::string strFNID(fnID);
    std::string strJobID(jobID);

    getFrontend().HandleSubmitJob(strVMID, strFNID, strJobID);

    return Py_BuildValue("");
}

static PyObject* queryjobstatus(PyObject* self, PyObject* args)
{
    char* jobid;

    if(!PyArg_ParseTuple(args, "s", &jobid))
    {
        return NULL;
    }

    std::string strJobID(jobid);

    JobStatusSignals oJobStatus = getFrontend().QueryJobStatus(strJobID);
    int nStatus;
    
    switch(oJobStatus)
    {
        case JobStatusSignals::eJobStart: 
            nStatus = 0;
            break;
        case JobStatusSignals::eJobDone: 
            nStatus = 1;
            break;
        case JobStatusSignals::eJobFail: 
            nStatus = -1;
            break;
        case JobStatusSignals::ePrivacyViolation: 
            nStatus = -2;
            break;
        default:
            break;
    }
    
    return Py_BuildValue("i", nStatus);
}

static PyObject* registersafeobj(PyObject* self, PyObject* args)
{
    char* file;

    if(!PyArg_ParseTuple(args, "s", &file))
    {
        return NULL;
    }

    std::string strFile(file);

    getFrontend().RegisterSafeObject(strFile);

    return Py_BuildValue("");
}

static PyObject* quit(PyObject* self, PyObject* args)
{
    getFrontend().HandleQuit();
    return Py_BuildValue("");
}

static PyObject* queryresult(PyObject* self, PyObject* args)
{
    char* jobid;
    char* fnid;

    if(!PyArg_ParseTuple(args, "ss", &jobid, &fnid))
    {
        return NULL;
    }

    std::string strJobID(jobid);
    std::string strFNID(fnid);
    std::map<std::string, int> stlOutput;

    getFrontend().QueryResult(strJobID, strFNID, stlOutput);
    
    PyObject* output = PyDict_New();
    
    for(auto const& x : stlOutput)
    {
        PyObject* value = Py_BuildValue("i", x.second);
        PyDict_SetItemString(output, x.first.c_str(), value);
    }

    return Py_BuildValue("O", output);
}

static PyObject* querydata(PyObject* self, PyObject* args)
{
    char* vmid;

    if(!PyArg_ParseTuple(args, "s", &vmid))
    {
        return NULL;
    }

    std::string strVMID(vmid);

    std::map<std::string, std::string> stlDataTable = getFrontend().QueryDataset(strVMID);
    
    PyObject* output = PyDict_New();
    
    for(auto const& x : stlDataTable)
    {
        PyObject* value = Py_BuildValue("s", x.second.c_str());
        PyDict_SetItemString(output, x.first.c_str(), value);
    }
    //PyObject* output = PyList_New(stlDataTableIDs.size());

    //for(size_t i=0;i<stlDataTableIDs.size();i++)
    //{
    //    const char* tmpdata = stlDataTableIDs[i].c_str();
    //    PyList_SetItem(output, i, Py_BuildValue("s", tmpdata));
    //}
    return Py_BuildValue("O", output);
}

static PyMethodDef SAILAPIMethods [] =
{
    {"createguid", (PyCFunction)createguid, METH_NOARGS, NULL},
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
    {"connect", (PyCFunction)vmconnect, METH_VARARGS, NULL},
    {"pushdata", (PyCFunction)pushdata, METH_VARARGS, NULL},
    {"pulldata", (PyCFunction)pulldata, METH_VARARGS, NULL},
    // {"deletedata", (PyCFunction)deletedata, METH_VARARGS, NULL},
    {"pushsafeobj", (PyCFunction)pushsafeobj, METH_VARARGS, NULL},
    {"submitjob", (PyCFunction)submitjob, METH_VARARGS, NULL},
    // {"gettableID", (PyCFunction)gettableID, METH_VARARGS, NULL},
    {"registersafeobj", (PyCFunction)registersafeobj, METH_VARARGS, NULL},
    {"queryresult", (PyCFunction)queryresult, METH_VARARGS, NULL},
    {"querydata", (PyCFunction)querydata, METH_VARARGS, NULL},
    {"queryjobstatus", (PyCFunction)queryjobstatus, METH_VARARGS, NULL},
    {"setparameter", (PyCFunction)setparameter, METH_VARARGS, NULL},
    {"quit", (PyCFunction)quit, METH_VARARGS, NULL},
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
