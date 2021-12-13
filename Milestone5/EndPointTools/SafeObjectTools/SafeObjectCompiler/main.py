import sys, os, pickle
from SafeObjectCompiler.parser import ScriptParser
from SafeObjectCompiler.process import TemplateProcessor, readScriptFile

if __name__ == "__main__":

    sourcePath = sys.argv[1]
    destinationPath = sys.argv[2]
    scriptFilename = sys.argv[3]

    lines, code, title = readScriptFile(sourcePath, scriptFilename)

    indexFileName = destinationPath + "/index"
    if not os.path.isfile(indexFileName):
        with open(indexFileName, 'wb') as f:
            emptyIndexDict = {}
            pickle.dump(emptyIndexDict, f)

    parser = ScriptParser(code)
    content = parser.ParseAll()

    processor = TemplateProcessor(lines, destinationPath, title)
    processor.ProcessAll(content)
