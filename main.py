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
#endregion variables

class Data(Resource):

    def post(self):
        parser = reqparse.RequestParser()  # initialize     
        parser.add_argument('timestamp', required=True)  # add args
        parser.add_argument('t1', required=True)
        parser.add_argument('t2', required=True)
        parser.add_argument('t3', required=True)
        parser.add_argument('t4', required=True)
        parser.add_argument('co2', required=True)       
        args = parser.parse_args()  # parse arguments to dictionary

        # create new dataframe containing new values
        new_data = pd.DataFrame({
            'timestamp': args['timestamp'],
            't1': [args['t1']],
            't2': [args['t2']],
            't3': [args['t3']],
            't4': [args['t4']],
            'co2': [args['co2']]          
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
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('locations', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('data.csv')
        
        if args['userId'] in list(data['userId']):
            # evaluate strings of lists to lists
            # select our user
            user_data = data[data['userId'] == args['userId']]

            # update user's locations
            user_data['locations'] = args['locations']
            print(args['locations'])
            # save back to CSV
            data.to_csv('data.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the userId does not exist
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404

    def get(self):
        data = pd.read_csv('data.csv')  # read CSV
        data = data.to_dict()  # convert dataframe to dictionary
        #print(data)
        return {'data': data}, 200  # return data and 200 OK code


api.add_resource(Data, '/data')  # '/data' is our entry point

if __name__ == '__main__':
    app.run()  # run our Flask app
