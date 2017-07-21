from flask import Flask
from flask import request
from msg_processor.message_processor import MessageProcessor


app = Flask(__name__)
message_processor = MessageProcessor()


@app.route('/')
def hello_world():
    return 'MP server is running\n'


@app.route('/mp', methods=['POST', "GET"])
def mp():
    if request.method == 'POST':
        data = request.data
        print("/mp POST", data)
        if not data:
            return ''
        result = message_processor.process(data)
        if type(result) == list:
            result = "\n".join(result)
        return str(result)
    elif request.method == 'GET':
        result = "post messages to /mp route\n"
        print("/mp GET", result)
        return result


if __name__ == "__main__":
    host, port = "localhost", 5000
    print("Running on host [{}] port [{}]".format(host, port))
    app.run(host=host, port=port)
