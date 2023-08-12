# dataloader/dataloader.py

"""
This module provides functions for loading geospatial data from various 
.csv files and for performing distance-based calculations on that data.

It defines two functions:
- haversine_vectorize, which calculates the haversine distance between 
  two points on the Earth's surface.
- count_place, which counts the number of geographical features within 
  a certain radius of a specified point.
"""


import pandas as pd
from haversine import haversine, Unit
from numpy import radians, cos, sin, arcsin, sqrt
import os

def haversine_vectorize(lat1, lon1, lat2, lon2):
    """
    Calculate the haversine distance between two points on the Earth's surface.

    Parameters:
    lat1 -- latitude of the first point
    lon1 -- longitude of the first point
    lat2 -- latitude of the second point
    lon2 -- longitude of the second point

    Returns:
    The haversine distance between the two points, in kilometers.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * arcsin(sqrt(a))
    km = 6371 * c
    return km

def count_place(latitude, longitude, radius=1,
    files = [
        "ansimee_cctv_v1.csv", 
        "emergency_bell_v1.csv",
        "entertainment_establishments_v1.csv", 
        "police_office_v1.csv",
        "safety_center_v1.csv", 
        "street_lamp_v1.csv", 
        "women_protective_house_v1.csv",
        "women_protective_parcel_v1.csv",
        "bus_stop_v1.csv"
    ]):
    """
    Count the number of geographical features from various .csv files 
    within a certain radius of a specified point.

    Parameters:
    latitude -- the latitude of the point
    longitude -- the longitude of the point
    radius -- the radius within which to count features (default 5)
    files -- a list of .csv file names containing geospatial data (default is a list of eight specific files)

    Returns:
    A dictionary mapping file names to the count of features within the radius.
    """
    
    # List of filenames
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets\datasets\coordinate_based')
    results = {}
    # Iterate over each file
    for file in files:
        # Join the base directory path and file name
        full_path = os.path.join(base_dir, file)
        df = pd.read_csv(full_path)

        # Convert the latitude and longitude to numeric
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

        # Calculate distances for all points in the dataframe
        distances = haversine_vectorize(latitude, longitude, df['latitude'], df['longitude'])

        # Count the number of points within the radius
        count = int((distances <= radius).sum())
        
        results[file] = count
    return results


def score_with_weights(results):
    score_result = {}

    location_score = 0
    facility_score = 0
    support_score = 0

    location_score += results['entertainment_establishments_v1.csv'] * (-30)
    location_score += results['police_office_v1.csv'] * 80
    location_score += results['safety_center_v1.csv'] * 80
    location_score += results['street_lamp_v1.csv'] * 20
    location_score += results['bus_stop_v1.csv'] * 50
    
    facility_score += results['doorLock'] * 130
    facility_score += results['keypad'] * 100
    facility_score += results['frontCCTV'] * 100
    facility_score += results['deliveryBox']  * 50

    support_score += results['ansimee_cctv_v1.csv'] * 5 
    support_score += results['emergency_bell_v1.csv'] * 30
    support_score += results['women_protective_house_v1.csv'] * 60
    support_score += results['women_protective_parcel_v1.csv'] * 30
    
    score_result['location score'] = location_score
    score_result['facility score'] = facility_score
    score_result['support score'] = support_score
    score_result['total score'] = location_score + facility_score + support_score
    
    return score_result
