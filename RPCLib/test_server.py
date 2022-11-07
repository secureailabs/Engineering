import sys

from zero import ZeroServer, load_module

if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise RuntimeError("must have port number argument")

    module_stat = load_module("sail_safe_functions.statistics")
    module_data = load_module("sail_safe_functions.preprocessing")
    module_ml = load_module("sail_safe_functions.machine_learning")
    module_privacy = load_module("sail_safe_functions.privacy_barrier")

    app = ZeroServer(port=int(sys.argv[1]))
    safe_contents = {"safe_funcs": set(), "safe_objects": set()}
    modules = [module_stat, module_data, module_ml, module_privacy]
    for m in modules:
        safe_contents["safe_funcs"].update(m["safe_funcs"])
        safe_contents["safe_objects"].update(m["safe_objects"])

    for func in safe_contents["safe_funcs"]:
        print(func.__name__, flush=True)
        app.register_rpc(func, "")
    for obj in safe_contents["safe_objects"]:
        app.register_ro(obj, "")
    print(app._ro_router)
    print(app._rpc_router)
    app.run()
