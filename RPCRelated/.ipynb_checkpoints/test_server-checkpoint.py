from zero import ZeroServer
from zero import load_module
import sys

if __name__ == "__main__":
    
    if(len(sys.argv) != 2):
        raise RuntimeError("must have port number argument")
    
    app = ZeroServer(port=int(sys.argv[1]))
    safe_contents = load_module("series")
    
    for func in safe_contents["safe_funcs"]:
        app.register_rpc(func, "series")
    for obj in safe_contents["safe_objects"]:
        app.register_ro(obj, "series")
    print(app._ro_router)
    print(app._rpc_router)
    app.run()
