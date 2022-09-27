import sys

from zero import ZeroServer, load_module

if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise RuntimeError("must have port number argument")

    app = ZeroServer(port=int(sys.argv[1]))
    safe_contents = load_module("dataframe")

    for func in safe_contents["safe_funcs"]:
        app.register_rpc(func, "dataframe")
    for obj in safe_contents["safe_objects"]:
        app.register_ro(obj, "dataframe")
    print(app._ro_router)
    print(app._rpc_router)
    app.run()
