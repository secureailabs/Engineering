#include "Python.h"
#include "StructuredBuffer.h"
#include <fstream>
#include <iostream>
#include <string>
#include <string.h>

static void parameterConvert(StructuredBuffer& oBuffer, PyObject* oUuids, PyObject* oTypes, PyObject* oConfidentiality = NULL)
{
    Py_ssize_t listLen = PyList_Size(oUuids);

    for(Py_ssize_t i = 0; i<listLen; i++)
    {
        std::cout<<"parameter: "<<i<<std::endl;
        StructuredBuffer oItem;

        PyObject* oParamGuid = PyList_GetItem(oUuid, i);
        const char* guid = PyUnicode_AsUTF8(oParamGuid);
        std::string strGuid(guid);
        oItem.PutString("Uuid", strGuid);
        std::cout<<"guid: "<<strGuid<<std::endl;

        PyObject* oParamType = PyList_GetItem(oTypes, i);
        const char* type = PyUnicode_AsUTF8(oParamType);
        std::string strType(type);
        oItem.PutString("Type", strType);
        std::cout<<"type: "<<strType<<std::endl;
        
        if(!oConfidentiality)
        {
            PyObject* oParamConf = PyList_GetItem(oConfidentiality, i);
            int confidentiality = PyObject_IsTrue(oParamConf);
            if(confidentiality)
                oItem.PutString("confidentiality", "1");
            else
                oItem.PutString("confidentiality", "0");
            std::cout<<"confidentiality: "<<strConfidentiality<<std::endl;
        }

        oBuffer.PutStructuredBuffer(std::to_string((int)i).c_str(), oItem);
    }
}

static PyObject* writeSafeObject(PyObject* self, PyObject* args)
{
    StructuredBuffer oResult;
    PyObject* oSafeObject;
    if(!PyArg_ParseTuple(args, "O", &oSafeObject))
    {
        return NULL;
    }

    PyObject* oTitle = PyObject_GetAttrString(oSafeObject, "name");
    const char* sTitle = PyUnicode_AsUTF8(oTitle);
    std::string strTitle(sTitle);
    oResult.PutString("Title", strTitle);
    std::cout<<"safe object title: "<<strTitle<<std::endl;

    PyObject* oUuid = PyObject_GetAttrString(oSafeObject, "uuid");
    const char* sUuid = PyUnicode_AsUTF8(oUuid);
    std::string strUuid(sUuid);
    oResult.PutString("Uuid", strUuid);
    std::cout<<"safe object uuid: "<<strUuid<<std::endl;

    PyObject* oDescription = PyObject_GetAttrString(oSafeObject, "doc");
    const char* sDes = PyUnicode_AsUTF8(oDescription);
    std::string strDes(sDes);
    oResult.PutString("Description", strDes);
    std::cout<<"safe object description: "<<strDes<<std::endl;

    PyObject* oInputUuids = PyObject_GetAttrString(oSafeObject, "argsuuid");
    PyObject* oInputTypes = PyObject_GetAttrString(oSafeObject, "argsTypes");
    PyObject* oOutputUuids = PyObject_GetAttrString(oSafeObject, "returnsuuid");
    PyObject* oOutputTypes = PyObject_GetAttrString(oSafeObject, "returnsTypes");
    PyObject* oOutputConfidentiality = PyObject_GetAttrString(oSafeObject, "confidentiality");
    
    StructuredBuffer oInput;
    StructuredBuffer oOutput;
    
    std::cout<<"safe object inputs: "<<std::endl;
    parameterConvert(oInput, oInputUuids, oInputTypes);
    std::cout<<"safe object outputs: "<<std::endl;
    parameterConvert(oOutput, oOutputUuids, oOutputTypes, oConfidentiality);
    oResult.PutStructuredBuffer("InputParameters", oInput);
    oResult.PutStructuredBuffer("OutputParameters", oOutput);

    PyObject* body = PyDict_GetItemString(oSafeObject, "template");
    const char* sBody = PyUnicode_AsUTF8(body);
    std::string strBody(sBody);
    oResult.PutString("Payload", strBody);
    std::cout<<"body"<<std::endl;

    std::ofstream stlFileStream;
    std::string strFname = strUuid + ".safe";
    std::cout<<strFname<<std::endl;
    std::vector<Byte> stlFileData = oResult.GetSerializedBuffer();
    stlFileStream.open(strFname, std::ios::out | std::ofstream::binary);
    std::copy(stlFileData.begin(), stlFileData.end(), std::ostreambuf_iterator<char>(stlFileStream));
    stlFileStream.close();

    return Py_BuildValue("");
}

static PyMethodDef SafeObjAPIMethods [] =
{
    {"writeSafeObject", (PyCFunction)writeSafeObject, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef SafeObjAPIModule =
{
    PyModuleDef_HEAD_INIT,
    "SafeObjectAPI",
    NULL,
    -1,
    SafeObjAPIMethods
};

PyMODINIT_FUNC PyInit_SafeObjectAPI(void){
    return PyModule_Create(&SafeObjAPIModule);
}
