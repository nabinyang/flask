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
import db_config
from pymongo.mongo_client import MongoClient

homeSurveys = db_config.homeSurveys
generalSurveys = db_config.generalSurveys
alarm = db_config.alarm

survey_api = Namespace(
    name='Survey',
    description='API for saving survey results'
)


@survey_api.route('/saveHomeSurvey')
class Saving(Resource):
    def post(self):
        result = {}
        result['authCode'] = str(request.form['authCode'])
        result['id'] = int(request.form['id'])
        result['address'] = str(request.form['address'])
        result['roomNo'] = int(request.form['requestNumber'])
        result['toiletNo'] = int(request.form['toiletNumber'])
        result['floorNo'] = int(request.form['floorNumber'])
        result['facility'] = list(request.form['facility'])
        result['safeLevel'] = int(request.form['saveLevel'])
        result['noSafetyReason'] = list(request.form['noSafetyReason'])
        result['standard'] = list(request.form['standard'])
        result['safety'] = list(request.form['safety'])
        result['prefer1'] = int(request.form['prefer1'])
        result['prefer2'] = int(request.form['prefer2'])
        result['prefer3'] = int(request.form['prefer3'])
        result['prefer4'] = int(request.form['prefer4'])


        try:
            homeSurveys.insert_one(jsonify(result))
            alarm_list = {}
            alarm['authCode'] = str(request.form['authCode'])
            alarm['homeSurveyAlarm'] = '설문결과완료'
            try: 
                alarm.insert_one(alarm_list)
                return "success"
            except Exception as e:
                return e
            
        except Exception as e:
            
            return e
        

@survey_api.route('/saveGeneralSurvey')
class Saving(Resource):
    def post(self):
        result = {}
        # page 1
        result['authCode'] = int(request.form['authCode'])
        result['safeLevel'] = int(request.form['safeLevel'])
        result['CP'] = int(request.form['CP'])
        result['location'] = int(request.form['location'])
        result['neighbors'] = int(request.form['neighbors'])
        result['ambience'] = int(request.form['ambience'])
        result['facility'] = list(request.form['facility'])
        result['ent'] = int(request.form['ent'])
        result['accident'] = list(request.form['accident'])
        result['reason'] = str(request.form['reason'])
        #page2
        result['importance'] = list(request.form['importance'])
        result['floor'] = int(request.form['floor'])
        result['road'] = int(request.form['road'])
        result['size'] = int(request.form['size'])
        result['new'] = int(request.form['new'])
        result['safeFacility'] = list(request.form['safeFacility'])
        result['extraSafeFacility'] = str(request.form['extraSafeFacility'])
        try: 
           
           homeSurveys.insert_one(jsonify(result))

           return "success"
        except Exception as e:
            
            return e