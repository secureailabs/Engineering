from flask import Flask

app = Flask(__name__)


@app.route('/SamplePlugin/Hello', methods=['GET'])
def Hello():
    return "Hello from SamplePlugin"


@app.route('/SamplePlugin/NotHello', methods=['GET'])
def NotHello():
    return "Not Hello from SamplePlugin"
