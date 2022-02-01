#region Library 
from flask import Flask, render_template, make_response
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import psycopg2
from PIL import Image
import base64
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#endregion library 

#region variables
app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
    return render_template('index.html')
    
DATABASE_URL = 'postgres://whheiyecnfjvze:e54c8491ffe0b37679db8a943fe672d876f440a3936d04724e7f0b82b7df9b6f@ec2-54-229-68-88.eu-west-1.compute.amazonaws.com:5432/dekdht4ds841en'
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
query = "INSERT INTO tinyhousedata(timestamp,t1,t2,t3,t4,t5,ct1,ps,source) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}');"

#app.route('/home')
#query2 = "SELECT * FROM parts;"
#DATABASE_URL = 'postgres://whheiyecnfjvze:e54c8491ffe0b37679db8a943fe672d876f440a3936d04724e7f0b82b7df9b6f@ec2-54-229-68-88.eu-west-1.compute.amazonaws.com:5432/dekdht4ds841en'
#endregion variables

#region database connection
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#endregion database connection

def Getdata_from_database(query):
    t1 = []
    t2 = []
    t3 = []
    t4 = []
    t5 = []
    t6 = []
    ct = []
    timestamp = []
    source = "none"
   # query2 = "SELECT * FROM tinyhousedata WHERE source = 'grid';"
    cur.execute(query)
    #print("The number of tinyhousedata: ", cur.rowcount)
    row = cur.fetchone()
    data = []
    while row is not None:
        data.append(row)
        row = cur.fetchone()

