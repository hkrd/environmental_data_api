from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from data_transformer.models import DataResponse, FilterDataResponse, StatsResponse, DataEntry
from data_transformer.data_processor import file_processor


router = APIRouter()


@router.get("/data")
def get_all_data(page: int = Query(1, ge=1), page_size: int = Query(100, le=1000)):
    start = (page - 1) * page_size
    end = start + page_size
    result = file_processor.get_data_generator(start, end)

    flattened_result = []
    files_used = []
    for file_name, file_data in result:
        flattened_result.extend(file_data)
        if file_name not in files_used:
            files_used.append(file_name)
    
    flattened_result = flattened_result[:page_size]
    
    return DataResponse(
        page=page,
        page_size=page_size,
        total_items=file_processor.get_total_points(),
        data_from=files_used,
        files_info=file_processor.file_info,
        data=flattened_result
    )


@router.get("/data/stats")
def get_stats(year: Optional[int] = None):
    return file_processor.get_stats(year)


@router.get("/data/filter")
def filter_data(
    year: Optional[int] = None,
    lat: Optional[float] = None,
    long: Optional[float] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(100, le=1000)
):
    start = (page - 1) * page_size
    end = start + page_size

    result = file_processor.get_data_generator(start, end, year=year, lat=lat, long=long)

    flattened_result = [item for _, file_data in result for item in file_data]

    total_items = file_processor.get_total_points(year=year, lat=lat, long=long)

    return FilterDataResponse(
        data=flattened_result,
        page=page,
        page_size=page_size,
        total_items=total_items
    )


@router.get("/data/{entry_id}")
def get_entry(entry_id: int):
    entry = file_processor.get_entry_by_id(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.post("/data")
def create_entry(entry: DataEntry):
    new_id = file_processor.create_entry(entry)
    return {"id": new_id, "entry": entry}


@router.put("/data/{entry_id}")
def update_entry(entry_id: int, updated_entry: DataEntry):
    existing_entry = file_processor.get_entry_by_id(entry_id)
    if existing_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    file_processor.update_entry(entry_id, updated_entry)
    return {"message": "Entry updated successfully"}


@router.delete("/data/{entry_id}")
def delete_entry(entry_id: int):
    existing_entry = file_processor.get_entry_by_id(entry_id)
    if existing_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    file_processor.delete_entry(entry_id)
    return {"message": "Entry deleted successfully"}
