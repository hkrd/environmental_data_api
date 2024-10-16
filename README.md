# Air Quality Data API

This API provides access to global annual PM2.5 air pollution levels data.

## Running the API

### Using Docker

1. Build the Docker image:
   ```
   docker build -t air-quality-api .
   ```

2. Run the Docker container:
   ```
   docker run -p 8000:8000 air-quality-api
   ```

3. Access the API at `http://localhost:8000`

### Running Locally

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the API:
   ```
   uvicorn main:app --reload
   ```

3. Access the API at `http://localhost:8000`

## API Endpoints

- `GET /data`: Retrieve all available data.
- `GET /data/{id}`: Fetch a specific data entry by ID.
- `POST /data`: Add a new data entry.
- `PUT /data/{id}`: Update an existing data entry.
- `DELETE /data/{id}`: Delete a data entry.
- `GET /data/filter?year={year}&lat={lat}&long={long}`: Filter the dataset based on year, latitude, and longitude.
- `GET /data/stats`: Provide basic statistics across the dataset.
- `GET /data/region?lat_min={lat_min}&lat_max={lat_max}&long_min={long_min}&long_max={long_max}`: Retrieve data within a bounding box.
- `GET /data/normalize`: Get normalized PM2.5 levels.
- `GET /data/top_polluted?year={year}`: Get top 10 most polluted locations for a given year.

For detailed API documentation, visit `http://localhost:8000/docs` after starting the server.
