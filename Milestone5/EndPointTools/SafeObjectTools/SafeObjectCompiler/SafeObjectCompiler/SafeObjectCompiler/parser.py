import ast
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
        self.code =code
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
        return ScriptContent(classes, imports, functions)

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
            doc = node.__doc__
            exec(self.code)
            annotations = locals()['Run'].__annotations__
        return FunctionBlock(name, start, end, annotations, doc)