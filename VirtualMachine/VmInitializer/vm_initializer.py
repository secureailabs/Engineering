import os

import psutil
import uvicorn
from fastapi import BackgroundTasks, FastAPI, File, Response, UploadFile


# This is a background task and will only be executed after the API calling it has finished.
def kill_server():
    parent = psutil.Process(os.getpid())
    parent.kill()


if __name__ == "__main__":
    # Start the server only if the two required files are not present
    if os.path.isfile("InitializationVector.json") and os.path.isfile("package.tar.gz"):
        print("InitializationVector and package.tar.gz already present, exiting!!")
        exit(0)

    app = FastAPI()

    @app.put(path="/initialization-data")
    def upload_initialization_vector(
        background_taks: BackgroundTasks,
        initialization_vector: UploadFile = File(description="application/json"),
        bin_package: UploadFile = File(description="application/json"),
    ):
        # Write the initialization vector to a file
        with open("InitializationVector.json", "wb") as f:
            f.write(initialization_vector.file.read())

        # Write the initialization vector to a file
        with open("package.tar.gz", "wb") as f:
            f.write(bin_package.file.read())

        # exit the server if the tar package is already present
        if os.path.isfile("InitializationVector.json") and os.path.isfile("package.tar.gz"):
            background_taks.add_task(kill_server)

        print("retruning response")
        return Response(status_code=200)

    # Start the uvicorn server
    config = uvicorn.Config(app, host="0.0.0.0", port=9090, log_level="info", loop="asyncio")
    server = uvicorn.Server(config=config)
    server.run()
