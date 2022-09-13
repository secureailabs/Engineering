from zero import ZeroServer
from zero import load_safefunctions
import sys

if __name__ == "__main__":
    
    if(len(sys.argv) != 2):
        raise RuntimeError("must have port number argument")
    
    app = ZeroServer(port=int(sys.argv[1]))
    safe_funcs = load_safefunctions("plot_func")
    safe_funcs.extend(load_safefunctions("data_func"))
    safe_funcs.extend(load_safefunctions("ml_func"))
    safe_funcs.extend(load_safefunctions("stat_func"))
    
    for func in safe_funcs:
        app.register_rpc(func)
    app.run()
