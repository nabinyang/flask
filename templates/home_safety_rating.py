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
from dataloader.dataloader import count_place, score_with_weights, count_places, relative_rating  # Update the import statement
import numpy as np
from urllib import parse
from PyKakao import Local


api = Local(service_key = "4c682d5d0c62b5c4a5d3e66d9c2c87e0")



ratings = db.ratings
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


@home_safety_rating_api.route('/ratingresult')
class RelativeRating(Resource):
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
        print(score)
        counts = count_places(result)
        print(counts)
        relative_ratings = relative_rating(score['location score'], score['facility score'], score['support score'], score['total score'])
        rel_result = {}
        rel_result['address'] = row['address']
        rel_result['rating'] = relative_ratings['tot_grade']
        rel_result['total_score'] = score['total score']
        rel_result['location_percent'] = relative_ratings['loc_percent']
        rel_result['facility_percent']= relative_ratings['fac_percent']
        rel_result['support_percent']= relative_ratings['sup_percent']
        #rel_result['no_of_polices'] = counts['noOfPoliceOffices']
        #rel_result['no_of_safetyCenters'] = counts['noOfSafetyCenters']
        #rel_result['no_of_ansimees'] = counts['noOfBusStops']
        #rel_result['no_of_busStops'] = counts['noOfWomenProtectiveCcenters']
        
        #print(final_json)
        # Calculate the rating
        #counts = list(result.values())
        #rating = sum(counts) / len(counts) if counts else 0
        return rel_result
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
