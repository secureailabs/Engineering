import uuid


class CodeBlock:
    '''
    Class associate with node and code block
    '''
    def __init__(self, start, end):
        '''
        constructor
        '''
        self.start = start
        self.end = end

    def blockToString(self, lines):
        '''
        convert a node to string block
        '''
        i = self.start - 1
        blockString = ""
        while(i < self.end):
            blockString.join(lines[i])
            i += 1
        return blockString


class ClassBlock(CodeBlock):
    '''
    class node code block
    '''
    def __init__(self, start, end):
        super().__init__(start, end)


class ImportBlock(CodeBlock):
    '''
    import node code block
    '''
    def __init__(self, start, end):
        super().__init__(start, end)


class FunctionBlock(CodeBlock):
    '''
    functiondef node code block
    '''
    def __init__(self, name, start, end, annotations, doc):
        self.name = name
        super().__init__(start, end)
        self.annotations = annotations
        self.doc = doc

    def blockToStringMajor(self, lines):
        '''
        process the entry point function node
        '''
        pos = lines[self.start-1].index('(')
        lines[self.start-1] = \
            f"{lines[self.start-1][:pos+1]}self, {lines[self.start-1][pos+1:]}"
        return super().blockToString(lines)


class ScriptContent:
    '''
    Data structure to store all code blocks in the parse tree
    '''
    def __init__(self, classes, imports, functions):
        self.classes = classes
        self.imports = imports
        self.functions = functions


class SafeFunction:
    '''
    safe function info class
    '''
    def __init__(self, name, doc, args, returns, confidentiality):
        self.name = name
        if doc is None:
            self.doc = ""
        else:
            self.doc = doc
        self.uuid = uuid.uuid4().hex.upper()
        self.argsuuid = []
        if not isinstance(args, dict):
            raise Exception("safe function args must be a dict")
        self.argTypes = self.ProcessArgs(args)
        self.returnsuuid = []
        if not isinstance(returns, tuple):
            raise Exception("safe function returns must be a tuple")
        self.returnTypes = self.ProcessReturns(returns)
        self.confidentiality = confidentiality
        self.template = ""

    def ProcessArgs(self, args):
        '''
        generate argument uuids
        '''
        argTypes = []
        for arg in args:
            argTypes.append(str(args[arg]))
            self.argsuuid.append(uuid.uuid4().hex.upper())
        return argTypes

    def ProcessReturns(self, returns):
        '''
        generate return variable uuids
        '''
        returnTypes = []
        for val in returns:
            returnTypes.append(str(val))
            self.returnsuuid.append(uuid.uuid4().hex.upper())
        return returnTypes

    def SaveTemplate(self, template):
        '''
        accept template after process
        '''
        self.template = template

    def PrintFunction(self):
        print("name: {0}".format(self.name), flush=True)
        print("uuid: {0}".format(self.uuid), flush=True)
        print("args: {0}".format(self.argsuuid), flush=True)
        print("argTypes: {0}".format(self.argTypes), flush=True)
        print("returnsuuid: {0}".format(self.returnsuuid), flush=True)
        print("returnTypes: {0}".format(self.returnTypes), flush=True)
        print("confidentiality: {0}".format(self.confidentiality), flush=True)
