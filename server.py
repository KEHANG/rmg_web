from flask import Flask, render_template, request, g
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

@app.route('/<cmd>/<script>/<input_file>')
def runCmdWithInput(cmd, script, input_file):

    if cmd in okCmds and script == "rmg":
    	script = "temp/rmg.py"
    	input_file = "temp/input.py"
        o = subprocess.call([cmd, script, input_file])
        if o == 0:
        	tail_log = subprocess.check_output(["tail", "-5", "temp/RMG.log"])
        	print tail_log
        	return tail_log
        else:
        	return "Need your effort to make it right!!"
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

@app.route('/find_molecule')
def find_molecule():
  return render_template('find_molecule.html')

@app.route('/run_rmg_job', methods=['GET', 'POST'])
def run_rmg_job():
    if request.method == 'POST':
        db = get_db()
        # insert blank
        print "get the db!"
        cur = db.cursor()
        cur.execute(
     """INSERT INTO job_result 
         VALUES (%s, %s, %s, null, TRUE)
         RETURNING id;""",
     ("5", request.form["job_name"], request.form["cmd"]))
        return_value = cur.fetchone()
        db.commit()

        cur.close()
        return str(return_value[0])
    else:
        return render_template('run_rmg_job.html')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

def connect_to_database():
    with open("settings", "r") as f:
        line = f.readline()
        if not line:
            print "Warning: Database connection info incomplete!"
        else:
            pwd = line
    conn = psycopg2.connect(database='postgres', user='postgres', host='localhost', password=pwd)
    return conn

if __name__ == "__main__":
    import psycopg2
    try:
        with app.app_context():
            conn = connect_to_database()
            g._database = conn
            print "connected!"
    except:
        print "I am unable to connect to the database"   
    app.run(host="0.0.0.0", port=80)
    

