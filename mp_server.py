from flask import Flask
from flask import request
from message_processor import MessageProcessor


app = Flask(__name__)
message_processor = MessageProcessor("", "")

@app.route('/')
def hello_world():
    return 'Hello, World!\n'


@app.route('/mp', methods=['POST', "GET"])
def mp():
    data = request.data
    result = message_processor.process(data)
    return result


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
