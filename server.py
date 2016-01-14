from flask import Flask, render_template
import os
import subprocess
app = Flask(__name__)

okCmds = frozenset(["python"])

@app.route('/<cmd>/<script>/')
def runCmd(cmd, script):

    if cmd in okCmds:
    	print cmd, script
        o = subprocess.check_output([cmd,script])
        return o
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
  return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

