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
from dataloader.dataloader import count_place, score_with_weights  # Update the import statement
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
        # Get latitude and longitude from the query parameters
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        
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
        
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        
        # Call the dataloader function
        result = count_place(latitude, longitude)
        
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
        addr = request.form['addr']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        # Call the dataloader function
        result = count_place(latitude, longitude)

        # Add additional information to the result
        add_info = {}

        add_info['doorLock'] = int(request.args.get('doorLock')) # 1 if there is a door lock else 0
        add_info['keypad'] = int(request.args.get('keyPad')) # 1 if there is a key pad else 0
        add_info['frontCCTV'] = int(request.args.get('frontCCTV')) # 1 if there is a cctv at the front else 0
        add_info['deliveryBox'] = int(request.args.get('deliveryBox')) # 1 if there is a delivery box else 0
        add_info['latitude'] = latitude,
        add_info['longitude'] = longitude,
        add_info['address'] = addr

        result.update(add_info)
        score = score_with_weights(result)

        final_json = score.update(add_info)
        # Calculate the rating
        #counts = list(result.values())
        #rating = sum(counts) / len(counts) if counts else 0
        return final_json
        
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
