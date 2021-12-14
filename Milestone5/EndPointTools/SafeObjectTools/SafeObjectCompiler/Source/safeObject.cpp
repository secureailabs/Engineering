#include "StructuredBuffer.h"
#include "Exceptions.h"
#include "ExceptionRegister.h"

#include <Python.h>
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
static PyObject* parameterConvert(StructuredBuffer& oBuffer, PyObject* oUuids, PyObject* oTypes, PyObject* oConfidentiality = NULL)
{
    Py_ssize_t unListLen = PyList_Size(oUuids);

    for(Py_ssize_t i = 0; i<unListLen; i++)
    {
        std::cout<<"parameter: "<<i<<std::endl;
        StructuredBuffer oItem;

        try
        {
            PyObject* oParamGuid = PyList_GetItem(oUuids, i);
            if(!oParamGuid)
            {
                PyErr_SetString(PyExc_Exception, "Parameter guid read fail");
                return Py_None;
            }
            const char* szGuid = PyUnicode_AsUTF8(oParamGuid);
            std::string strGuid(szGuid);
            oItem.PutString("Uuid", strGuid);
            std::cout<<"guid: "<<strGuid<<std::endl;

            PyObject* oParamType = PyList_GetItem(oTypes, i);
            if(!oParamType)
            {
                PyErr_SetString(PyExc_Exception, "Parameter type read fail");
                return Py_None;
            }
            const char* szType = PyUnicode_AsUTF8(oParamType);
            std::string strType(szType);
            oItem.PutString("Type", strType);
            std::cout<<"type: "<<strType<<std::endl;
        
            if(oConfidentiality)
            {
                PyObject* oParamConf = PyList_GetItem(oConfidentiality, i);
                if(!oParamConf)
                {
                   PyErr_SetString(PyExc_Exception, "Parameter confidentiality read fail");
                   return Py_None;
                }
                int nConfidentiality = PyObject_IsTrue(oParamConf);
                if(nConfidentiality)
                    oItem.PutString("confidentiality", "1");
                else
                    oItem.PutString("confidentiality", "0");
                std::cout<<"confidentiality: "<<nConfidentiality<<std::endl;
            }
        }
        
        catch (const BaseException& oException) 
        { 
            ::RegisterException(oException, __func__, __FILE__, __LINE__); 
        } 
        catch (...) 
        { 
            ::RegisterUnknownException(__func__, __FILE__, __LINE__); 
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
    std::string strTitle;

    if(!PyArg_ParseTuple(args, "Os", &oSafeObject, &szDestinationDir))
    {
        return Py_None;
    }

    std::string strDestination(szDestinationDir);

    try
    {
        PyObject* oTitle = PyObject_GetAttrString(oSafeObject, "name");
        if(!oTitle)
        {
            PyErr_SetString(PyExc_Exception, "Safe object title read fail");
            return Py_None;
        }
        
        const char* szTitle = PyUnicode_AsUTF8(oTitle);
        strTitle = szTitle;
        oResult.PutString("Title", strTitle);
        std::cout<<"safe object title: "<<strTitle<<std::endl;

        PyObject* oUuid = PyObject_GetAttrString(oSafeObject, "uuid");
        if(!oUuid)
        {
            PyErr_SetString(PyExc_Exception, "Safe object uuid read fail");
            return Py_None;
        }
        const char* szUuid = PyUnicode_AsUTF8(oUuid);
        std::string strUuid(szUuid);
        oResult.PutString("Uuid", strUuid);
        std::cout<<"safe object uuid: "<<strUuid<<std::endl;

        PyObject* oDescription = PyObject_GetAttrString(oSafeObject, "doc");
        if(!oDescription)
        {
            PyErr_SetString(PyExc_Exception, "Safe object doc read fail");
            return Py_None;
        }
        const char* szDes = PyUnicode_AsUTF8(oDescription);
        std::string strDes(szDes);
        oResult.PutString("Description", strDes);
        std::cout<<"safe object description: "<<strDes<<std::endl;

        PyObject* oInputUuids = PyObject_GetAttrString(oSafeObject, "argsuuid");
        if(!oInputUuids)
        {
            PyErr_SetString(PyExc_Exception, "Safe object argsuuid read fail");
            return Py_None;
        }
        PyObject* oInputTypes = PyObject_GetAttrString(oSafeObject, "argTypes");
        if(!oInputTypes)
        {
            PyErr_SetString(PyExc_Exception, "Safe object argTypes read fail");
            return Py_None;
        }
        PyObject* oOutputUuids = PyObject_GetAttrString(oSafeObject, "returnsuuid");
        if(!oOutputUuids)
        {
            PyErr_SetString(PyExc_Exception, "Safe object return uuids read fail");
            return Py_None;
        }
        PyObject* oOutputTypes = PyObject_GetAttrString(oSafeObject, "returnTypes");
        if(!oOutputTypes)
        {
            PyErr_SetString(PyExc_Exception, "Safe object return types read fail");
            return Py_None;
        }
        PyObject* oOutputConfidentiality = PyObject_GetAttrString(oSafeObject, "confidentiality");
        if(!oOutputConfidentiality)
        {
            PyErr_SetString(PyExc_Exception, "Safe object confidentiality read fail");
            return Py_None;
        }
    
        StructuredBuffer oInput;
        StructuredBuffer oOutput;
    
        std::cout<<"safe object inputs: "<<std::endl;
        PyObject* oInputResult = parameterConvert(oInput, oInputUuids, oInputTypes);
        if(!oInputResult)
        {
            PyErr_SetString(PyExc_Exception, "Safe object input parameter convert fail");
            return Py_None;
        }
        std::cout<<"safe object outputs: "<<std::endl;
        PyObject* oOutputResult = parameterConvert(oOutput, oOutputUuids, oOutputTypes, oOutputConfidentiality);
        if(!oOutputResult)
        {
            PyErr_SetString(PyExc_Exception, "Safe object output parameter convert fail");
            return Py_None;
        }
        oResult.PutStructuredBuffer("InputParameters", oInput);
        oResult.PutStructuredBuffer("OutputParameters", oOutput);

        PyObject* oBody = PyObject_GetAttrString(oSafeObject, "template");
        if(!oBody)
        {
            PyErr_SetString(PyExc_Exception, "Safe object template read fail");
            return Py_None;
        }
        const char* szBody = PyUnicode_AsUTF8(oBody);
        std::string strBody(szBody);
        oResult.PutString("Payload", strBody);
    }
    
    catch (const BaseException& oException) 
    { 
        ::RegisterException(oException, __func__, __FILE__, __LINE__);
    } 
    catch (...) 
    { 
        ::RegisterUnknownException(__func__, __FILE__, __LINE__); 
    }
    
    std::ofstream stlFileStream;
    std::string strFname = strDestination + "/" + strTitle + ".safe";
    std::cout<<strFname<<std::endl;
    std::vector<Byte> stlFileData = oResult.GetSerializedBuffer();
    stlFileStream.open(strFname, std::ios::out | std::ofstream::binary);
    if(!stlFileStream)
    {
        return Py_None;
    }
    
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
