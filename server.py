from flask import Flask
import os
import subprocess
app = Flask(__name__)

okCmds = frozenset(["python"])

@app.route('/<cmd>/<arg>/<model>/<mol>')
def runCmd(cmd, arg, model, mol):

    if cmd in okCmds:
        o = subprocess.check_output([cmd,arg, model, mol])
        return ('<pre>' + o + '</pre>')
    else:
        return ( cmd + ' is not an ok command.' )

# chem_args = parse(inputBytes)      # Bytes
# chem_ret_val = fullrun(chem_args)  # Data
# # chem_out = toString(chem_ret_val)  # Bytes

# @app.route('processData','GET')
# def processData():
#     renderForm

# @app.route('processData','POST')
# def processData(dataBytes):
#     bytes = app.getBytes
#     resp  = toString( fullrun ( parse (bytes)))
#     resp.setHeader('Content-Style','download');


@app.route('/')
def index():
  return "Hi"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

