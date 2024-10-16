from pydantic import BaseModel


class DataEntry(BaseModel):
    Year: int
    Latitude: float
    Longitude: float
    PM2_5_Level: float


class DataResponse(BaseModel):
    page: int
    page_size: int
    total_items: int
    data_from: list[str]
    files_info: list[dict]
    data: list[DataEntry]


class StatsResponse(BaseModel):
    count: int
    average_pm2_5: float
    min_pm2_5: float
    max_pm2_5: float
    years_available: list[int]


class FilterDataResponse(BaseModel):
    data: list[DataEntry]
    page: int
    page_size: int
    total_items: int
