# apis/home_safety_rating.py
"""
This module defines the Flask-RestX resources for the Home Safety Rating API.

The Home Safety Rating API provides resources for fetching safety-related data 
based on geographical location and for performing safety rating calculations 
and anomaly detection on that data.
"""

import os
import sys
from db_config import db
from pymongo.mongo_client import MongoClient
from flask import request
from flask import jsonify
from flask_restx import Namespace, Resource
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from dataloader.dataloader import count_place, score_with_weights, relative_rating  # Update the import statement
import numpy as np
from urllib import parse
from PyKakao import Local


api = Local(service_key = "4c682d5d0c62b5c4a5d3e66d9c2c87e0")



ratings = db.ratings
surveys = db.homeSurveys

#surs = surveys.find()
#for sur in surs:
#    print(sur)
home_safety_rating_api = Namespace('home_safety_rating')

@home_safety_rating_api.route('/findLocation')
class Find(Resource):
    """
    Count resource for the Home Safety Rating API.

    Provides the count of various safety-related features around a specific 
    geographical location.
    """
    def get(self):
        """
            Fetch the count of safety-related features for a specific location.

            Query Parameters:
            latitude -- the latitude of the location
            longitude -- the longitude of the location

            Returns:
            A JSON object mapping safety feature types to their respective counts.
        """

        
        addr = str(request.form['addr'])


        result = api.search_address(addr)
        if result['meta']['total_count'] > 0:

            row = {
                'addr': addr,
                'longitude': result['documents'][0]['x'], 
                'latitude': result['documents'][0]['y'], 
            }
        
        return jsonify(row)



@home_safety_rating_api.route('/count')
class Count(Resource):
    """
    Count resource for the Home Safety Rating API.

    Provides the count of various safety-related features around a specific 
    geographical location.
    """
    def get(self):
        """
            Fetch the count of safety-related features for a specific location.

            Query Parameters:
            latitude -- the latitude of the location
            longitude -- the longitude of the location

            Returns:
            A JSON object mapping safety feature types to their respective counts.
        """
        req = request.get_json()
        # Get latitude and longitude from the query parameters
        latitude = float(req['latitude'])
        longitude = float(req['latitude'])
        
        # Call the dataloader function
        result = count_place(latitude, longitude)
        return jsonify(result)

@home_safety_rating_api.route('/rating')
class Rating(Resource):
    """
    Rating resource for the Home Safety Rating API.

    Provides a safety rating for a specific geographical location, 
    based on the count of various safety-related features around that location.
    """
    def get(self):
        """
        Fetch the safety rating for a specific location.

        Query Parameters:
        latitude -- the latitude of the location
        longitude -- the longitude of the location

        Returns:
        A JSON object containing the safety rating.
        """
        # Get latitude and longitude from the query parameters
        req = request.get_json()
        address = req['address']
        result = api.search_address(address)
        if result['meta']['total_count'] > 0:

            row = {
                'addr': address,
                'longitude': result['documents'][0]['x'], 
                'latitude': result['documents'][0]['y'], 
            }
        #latitude = float(req['latitude'])
        #longitude = float(req['latitude'])
        
        # Call the dataloader function
        result = count_place(row['latitude'], row['longitude'])
        
        # Calculate the rating
        counts = list(result.values())
        rating = sum(counts) / len(counts) if counts else 0
        #return result
        #return {"rating": rating}

