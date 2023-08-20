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
import json
from bson import json_util 
#from pymongo.mongo_client import MongoClient

homeSurveys = db.homeSurveys
generalSurveys = db.generalSurveys
alarm = db.alarm

survey_api = Namespace(
    name='survey',
    description='API for saving survey results'
)


@survey_api.route('/saveHomeSurvey')
class SavingHomeSurvey(Resource):
    def post(self):
        params = request.get_json()
        result = {}
        result['id'] = int(params['id'])
        result['address'] = str(params['address'])
        result['dwellingType'] = str(params['dwellingType'])
        result['toiletNumber'] = str(params['toiletNumber'])
        result['floorNumber'] = str(params['floorNumber'])
        result['facility'] = list(params['facility'])
        result['standard'] = list(params['standard'])
        result['prefer1'] = str(params['prefer1'])
        result['prefer2'] = str(params['prefer2'])
        result['prefer3'] = str(params['prefer3'])
        result['prefer4'] = str(params['prefer4'])
        result['safety'] = list(params['safety'])
        result['another'] = str(params['another'])
        result['isSafety'] = str(params['isSafety'])
        result['reason'] = str(params['reason'])
        result['yesOrNo'] = list(params['yesOrNo'])
        #return result

        
        try:
            count = homeSurveys.count_documents({'id': result['id']})
            print(f'count: {count}')
            result['surveyNo'] = count + 1
            
            try:
                homeSurveys.insert_one(result)
                alarm_list = {}
                alarm_list['id'] = result['id']
                alarm_list['alarm'] = []
                alarm_list['alarm'].append('설문결과완료')
                try: 
                    alarm.insert_one(alarm_list)
                    return "success"
                except Exception as e:
                    return e
            except Exception as e:
                return e
            
        except Exception as e:
            
            return e
        
@survey_api.route('/showHomeSurvey')
class ShowingHomeSurvey(Resource):
    def get(self):
        params = request.get_json()
        #print(params['id'])
        try:
            survey = homeSurveys.find_one({'id': int(params['id']), 'surveyNo': int(params['surveyNo'])})
            print(type(survey))
            if survey is None:
                return '저장된 결과 없음'
            else:
                result = {}
                result['id'] = survey['id']
                result['surveyNo'] = survey['surveyNo']
                result['address'] = survey['address']
                result['dwellingType'] =survey['dwellingType']
                result['toiletNumber'] = survey['toiletNumber']
                result['floorNumber'] = survey['floorNumber']
                result['facility'] = survey['facility']
                result['standard'] = survey['standard']
                result['prefer1'] = survey['prefer1']
                result['prefer2'] = survey['prefer2']
                result['prefer3'] = survey['prefer3']
                result['prefer4'] = survey['prefer4']
                result['safety'] = survey['safety']
                result['another'] = survey['another']
                result['isSafety'] = survey['isSafety']
                result['reason'] = survey['reason']
                result['yesOrNo'] = survey['yesOrNo']

                return result
            
        except Exception as e:
            
            return e
        

@survey_api.route('/saveGeneralSurvey')
class SavingGeneralSurvey(Resource):
    def post(self):

        params = request.get_json()
        result = {}
        # page 1
        result['id'] = int(params['id'])
        result['safeLevel'] = int(params['safeLevel'])
        result['preventionFacility'] = int(params['preventionFacility'])
        result['location'] = int(params['location'])
        result['neighbors'] = int(params['neighbors'])
        result['ambience'] = int(params['ambience'])
        result['facility'] = int(params['facility'])
        result['ent'] = int(params['ent'])
        result['accident'] = int(params['accident'])
        result['reason'] = str(params['reason'])
        #page2
        result['importance'] = list(params['importance'])
        result['floor'] = int(params['floor'])
        result['road'] = int(params['road'])
        result['size'] = int(params['size'])
        result['new'] = int(params['new'])
        result['safeFacility'] = list(params['safeFacility'])
        result['extraSafeFacility'] = str(params['extraSafeFacility'])
        try: 
           
           generalSurveys.insert_one(result)

           return "success"
        except Exception as e:
            
            return e
        
@survey_api.route('/showGeneralSurvey')
class ShowingGeneralSurvey(Resource):
    def get(self):
        params = request.get_json()
        try:
            survey = generalSurveys.find_one({'id': params['id']})
            if survey is None:
                return '저장된 결과 없음'
            else:
                result = {}
                # page 1
                result['id'] = survey['id']
                result['safeLevel'] = survey['safeLevel']
                result['preventionFacility'] = survey['preventionFacility']
                result['location'] = survey['location']
                result['neighbors'] = survey['neighbors']
                result['ambience'] = survey['ambience']
                result['facility'] = survey['facility']
                result['ent'] = survey['ent']
                result['accident'] = survey['accident']
                result['reason'] = survey['reason']
                #page2
                result['importance'] = survey['importance']
                result['floor'] = survey['floor']
                result['road'] = survey['road']
                result['size'] = survey['size']
                result['new'] = survey['new']
                result['safeFacility'] = survey['safeFacility']
                result['extraSafeFacility'] = survey['extraSafeFacility']
                return survey
        except Exception as e:
            
            return e
