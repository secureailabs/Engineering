# SAIL safe object compiler

What sail safe object compiler do is compiling a python script into a safe object. 

### Compiler installation

To install the compiler, navigate under SafeObjectCompiler/SafeOjbectCompiler folder and type:
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
    -> type annotation:
    '''
    docstring
        basic task the function does
        Args:
         ...
        Return:
         ...
        Confidentiality: True
    '''
    /*function code*/
```
It is the safe object creator's responsibility to annotate types and confidentiality for the safe function. The type annotation can reference the python types module.

The defination of input and output parameter are done via the arguments and returns in the Run function, for example:
```
def Run(a: int, b:int, c:int)->Tuple[int, int, int]:
    '''
    Confidentiality:True,True,True
    '''
    d = a+b+c
    e = a-b+c
    f = a+b-c
    return d,e,f
```
This particular function has a, b and c as input parameters, and d, e, f as output parameters. The input and output parameters are automatically discovered by the compiler.

### Type annotations
The input and output types are recorded via python type annotations, to read more about annotation, one can refer to:

[Python typing](https://docs.python.org/3/library/typing.html)  
[Python function annotation](https://www.python.org/dev/peps/pep-3107/)  
[Python typing library](https://docs.python.org/3/library/typing.html)  
Some simple examples are given below:
```
def Run(a: float) -> float:
    '''
    Confidentiality:True
    '''
    return a
```
This function intake a float input parameter a and returen a float parameter a, the output parameter is not confidential.

```
from typing import Any

def Run(a: Any) -> Any:
    '''
    Confidentiality:False
    '''
    return a
```
This function intakes a parameter which can be any type, and output a parameter which can be any type. The output is not confidential

```
def Run(a:dict[str, str]) ->dict[str:str]:
    '''
    Confidentiality:True
    '''
    return a
```
This function intakes a parameter which can be a dict type and output a parameter which is dict type. The dict has key value pair as str:str. The output is confidential.