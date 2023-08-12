import os
import sys
import pickle
import pandas as pd
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from dataloader.dataloader import count_place
from sklearn.preprocessing import MinMaxScaler


def generate_coordinates(n, lat_bounds, lon_bounds):
    """
    Generate random geographical coordinates within specified bounds.

    Parameters:
    n -- number of coordinates to generate
    lat_bounds -- tuple of lower and upper bounds for latitude
    lon_bounds -- tuple of lower and upper bounds for longitude

    Returns:
    A list of (latitude, longitude) tuples.
    """
    lats = np.random.uniform(lat_bounds[0], lat_bounds[1], n)
    lons = np.random.uniform(lon_bounds[0], lon_bounds[1], n)
    return list(zip(lats, lons))

def generate_data(n, lat_bounds=(37.426, 37.701), lon_bounds=(126.764, 127.183)):
    """
    Generate a pandas DataFrame with random geographical coordinates in Seoul 
    and their corresponding counts of nearby geographical features.

    Parameters:
    n -- number of rows in the DataFrame
    lat_bounds -- tuple of lower and upper bounds for latitude (default is the bounds for Seoul)
    lon_bounds -- tuple of lower and upper bounds for longitude (default is the bounds for Seoul)

    Returns:
    A pandas DataFrame.
    """
    coords = generate_coordinates(n, lat_bounds, lon_bounds)

    data = []
    for lat, lon in coords:
        counts = count_place(lat, lon)
        if sum(counts.values()) == 0:
            continue
        counts["latitude"] = lat
        counts["longitude"] = lon
        data.append(counts)

    df = pd.DataFrame(data)

    # Initialize a MinMaxScaler
    scaler = MinMaxScaler()

    # Normalize the count data and add it to the DataFrame
    for file in df.columns:
        if file not in ["latitude", "longitude"]:
            # Normalize the count data using MinMaxScaler and save the scaler
            df[[file]] = scaler.fit_transform(df[[file]])

            # Save the scaler for each column separately
            with open(f'./weight/scaler_{file}.pkl', 'wb') as f:
                pickle.dump(scaler, f)

    return df

def main():
    df = generate_data(10000)
    df.to_csv("./data/train.csv", index=False)

if __name__ == "__main__":
    main()
