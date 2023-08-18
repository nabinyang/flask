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
import sys
import os
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)
 
# now we can import the module in the parent
# directory.
import db_config
#from db_config import db
samples = db_config.db.samples
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
        "safety_center_v2.csv", 
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
    result = {"counts": {}, "list": {}}
    # Iterate over each file
    for file in files:
        # Join the base directory path and file name
        full_path = os.path.join(base_dir, file)
        df = pd.read_csv(full_path)

        # Convert the latitude and longitude to numeric
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        #print(df['latitude'], df['longitude'])
        #print(latitude, longitude)
        # Calculate distances for all points in the dataframe
        distances = haversine_vectorize(latitude, longitude, df['latitude'], df['longitude'])

        # Count the number of points within the radius
        count = int((distances <= radius).sum())
        result_df= df.loc[distances <= radius, ['latitude', 'longitude']].values.tolist()
        #print(f'result_df: {result_df}')
        results[file] = count
        result["counts"][file] = count
        result["list"][file] = result_df
        #result['counts']= {file: count}
        #result['list'] = {file: result_df}
    #print(f'results: {results}')
    #print(f'result: {result}')
    return result


def score_with_weights(results):
    
    score_result = {}

    location_score = 0
    facility_score = 0
    support_score = 0

    location_score += results["counts"]['entertainment_establishments_v1.csv'] * (-30)
    location_score += results["counts"]['police_office_v1.csv'] * 80
    location_score += results["counts"]['safety_center_v2.csv'] * 80
    location_score += results["counts"]['street_lamp_v1.csv'] * 20
    location_score += results["counts"]['bus_stop_v1.csv'] * 50
    
    facility_score += results['doorLock'] * 130
    facility_score += results['keypad'] * 100
    facility_score += results['frontCCTV'] * 100
    facility_score += results['deliveryBox']  * 50

    support_score += results["counts"]['ansimee_cctv_v1.csv'] * 5 
    support_score += results["counts"]['emergency_bell_v1.csv'] * 30
    support_score += results["counts"]['women_protective_house_v1.csv'] * 60
    support_score += results["counts"]['women_protective_parcel_v1.csv'] * 30
    
    score_result['location score'] = location_score
    score_result['facility score'] = facility_score
    score_result['support score'] = support_score
    score_result['total score'] = location_score + facility_score + support_score
    
    return score_result


def percentile_rank(scores, target_score):
    sorted_scores = sorted(scores, reverse=True)
    total_scores = len(sorted_scores)
    
    lower_scores = [score for score in sorted_scores if score <= target_score]
    lower_count = len(lower_scores)
    
    percentile = (lower_count / total_scores) * 100
    return percentile

def assign_grade(score):
    if score >= 90:
        return 1
    elif score >= 80:
        return 2
    elif score >= 70:
        return 3
    elif score >= 60:
        return 4
    elif score >= 50:
        return 5
    elif score >= 40:
        return 6
    elif score >= 30:
        return 7
    elif score >= 20:
        return 8
    elif score >= 10:
        return 9
    else:
        return 10
# 사용 예시
#all_scores = [85, 90, 78, 95, 67, 88, 76, 92, 81, 70]
#input_score = int(input("Enter a score: "))
#percentile = percentile_rank(all_scores, input_score)
#print(f"The score {input_score} is in the {percentile:.2f}% percentile.")
def relative_rating(my_location_score, my_facility_score, my_support_score, my_total_score):
    location_scores = []
    facility_scores = []
    support_scores = []
    total_scores = []
    count = 0
    for x in samples.find():
        count += 1
        location_scores.append(int(x['location_score']))
        facility_scores.append(int(x['facility_score']))
        support_scores.append(int(x['support_score']))
        total_scores.append(int(x['total_score']))

        #print(x)
    #print(count)
    result = {}
    result['loc_percent'] = percentile_rank(location_scores, my_location_score)
    result['fac_percent'] = percentile_rank(facility_scores, my_facility_score)
    result['sup_percent'] = percentile_rank(support_scores, my_support_score)
    result['tot_grade'] = assign_grade(percentile_rank(total_scores, my_total_score))
    return result
    '''
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
    '''

#relative_rating()