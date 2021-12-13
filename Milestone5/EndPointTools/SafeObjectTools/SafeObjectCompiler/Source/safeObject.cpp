#include "Python.h"
#include "StructuredBuffer.h"

#include <fstream>
#include <iostream>
#include <string>
#include <string.h>


/********************************************************************************************
 *
 * @function parameterConvert
 * @brief write safe function parameter info into a structuredbuffer
 *
 ********************************************************************************************/
static void parameterConvert(StructuredBuffer& oBuffer, PyObject* oUuids, PyObject* oTypes, PyObject* oConfidentiality = NULL)
{
    Py_ssize_t unListLen = PyList_Size(oUuids);

    for(Py_ssize_t i = 0; i<unListLen; i++)
    {
        std::cout<<"parameter: "<<i<<std::endl;
        StructuredBuffer oItem;

        PyObject* oParamGuid = PyList_GetItem(oUuids, i);
        const char* szGuid = PyUnicode_AsUTF8(oParamGuid);
        std::string strGuid(szGuid);
        oItem.PutString("Uuid", strGuid);
        std::cout<<"guid: "<<strGuid<<std::endl;

        PyObject* oParamType = PyList_GetItem(oTypes, i);
        const char* szType = PyUnicode_AsUTF8(oParamType);
        std::string strType(szType);
        oItem.PutString("Type", strType);
        std::cout<<"type: "<<strType<<std::endl;
        
        if(oConfidentiality)
        {
            PyObject* oParamConf = PyList_GetItem(oConfidentiality, i);
            int nConfidentiality = PyObject_IsTrue(oParamConf);
            if(nConfidentiality)
                oItem.PutString("confidentiality", "1");
            else
                oItem.PutString("confidentiality", "0");
            std::cout<<"confidentiality: "<<nConfidentiality<<std::endl;
        }

        oBuffer.PutStructuredBuffer(std::to_string((int)i).c_str(), oItem);
    }
}

/********************************************************************************************
 *
 * @function writeSafeObject
 * @brief write safe object info into a structured buffer, save it at designated path
 *
 ********************************************************************************************/

static PyObject* writeSafeObject(PyObject* self, PyObject* args)
{
    StructuredBuffer oResult;
    PyObject* oSafeObject;
    const char* szDestinationDir;

    if(!PyArg_ParseTuple(args, "Os", &oSafeObject, &szDestinationDir))
    {
        return NULL;
    }

    std::string strDestination(szDestinationDir);

    PyObject* oTitle = PyObject_GetAttrString(oSafeObject, "name");
    const char* szTitle = PyUnicode_AsUTF8(oTitle);
    std::string strTitle(szTitle);
    oResult.PutString("Title", strTitle);
    std::cout<<"safe object title: "<<strTitle<<std::endl;

    PyObject* oUuid = PyObject_GetAttrString(oSafeObject, "uuid");
    const char* szUuid = PyUnicode_AsUTF8(oUuid);
    std::string strUuid(szUuid);
    oResult.PutString("Uuid", strUuid);
    std::cout<<"safe object uuid: "<<strUuid<<std::endl;

    PyObject* oDescription = PyObject_GetAttrString(oSafeObject, "doc");
    const char* szDes = PyUnicode_AsUTF8(oDescription);
    std::string strDes(szDes);
    oResult.PutString("Description", strDes);
    std::cout<<"safe object description: "<<strDes<<std::endl;

    PyObject* oInputUuids = PyObject_GetAttrString(oSafeObject, "argsuuid");
    PyObject* oInputTypes = PyObject_GetAttrString(oSafeObject, "argTypes");
    PyObject* oOutputUuids = PyObject_GetAttrString(oSafeObject, "returnsuuid");
    PyObject* oOutputTypes = PyObject_GetAttrString(oSafeObject, "returnTypes");
    PyObject* oOutputConfidentiality = PyObject_GetAttrString(oSafeObject, "confidentiality");
    
    StructuredBuffer oInput;
    StructuredBuffer oOutput;
    
    std::cout<<"safe object inputs: "<<std::endl;
    parameterConvert(oInput, oInputUuids, oInputTypes);
    std::cout<<"safe object outputs: "<<std::endl;
    parameterConvert(oOutput, oOutputUuids, oOutputTypes, oOutputConfidentiality);
    oResult.PutStructuredBuffer("InputParameters", oInput);
    oResult.PutStructuredBuffer("OutputParameters", oOutput);

    PyObject* body = PyObject_GetAttrString(oSafeObject, "template");
    const char* szBody = PyUnicode_AsUTF8(body);
    std::string strBody(szBody);
    oResult.PutString("Payload", strBody);

    std::ofstream stlFileStream;
    std::string strFname = strDestination + "/" + strTitle + ".safe";
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
