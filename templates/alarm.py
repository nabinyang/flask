# apis/survey.py
"""
This module defines the Flask-RestX resources for the Home Safety Rating API.

The Home Safety Rating API provides resources for fetching safety-related data 
based on geographical location and for performing safety rating calculations 
and anomaly detection on that data.
"""
from flask_restx import Namespace, Resource
from flask import request
from flask import jsonify
from db_config import db
from pymongo.mongo_client import MongoClient

#homeSurveys = db_config.homeSurveys
#generalSurveys = db_config.generalSurveys
alarm = db.alarm


alarm_api = Namespace(
    name='alarm',
    description='API for saving survey results'
)


@alarm_api.route('/showAlarm')
class Saving(Resource):
    def get(self):
        #id = request.form['id']
        params = request.get_json()
        #homeSurveys.find_one({'id': int(params['id'])})
        try: 
            result = alarm.find_one({'id':int(params['id'])})
            if result is None:
                return 'No result'
            else: 
                print('yes')
                print(result)
                #return result['homeSurveyAlarm']
                return return result['alarm']
        except Exception as e: 
            return e
