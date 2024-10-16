import os
import math
from data_transformer.data_loader import parse_nc_file
from typing import Optional, List, Tuple, Dict
from tqdm import tqdm
import pandas as pd
import numpy as np
from data_transformer.models import DataEntry, StatsResponse


BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data")
NC_FILES = [os.path.join(BASE_PATH, f) for f in os.listdir(BASE_PATH) if f.endswith(".nc")]


class FileProcessor:
    def __init__(self):
        self.file_info = []
        self.cumulative_points = 0
        self.year_stats: Dict[int, Dict] = {}
        self.modified_entries = {}  # Dictionary to store modified entries

    def initialize_data(self):
        pbar = tqdm(NC_FILES, desc="Initializing data", unit="file")
        
        for file in pbar:
            data_gen, file_total_points = parse_nc_file(file, 100000)
            
            first_page = math.floor(self.cumulative_points / 100) + 1
            last_page = math.ceil((self.cumulative_points + file_total_points) / 100)
            
            file_info = {
                "file": os.path.basename(file),
                "total_points": file_total_points,
                "first_page": first_page,
                "last_page": last_page
            }
            self.file_info.append(file_info)
            self.cumulative_points += file_total_points
            
            # Pre-compute stats for each year
            for chunk in data_gen():
                years = chunk['Year'].unique()
                for year in years:
                    year_data = chunk[chunk['Year'] == year]['PM2.5 Level']
                    if year not in self.year_stats:
                        self.year_stats[year] = {
                            'count': 0,
                            'sum': 0,
                            'min': np.inf,
                            'max': -np.inf
                        }
                    self.year_stats[year]['count'] += len(year_data)
                    self.year_stats[year]['sum'] += year_data.sum()
                    self.year_stats[year]['min'] = min(self.year_stats[year]['min'], year_data.min())
                    self.year_stats[year]['max'] = max(self.year_stats[year]['max'], year_data.max())
            
            pbar.set_postfix({"Total Points": self.cumulative_points})

    def process_chunk(self, chunk: pd.DataFrame, year: Optional[int] = None, lat: Optional[float] = None, long: Optional[float] = None) -> List[DataEntry]:
        if year:
            chunk = chunk[chunk['Year'] == year]
        if lat is not None:
            chunk = chunk[chunk['Latitude'].between(lat - 0.01, lat + 0.01)]
        if long is not None:
            chunk = chunk[chunk['Longitude'].between(long - 0.01, long + 0.01)]
        
        if 'PM2_5_Level' not in chunk.columns:
            pm25_columns = [col for col in chunk.columns if 'PM2.5' in col or 'PM2_5' in col]
            if pm25_columns:
                chunk['PM2_5_Level'] = chunk[pm25_columns[0]]
            else:
                chunk['PM2_5_Level'] = None
        
        return [DataEntry(
            Year=row['Year'],
            Latitude=row['Latitude'],
            Longitude=row['Longitude'],
            PM2_5_Level=row['PM2_5_Level']
        ) for _, row in chunk.iterrows()]

    def get_data_generator(self, start: int, end: int, year: Optional[int] = None, lat: Optional[float] = None, long: Optional[float] = None) -> List[Tuple[str, List[DataEntry]]]:
        current_index = 0
        result = []

        for fi in self.file_info:
            file_path = os.path.join(BASE_PATH, fi["file"])
            file_total_points = fi["total_points"]

            if current_index + file_total_points <= start:
                current_index += file_total_points
                continue

            data_gen, _ = parse_nc_file(file_path, 100000)
            for chunk in data_gen():
                if year:
                    chunk = chunk[chunk['Year'] == year]
                if lat is not None:
                    chunk = chunk[chunk['Latitude'].between(lat - 0.01, lat + 0.01)]
                if long is not None:
                    chunk = chunk[chunk['Longitude'].between(long - 0.01, long + 0.01)]
                
                if current_index + len(chunk) > start:
                    start_in_chunk = max(0, start - current_index)
                    end_in_chunk = min(len(chunk), end - current_index)
                    file_data = self.process_chunk(chunk.iloc[start_in_chunk:end_in_chunk])
                    
                    result.append((fi["file"], file_data))
                    
                    if sum(len(data) for _, data in result) >= end - start:
                        return result

                current_index += len(chunk)

            if current_index >= end:
                break

        return result

    def get_total_points(self, year: Optional[int] = None, lat: Optional[float] = None, long: Optional[float] = None) -> int:
        if year is None and lat is None and long is None:
            return self.cumulative_points
        
        if year is not None and lat is None and long is None:
            return self.year_stats[year]['count']
        
        # If we need to filter by lat or long, we need to process the data
        total = 0
        for fi in self.file_info:
            file_path = os.path.join(BASE_PATH, fi["file"])
            data_gen, _ = parse_nc_file(file_path, 100000)
            for chunk in data_gen():
                if year:
                    chunk = chunk[chunk['Year'] == year]
                if lat is not None:
                    chunk = chunk[chunk['Latitude'].between(lat - 0.01, lat + 0.01)]
                if long is not None:
                    chunk = chunk[chunk['Longitude'].between(long - 0.01, long + 0.01)]
                total += len(chunk)
        return total

    def get_stats(self, year: Optional[int] = None) -> StatsResponse:
        if year is not None:
            if year in self.year_stats:
                stats = self.year_stats[year]
                return StatsResponse(
                    count=stats['count'],
                    average_pm2_5=stats['sum'] / stats['count'],
                    min_pm2_5=stats['min'],
                    max_pm2_5=stats['max'],
                    years_available=[year]
                )
            else:
                return StatsResponse(
                    count=0,
                    average_pm2_5=0,
                    min_pm2_5=0,
                    max_pm2_5=0,
                    years_available=[]
                )
        else:
            total_count = sum(stats['count'] for stats in self.year_stats.values())
            total_sum = sum(stats['sum'] for stats in self.year_stats.values())
            return StatsResponse(
                count=total_count,
                average_pm2_5=total_sum / total_count if total_count > 0 else 0,
                min_pm2_5=min(stats['min'] for stats in self.year_stats.values()),
                max_pm2_5=max(stats['max'] for stats in self.year_stats.values()),
                years_available=sorted(self.year_stats.keys())
            )

    def get_entry_by_id(self, entry_id: int) -> Optional[DataEntry]:
        if entry_id in self.modified_entries:
            return self.modified_entries[entry_id]

        results = self.get_data_generator(entry_id, entry_id + 1)
        for file_name, file_data in results:
            if file_data:
                return file_data[0]
        return None

    def update_entry(self, entry_id: int, updated_entry: DataEntry):
        self.modified_entries[entry_id] = updated_entry

    def delete_entry(self, entry_id: int):
        self.modified_entries[entry_id] = None

    def create_entry(self, new_entry: DataEntry) -> int:
        new_id = self.cumulative_points
        self.modified_entries[new_id] = new_entry
        self.cumulative_points += 1
        return new_id

file_processor = FileProcessor()
file_processor.initialize_data()
