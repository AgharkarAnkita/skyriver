import copy

from flask import Flask,request
from flask_sockets import Sockets
import pyodbc,datetime
from flask import json

app = Flask(__name__)
sockets = Sockets(app)
con = pyodbc.connect('DRIVER={SQL Server};SERVER=WINJIT214;DATABASE=ServerSocket;UID=sa;PWD=winjit@123')
c = con.cursor()

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/Login',methods=['POST'])
def Login():
    try:
        pageno=request.json['pgn']
        pagesize=request.json['pgs']
        deviceid=request.json['device']
        after = request.json['afterDate']
        a=datetime.datetime.strptime(after, "%Y%m%d")
        before = request.json['beforeDate']
        b = datetime.datetime.strptime(before, "%Y%m%d")
        query = c.execute("exec ServerSocket.dbo.sp_AllData ?,?,?,?,?", pageno, pagesize, deviceid, a, b)
        result = [dict((query.description[i][0], value) for i, value in enumerate(row)) for row in
                  query.fetchall()]
        js=scrub(result)
        response = {
            'Data': {
                'DeviceId': deviceid,
                'Date': datetime.datetime.now().strftime("%H:%M:%S"),
                #  'Actual Date': datetime.time("%H:%M:%S")
                'MetaData':
                js


            }
        }
        js=json.dumps(response,indent=4)
        return js

    except Exception, E:
        print str(E)
        response = {'Error': {'ErrorMessage': 'Invalid Input',
                      'isError': 1
                      },
            'Result': ''
            }
        js = json.dumps(response)
        return js

def scrub(x):
        # Converts None to empty string
        ret = copy.deepcopy(x)
        # Handle dictionaries, lits & tuples. Scrub all values
        if isinstance(x, dict):
            for k, v in ret.items():
                ret[k] = scrub(v)
        if isinstance(x, (list, tuple)):
            for k, v in enumerate(ret):
                ret[k] = scrub(v)
        # Handle None
        if x is None:
            ret = {}
        # Finished scrubbing
        return ret

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer((''), app, handler_class=WebSocketHandler)
    server.serve_forever()