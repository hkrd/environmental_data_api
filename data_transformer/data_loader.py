import netCDF4 as nc
import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


def parse_nc_file(file_path, chunk_size=10000):
    # Open the NetCDF file
    dataset = nc.Dataset(file_path, 'r')

    # Extract variables
    lat = dataset.variables['lat'][:]
    lon = dataset.variables['lon'][:]
    pm25 = dataset.variables['GWRPM25'][:]
    year = int(str(dataset.Start_Date)[:4])

    # Get total number of data points
    total_points = len(lat) * len(lon)

    # Function to yield chunks of data
    def data_generator():
        for i in range(0, total_points, chunk_size):
            lat_index = i // len(lon)
            lon_index = i % len(lon)
            
            chunk_size_lat = min(chunk_size // len(lon) + 1, len(lat) - lat_index)
            chunk_size_lon = min(chunk_size, len(lon) - lon_index)
            
            chunk_lat = np.repeat(lat[lat_index:lat_index+chunk_size_lat], chunk_size_lon)
            chunk_lon = np.tile(lon[lon_index:lon_index+chunk_size_lon], chunk_size_lat)
            chunk_pm25 = pm25[lat_index:lat_index+chunk_size_lat, lon_index:lon_index+chunk_size_lon].flatten()

            chunk = pd.DataFrame({
                'Year': year,
                'Latitude': chunk_lat.astype(float),
                'Longitude': chunk_lon.astype(float),
                'PM2.5 Level': chunk_pm25.astype(float)
            })
            chunk = chunk.dropna(subset=['PM2.5 Level'])
            yield chunk

    return data_generator, total_points
