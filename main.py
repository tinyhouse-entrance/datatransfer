#region Library 
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import psycopg2
#endregion library 

#region variables
app = Flask(__name__)
api = Api(app)
app.route('/')

DATABASE_URL = 'postgres://whheiyecnfjvze:e54c8491ffe0b37679db8a943fe672d876f440a3936d04724e7f0b82b7df9b6f@ec2-54-229-68-88.eu-west-1.compute.amazonaws.com:5432/dekdht4ds841en'
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
query = "INSERT INTO tinyhousedata(timestamp,t1,t2,t3,t4,t5,ct1,ps,source) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}');"

#endregion variables

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
        parser.add_argument('t6', required=True)  
        parser.add_argument('source', required=True)   
        args = parser.parse_args()  # parse arguments to dictionary

        # create new dataframe containing new values
        new_data = pd.DataFrame({
            'timestamp': [args['timestamp']],
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
        data.to_csv('data.csv', index=False)
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



api.add_resource(Data, '/data')  #: '/data' is our entry point
api.add_resource(TinyHouseData,'/tinyhousedata')

if __name__ == '__main__':
    app.run()  # run our Flask app
