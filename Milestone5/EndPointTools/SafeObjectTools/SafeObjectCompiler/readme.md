# SAIL safe object compiler

What sail safe object compiler do is compiling a python script into a safe object. 

### Compiler installation

To install the compiler, navigate under SafeObjectCompiler folder and type:
```
sudo pip3 install .
```

### Compile safe objects

To use the compiler, include an edited safe object under Scripts, and run:
```
make
```
The compiled safe object will be generated in the SafeObjects folder with an index file. The index file is a pickled python dictionary which has all key-value pair for safe object names and UUIDs.

### Generate documentation

Documentation generation requires third-party package pdoc3. To install the package, run:
```
sudo pip3 install pdoc3
```
To run the makefile for document generation, navigate to Scripts folder and run:
```
make doc
```
The a doc.md file will be generated under SafeObjects folder.

### Example of safe object scripts
An example script in provided in test.py file, which can include heler classes and functions. The entry point must be names as run function with annotated types and informations. The general strucutre of the Run function is:
```
def Run(param1: type annotation, param2: type annotation...) 
    -> (return value 1: type annotation, ... 
        [confidentiality of return value 1, ...]):
    '''
    docstring
        basic task the function does
        Args:
         ...
        Return:
         ...
    '''
    /*function code*/
```
It is the safe object creator's responsibility to annotate types and confidentiality for the safe function. The type annotation can reference the python types module.