@home_safety_rating_api.route('/score')
class Scoring(Resource):
    """
    Rating resource for the Home Safety Rating API.

    Provides a safety rating for a specific geographical location, 
    based on the count of various safety-related features around that location.
    """
    def get(self):
        """
        Fetch the safety rating for a specific location.

        Query Parameters:
        latitude -- the latitude of the location
        longitude -- the longitude of the location

        Returns:
        A JSON object containing the safety rating.
        """


        # Get latitude and longitude from the query parameters
        
        req = request.get_json()
        address = req['address']
        result = api.search_address(address)
        if result['meta']['total_count'] > 0:

            row = {
                'address': address,
                'longitude': result['documents'][0]['x'], 
                'latitude': result['documents'][0]['y'], 
            }
        #print(row['latitude'], row['longitude'])
        #latitude = request.form['latitude']
        #longitude = request.form['longitude']

        # Call the dataloader function
        result = count_place(float(row['latitude']), float(row['longitude']))

        # Add additional information to the result
        add_info = {}

        add_info['doorLock'] = int(req['doorLock']) # 1 if there is a door lock else 0
        add_info['keypad'] = int(req['keypad']) # 1 if there is a key pad else 0
        add_info['frontCCTV'] = int(req['frontCCTV']) # 1 if there is a cctv at the front else 0
        add_info['deliveryBox'] = int(req['deliveryBox']) # 1 if there is a delivery box else 0
        add_info['latitude'] = float(row['latitude'])
        add_info['longitude'] = float(row['longitude'])
        add_info['address'] = row['address']

        result.update(add_info)
        #print(result)
        score = score_with_weights(result)

        #print(score)
        score.update(add_info)
        #print(final_json)
        # Calculate the rating
        #counts = list(result.values())
        #rating = sum(counts) / len(counts) if counts else 0
        return score


@home_safety_rating_api.route('/showResult')
class RelativeRating(Resource):
    """
    Rating resource for the Home Safety Rating API.

    Provides a safety rating for a specific geographical location, 
    based on the count of various safety-related features around that location.
    """
    def post(self):
        """
        Fetch the safety rating for a specific location.

        Query Parameters:
        latitude -- the latitude of the location
        longitude -- the longitude of the location

        Returns:
        A JSON object containing the safety rating.
        """
        # Get latitude and longitude from the query parameters
        params = request.get_json()
        id_ = int(params['id'])
        survey_no = int(params['surveyNo'])
        #print(params)
        #print(params['id'])
        try:
            
            survey = surveys.find_one(params)
            #print(survey)
            if survey is None:
                return '저장된 결과 없음'
            else:
        
        
                address = survey['address']
                facility = survey['facility']
                result = api.search_address(address)
                if result['meta']['total_count'] > 0:

                    row = {
                        'address': address,
                        'longitude': result['documents'][0]['x'], 
                        'latitude': result['documents'][0]['y'], 
                    }
                #print(row['latitude'], row['longitude'])
                #latitude = request.form['latitude']
                #longitude = request.form['longitude']

                # Call the dataloader function
                result = count_place(float(row['latitude']), float(row['longitude']))

                # Add additional information to the result
                add_info = {}
                if '도어락' in facility:
                    add_info['doorLock'] = 1 # 1 if there is a door lock else 0
                else: 
                    add_info['doorLock'] = 0
                if '키패드' in facility:
                    add_info['keypad'] = 1 # 1 if there is a door lock else 0
                else: 
                    add_info['keypad'] = 0
                if 'CCTV' in facility:
                    add_info['frontCCTV'] = 1 # 1 if there is a door lock else 0
                else: 
                    add_info['frontCCTV'] = 0
                if '택배함' in facility:
                    add_info['deliveryBox'] = 1 # 1 if there is a door lock else 0
                else: 
                    add_info['deliveryBox'] = 0
                
                add_info['latitude'] = float(row['latitude'])
                add_info['longitude'] = float(row['longitude'])
                add_info['address'] = row['address']
                result.update(add_info)
                #print(f'result: {result}')
                score = score_with_weights(result)

                #print(f'result: {result}')
                score.update(add_info)
                #print(f'score: {score}')
         
                relative_ratings = relative_rating(score['location score'], score['facility score'], score['support score'], score['total score'])
                rel_result = {}
                rel_result['id'] = params['id']
                rel_result['surveyNo'] = params['surveyNo']
                rel_result['address'] = row['address']
                rel_result['rating'] = relative_ratings['tot_grade']
                rel_result['total_score'] = score['total score']
                rel_result['location_percent'] = relative_ratings['loc_percent']
                rel_result['facility_percent']= relative_ratings['fac_percent']
                rel_result['support_percent']= relative_ratings['sup_percent']
                rel_result['no_of_polices'] = result["counts"]['police_office_v1.csv']
                rel_result['no_of_safetyCenters'] = result["counts"]['safety_center_v2.csv']
                rel_result['no_of_ansimees'] = result["counts"]['women_protective_house_v1.csv']
                rel_result['no_of_busStops'] = result["counts"]['bus_stop_v1.csv']
                rel_result['list_of_polices'] = result["list"]['police_office_v1.csv']
                rel_result['list_of_safetyCenters'] = result["list"]['safety_center_v2.csv']
                rel_result['list_of_ansimees'] = result["list"]['women_protective_house_v1.csv']
                rel_result['list_of_busStops'] = result["list"]['bus_stop_v1.csv']
        
                #print('rel_result: ', rel_result)
                try: 
                    #ratings.insert_one({'id': id_, 'nickname': nickname})
                    ratings.insert_one(rel_result)
                    #print('success1')
                    #return jsonify({'response': 'success1'})
                    return "success"
                
                except Exception as e:
                    print(e)
                    response = {'response': e}
                    #return jsonify(response)
                    return "오류1"
        except Exception as e:
                print(e)
                response = {'response': e}
                #return jsonify(response)
                return "오류2"
        #return rel_result
    
