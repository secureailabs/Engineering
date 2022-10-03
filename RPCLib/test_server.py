import sys

from zero import ZeroServer, load_module

if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise RuntimeError("must have port number argument")
    
    module_stat = load_module("sail_scn_lib.statistics")
    module_data = load_module("sail_scn_lib.data")

    app = ZeroServer(port=int(sys.argv[1]))
    safe_contents = {"safe_funcs":set(), "safe_objects": set()}
    modules = [module_stat, module_data]
    for m in modules:
        safe_contents["safe_funcs"].update(m["safe_funcs"])
        safe_contents["safe_objects"].update(m["safe_objects"])
    print(safe_contents)

    for func in safe_contents["safe_funcs"]:
        app.register_rpc(func, "")
    for obj in safe_contents["safe_objects"]:
        app.register_ro(obj, "")
    print(app._ro_router)
    print(app._rpc_router)
    app.run()