#print(data[1])
    for i in data:
        timestamp.append(i[1])
        t1.append(int(float(i[2])))
        t2.append(int(float(i[3])))
        t3.append(int(float(i[4])))
        t4.append(int(float(i[5])))
        t5.append(int(float(i[6]))) 
        t6.append(int(float(i[8])))  
        ct.append(int(float(i[7])))
        source = i[9]

    #cur.close()
    xs = range(len(timestamp))
    test = plt.figure(figsize=(18,10))
    plt.subplot(211)

    plt.grid(True)
    plt.plot(xs,t1,"tab:blue", label="t1")
    plt.plot(xs,t2,"tab:orange", label="t2")
    plt.plot(xs,t3,"tab:green", label="t3")
    plt.plot(xs,t4,"tab:red", label="t4")
    plt.plot(xs,t5,"tab:purple", label="t5")
    plt.plot(xs,t6,"tab:brown", label="t6")
    plt.ylabel("Temperature [°C]")
    plt.xlabel("Timestamp: " + timestamp[0] + "   to   " + timestamp[-1])
    plt.title("Temperature")
    plt.legend()
    plt.subplot(212)
    plt.grid(True)
    plt.plot(xs,ct,"tab:cyan", label="Power")
    plt.ylabel("Power [watts]")
    plt.xlabel("Timestamp: " + timestamp[0] + "   to   " + timestamp[-1])
    plt.title("Power usage " + source)
    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
    plt.legend()
    canvas = FigureCanvas(test)
    output = io.BytesIO()
    #canvas.print_png(output)
    canvas.print_jpg(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/jpeg'
    return response

class Data(Resource):

    def post(self):
        parser = reqparse.RequestParser()  # initialize     
        parser.add_argument('timestamp', required=True)  # add args
        parser.add_argument('t1', required=True)
        parser.add_argument('t2', required=True)
        parser.add_argument('t3', required=True)
        parser.add_argument('t4', required=True)
        parser.add_argument('t5', required=True)   
        parser.add_argument('ct', required=True)  
        parser.add_argument('ps', required=True)      
        args = parser.parse_args()  # parse arguments to dictionary

        # create new dataframe containing new values
        new_data = pd.DataFrame({
            'timestamp': args['timestamp'],
            't1': [args['t1']],
            't2': [args['t2']],
            't3': [args['t3']],
            't4': [args['t4']],
            't5': [args['t5']],    
            'ct': [args['ct']], 
            'ps': [args['ps']]         
        })
        # read our CSV
        data = pd.read_csv('data.csv')
        # add the newly provided values
        data = data.append(new_data, ignore_index=True)
        # save back to CSV
        #data.to_csv('data.csv', index=False)
        return {'data': data.to_dict()}, 200  # return data with 200 OK
        
    def put(self):
        parser = reqparse.RequestParser()  # initialize     
        parser.add_argument('timestamp', required=True)  # add args
        parser.add_argument('t1', required=True)
        parser.add_argument('t2', required=True)
        parser.add_argument('t3', required=True)
        parser.add_argument('t4', required=True)
        parser.add_argument('t5', required=True)   
        parser.add_argument('ct', required=True)  
        parser.add_argument('ps', required=True)       
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('data.csv')
            
        # update data
        data['timestamp'] = args['timestamp']
        data['t1'] = args['t1']
        data['t2'] = args['t2']
        data['t3'] = args['t3']
        data['t4'] = args['t4']
        data['t5'] = args['t5']   
        data['ct'] = args['ct'] 
        data['ps'] = args['ps'] 
            # save back to CSV
        data.to_csv('data.csv', index=False)
            # return data and 200 OK
        
        return {'data': data.to_dict()}, 200

    def get(self):
        data = pd.read_csv('data.csv')  # read CSV
        data = data.to_dict()  # convert dataframe to dictionary
        #print(data)
        return {'data': data}, 200  # return data and 200 OK code

class TinyHouseData(Resource):
    def put(self):
        parser = reqparse.RequestParser()  # initialize     
        parser.add_argument('timestamp', required=True)  # add args
        parser.add_argument('t1', required=True)
        parser.add_argument('t2', required=True)
        parser.add_argument('t3', required=True)
        parser.add_argument('t4', required=True)
        parser.add_argument('t5', required=True)   
        parser.add_argument('ct', required=True)  
        parser.add_argument('t6', required=True)    
        parser.add_argument('source', required=True)     
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('tinydata.csv')
            
        # update data
        data['timestamp'] = args['timestamp']
        data['t1'] = args['t1']
        data['t2'] = args['t2']
        data['t3'] = args['t3']
        data['t4'] = args['t4']
        data['t5'] = args['t5']   
        data['ct'] = args['ct'] 
        data['t6'] = args['t6'] 
        data['source'] = args['source'] 
            # save back to CSV
        data.to_csv('tinydata.csv', index=False)
            # return data and 200 OK
        try:
            q_data = query.format(args['timestamp'],args['t1'],args['t2'],args['t3'],args['t4'],args['t5'],args['ct'],args['t6'],args['source'])
            cur.execute(q_data)
            conn.commit()
        except Exception as e:
            print(e)
        return {'data': data.to_dict()}, 200

    def get(self):
        data = pd.read_csv('tinydata.csv')  # read CSV
        data = data.to_dict()  # convert dataframe to dictionary
        #print(data)
        return {'data': data}, 200  # return data and 200 OK code

@app.route('/line')
def line():
    t1 = []
    t2 = []
    t3 = []
    t4 = []
    t5 = []
    t6 = []
    ct = []
    timestamp = []
    source = "none"
    query2 = "SELECT * FROM tinyhousedata ORDER BY data_id DESC LIMIT 10;"
    cur.execute(query2)
    row = cur.fetchone()
    data = []
    while row is not None:
        data.append(row)
        row = cur.fetchone()

    for i in data:
        timestamp.append(i[1])
        t1.append(int(float(i[2])))
        t2.append(int(float(i[3])))
        t3.append(int(float(i[4])))
        t4.append(int(float(i[5])))
        t5.append(int(float(i[6]))) 
        t6.append(int(float(i[8])))  
        ct.append(int(float(i[7])))
        source = i[9]

    timestamp.reverse()
    t1.reverse()
    t2.reverse()
    t3.reverse()
    t4.reverse()
    t5.reverse()
    t6.reverse()
    ct.reverse()
    #cur.close()
    xs = range(len(timestamp))
    test = plt.figure(figsize=(18,10))
    plt.subplot(211)

    plt.grid(True)
    plt.plot(xs,t1,"tab:blue", label="t1")
    plt.plot(xs,t2,"tab:orange", label="t2")
    plt.plot(xs,t3,"tab:green", label="t3")
    plt.plot(xs,t4,"tab:red", label="t4")
    plt.plot(xs,t5,"tab:purple", label="t5")
    plt.plot(xs,t6,"tab:brown", label="t6")
    plt.ylabel("Temperature [°C]")
    plt.xlabel("Timestamp: " + timestamp[1] + "   to   " + timestamp[-1])
    plt.title("Temperature")
    plt.legend()
    plt.subplot(212)
    plt.grid(True)
    plt.plot(xs,ct,"tab:cyan", label="Power")
    plt.ylabel("Power [watts]")
    plt.xlabel("Timestamp: " + timestamp[1] + "   to   " + timestamp[-1])
    plt.title("Power usage " + source)
    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
    plt.legend()
    canvas = FigureCanvas(test)
    output = io.BytesIO()
    #canvas.print_png(output)
    canvas.print_jpg(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/jpeg'
    return response

@app.route('/fuelcell')
def fuelcell():
    query = "SELECT * FROM tinyhousedata WHERE source = 'fuelcell';"
    return(Getdata_from_database(query))

@app.route('/grid')
def grid():
    query = "SELECT * FROM tinyhousedata WHERE source = 'grid';"
    return(Getdata_from_database(query))

api.add_resource(Data, '/data')  #: '/data' is our entry point
api.add_resource(TinyHouseData,'/tinyhousedata')

if __name__ == '__main__':
    app.run()  # run our Flask app