@home_safety_rating_api.route('/saveRating')
class Saving(Resource):
    """
    Rating resource for the Home Safety Rating API.

    Provides a safety rating for a specific geographical location, 
    based on the count of various safety-related features around that location.
    """
    def post(self):
        """
        Fetch the safety rating for a specific location.

        Query Parameters:
        latitude -- the latitude of the location
        longitude -- the longitude of the location

        Returns:
        A JSON object containing the safety rating.
        """
        # Get latitude and longitude from the query parameters
        #latitude = float(request.args.get('latitude'))
        #longitude = float(request.args.get('longitude'))
        # Get the rating 

        authCode = request.form['authCode']
        result = request.json('result')
        
        add_info = {}
        add_info['authCode'] = authCode
        result.update(add_info)
        try: 
            ratings.insert_one(result)
            return 'success'
        except Exception as e:
            return e
        # Calculate the rating
        #counts = list(result.values())
        #rating = sum(counts) / len(counts) if counts else 0
        #return score

@home_safety_rating_api.route('/findResult')
class Showing(Resource):
    """
    Rating resource for the Home Safety Rating API.

    Provides a safety rating for a specific geographical location, 
    based on the count of various safety-related features around that location.
    """
    def get(self):
        """
        Fetch the safety rating for a specific location.

        Query Parameters:
        latitude -- the latitude of the location
        longitude -- the longitude of the location

        Returns:
        A JSON object containing the safety rating.
        """
        # Get latitude and longitude from the query parameters
        #latitude = float(request.args.get('latitude'))
        #longitude = float(request.args.get('longitude'))
        # Get the rating 
        #name = request.form['name']
        authCode = request.form['authCode']
        try: 
            result = ratings.rating.find({'authCode':authCode})
            if result is None:
                return 'No result'
            else: 
                return result
        except Exception as e: 
            return e

        # Calculate the rating
        #counts = list(result.values())
        #rating = sum(counts) / len(counts) if counts else 0
        #return score

@home_safety_rating_api.route('/anomaly')
class Anomaly(Resource):
    """
    Anomaly resource for the Home Safety Rating API.

    Provides an anomaly detection for a specific geographical location, 
    based on the count of various safety-related features around that location.
    """
    def get(self):
        """
        Detect anomalies in the safety-related feature counts for a specific location.

        Query Parameters:
        latitude -- the latitude of the location
        longitude -- the longitude of the location

        Returns:
        A JSON object mapping safety feature types to boolean values indicating 
        whether an anomaly was detected for each feature.
        """
        # Get latitude and longitude from the query parameters
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        
        # Call the dataloader function
        result = count_place(latitude, longitude)
        
        # Detect anomalies
        counts = np.array(list(result.values()))
        mean = counts.mean()
        std = counts.std()
        anomalies = (np.abs(counts - mean) > 2 * std).tolist()
        
        return {"anomalies": anomalies}
