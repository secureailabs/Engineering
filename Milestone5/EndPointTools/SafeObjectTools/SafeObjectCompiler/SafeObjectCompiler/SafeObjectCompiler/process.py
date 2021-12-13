import textwrap
from .types import SafeFunction
from .SafeObjectAPI import writeSafeObject

def readScriptFile(sourcePath, fileName):
    '''
    read a single python script
    '''
    scriptFileName = sourcePath + '/' + fileName
    title = fileName[:fileName.index('.')]
    lines = []
    with open(scriptFileName, 'r') as f:
        lines = f.readlines()
    code = ''.join(lines)
    return lines, code, title

class TemplateProcessor:
    '''
    process the python script into a safe function structuredbuffer
    '''
    def __init__(self, lines, destination, title):
        self.template = ""
        self.lines = lines
        self.title = title
        self.destination = destination
        self.LoadTemplate(destination)
    
    def LoadTemplate(self, path):
        '''
        load template from path
        '''
        filename = path + "/SafeObjectTemplate"
        with open(filename, 'r') as f:
            self.template = f.read()
    
    def ProcessAll(self, substituteContents):
        '''
        process the python script and convert it into a structuredbuffer
        '''

        imports = self.ProcessImports(substituteContents.imports)
        classes = self.ProcessClasses(substituteContents.classes)
        localFunctions, majorFunction, safeFunction = self.ProcessFunctions(substituteContents.functions)

        input = self.GenerateFileLoad(safeFunction)
        output = self.GenerateFileDump(safeFunction)
        execution = self.GenerateExecution(safeFunction)

        self.template = self.template.replace("{{__OTHERIMPORTS__}}", imports)
        self.template = self.template.replace("{{__OTHERCLASSES__}}", classes)
        self.template = self.template.replace("{{__NONCLASSMETHODS__}}", localFunctions)
        self.template = self.template.replace("{{__MEMBERMETHODS__}}", majorFunction)
        self.template = self.template.replace("{{__SAFEOBJECTID__}}", safeFunction.uuid)
        self.template = self.template.replace("{{__READINPUT__}}", input)
        self.template = self.template.replace("{{__WRITEOUTPUT__}}", output)
        self.template = self.template.replace("{{__SAFEFUNCTIONEXEC__}}", execution)

        safeFunction.SaveTemplate(self.template)
        #safeFunction.PrintFunction()

        self.WriteStructureBuffer(safeFunction, self.destination)
        self.WriteIndexFile(safeFunction)
    
    def ProcessImports(self, importContents):
        '''
        process imports code blocks
        '''
        substituteImportContents = ""
        for contentBlock in importContents:
            substituteImportContents += contentBlock.blockToString(self.lines)
        return substituteImportContents

    def ProcessClasses(self, classContents):
        '''
        process class code blocks
        '''
        substituteClassContents = ""
        for contentBlock in classContents:
            substituteClassContents += contentBlock.blockToString(self.lines)
            substituteClassContents += "\n"
        return substituteClassContents

    def ProcessFunctions(self, functionContents):
        '''
        process function code blocks
        '''
        localFunctions = ""
        majorFunction = ""
        entryFunction = ""
        for contentBlock in functionContents:
            if(contentBlock.name == 'Run'):
                majorFunction += contentBlock.blockToStringMajor(self.lines)
                entryFunction = self.GenerateMainFunction(contentBlock)
            else:
                localFunctions += contentBlock.blockToString(self.lines)
                localFunctions += '\n'
        majorFunction = textwrap.indent(majorFunction, "    ")
        return localFunctions, majorFunction, entryFunction
    
    def GenerateMainFunction(self, funcBlock):
        '''
        generate the safe function instance
        '''
        returns = funcBlock.annotations.pop('return')
        args = funcBlock.annotations
        returns = list(returns)
        returnConfidentiality = returns.pop()
        returns = tuple(returns)
        return SafeFunction(self.title, funcBlock.doc, args, returns, returnConfidentiality)
    
    def GenerateFileLoad(self, safeFunction):
        '''
        create replacement string for file loading
        '''
        fileLoadStr = ''
        for argid in safeFunction.argsuuid:
            fileLoadStr += ("with open(oInputParameters[\""+ argid +"\"][\"0\"], 'rb') as ifp:\n"        
                            "    self.m_"+ argid + " = pickle.load(ifp)\n")
        fileLoadStr = textwrap.indent(fileLoadStr, "        ")
        return fileLoadStr
    
    def GenerateFileDump(self, safeFunction):
        '''
        create replacement string for file dumping
        '''
        fileDumpStr = ''
        for returnid in safeFunction.returnsuuid:
            fileDumpStr +=  ("with open(self.m_JobIdentifier+\"." + returnid + "\",\"wb\") as ofp:\n"
                             "    pickle.dump(self.m_" + returnid + ", ofp)\n"        
                             "with open(\"DataSignals/\" + self.m_JobIdentifier + \"." + returnid + "\", 'w') as fp:\n"
                             "    pass\n")
        fileDumpStr = textwrap.indent(fileDumpStr, "        ")
        return fileDumpStr
    
    def GenerateExecution(self, safeFunction):
        '''
        create replacement string for safe function execution
        '''
        inputArgs = ""
        results = ""
        for argid in safeFunction.argsuuid:
            inputArgs += "safe" + safeFunction.uuid + ".m_" + argid + ', '
        inputArgs = inputArgs[:-2]
        for returnid in safeFunction.returnsuuid:
            results += "safe" + safeFunction.uuid + ".m_" + returnid + ', '
        results = results[:-2]
        executionStr = results + " = safe" + safeFunction.uuid + ".Run(" + inputArgs + ")"
        executionStr = textwrap.indent(executionStr, "            ")
        return executionStr


    def WriteStructureBuffer(self, safeFunction, destinationDir):
        '''
        write structuredbuffer into file
        '''
        writeSafeObject(safeFunction, destinationDir)
    
    def WriteIndexFile(self, safeFunction):
        '''
        write index file
        '''
        import pickle
        indexDict = {}
        indexFile = self.destination+"/index"
        with open(indexFile, 'rb') as f:
            indexDict = pickle.load(f)
        indexDict[self.title] = safeFunction.uuid
        with open(indexFile, 'wb') as f:
            pickle.dump(indexDict, f)
