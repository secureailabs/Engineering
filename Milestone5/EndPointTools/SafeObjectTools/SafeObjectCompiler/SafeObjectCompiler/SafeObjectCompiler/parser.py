import ast
import types
from .types import ClassBlock, FunctionBlock, ImportBlock, ScriptContent


class ScriptParser:
    '''
    parse a script by node
    currently only support four different kinds of nodes
    '''
    def __init__(self, code):
        '''
        constructor
        '''
        self.code = code
        self.tree = ast.parse(code)

    def ParseAll(self):
        '''
        parse the entire script
        '''
        classes = []
        imports = []
        functions = []
        for node in self.tree.body:
            if isinstance(node, ast.Import):
                block = self.ParseImports(node)
                imports.append(block)
            elif isinstance(node, ast.ImportFrom):
                block = self.ParseFromImports(node)
                imports.append(block)
            elif isinstance(node, ast.ClassDef):
                block = self.ParseClass(node)
                classes.append(block)
            elif isinstance(node, ast.FunctionDef):
                block = self.ParseFunction(node)
                functions.append(block)
            else:
                raise Exception("Ast node type not supported")
        libdict = self.ParseLibs()
        return ScriptContent(classes, imports, functions, libdict)

    def ParseImports(self, node):
        '''
        parse a import node
        '''
        start = node.lineno
        end = node.end_lineno
        return ImportBlock(start, end)

    def ParseFromImports(self, node):
        '''
        parse a fromImport node
        '''
        start = node.lineno
        end = node.end_lineno
        return ImportBlock(start, end)

    def ParseClass(self, node):
        '''
        parse a class node
        '''
        start = node.lineno
        end = node.end_lineno
        return ClassBlock(start, end)

    def ParseFunction(self, node):
        '''
        parse a functiondef node
        '''
        name = node.name
        start = node.lineno
        end = node.end_lineno
        annotations = 0
        doc = 0
        if(name == 'Run'):
            exec(self.code)
            annotations = locals()['Run'].__annotations__
            doc = locals()['Run'].__doc__
        return FunctionBlock(name, start, end, annotations, doc)

    def ParseLibs(self):
        '''
        parse source code to get lib versions
        '''
        exec(self.code)
        libdict = {}
        for name, val in locals().items():
            if isinstance(val, types.ModuleType):
                if hasattr(val, '__version__'):
                    libdict[val.__name__] = val.__version__
                else:
                    libdict[val.__name__] = "not available"
        return libdict
