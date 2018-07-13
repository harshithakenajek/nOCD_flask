import os

from flask import Flask, request

app = Flask(__name__)

@app.route('/login' ,methods = ['GET'])
def login():
    if request.values:
        return "user name " + request.values["username"]
    else:
        return "ERrror"
# @app.route('/hello')
# def hello():
#     # tracing
#     # import pdb
#     # pdb.set_trace()
#     return "Hello World !!"

if __name__ == '__main__':
    host = os.getenv('IP','0.0.0.0')
    port = int(os.getenv('PORT',5000))
    app.debug = True
    app.run(port=port,host=host)