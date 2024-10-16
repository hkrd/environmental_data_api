# Air Quality Data API

This API provides access to global annual PM2.5 air pollution levels data.

## Building and Running the Docker Container

1. Build the Docker image:
   ```
   docker build -t air-quality-api .
   ```

2. Run the Docker container:
   ```
   docker run -p 8000:8000 air-quality-api
   ```

3. Access the API:
   - `http://localhost:8000`

## API Endpoints

- `GET /data`: Retrieve all available data (paginated).
- `GET /data/{id}`: Fetch a specific data entry by ID.
- `POST /data`: Add a new data entry.
- `PUT /data/{id}`: Update an existing data entry.
- `DELETE /data/{id}`: Delete a data entry.
- `GET /data/filter?year={year}&lat={lat}&long={long}`: Filter the dataset based on year, latitude, and longitude.
- `GET /data/stats`: Provide basic statistics across the dataset.

## Data Source

The API uses PM2.5 data from the Socioeconomic Data and Applications Center (SEDAC). The data is automatically downloaded and processed when the container starts.

## API Documentation

For detailed API documentation, visit `http://<host>:8000/docs` after starting the server.

## Development

To set up the development environment:

1. Install Poetry: `pip install poetry`
2. Install dependencies: `poetry install`
3. Run the development server: `poetry run uvicorn data_transformer.main:app --reload`

## Notes

- The first run may take some time as it downloads and processes the data files.
- You can provide more google drive links to download more data files which will be added to the overall results.
- Ensure you have sufficiet memory to load these files. On my machine (16GB RAM), I can load 2 files.
- The CRUD endpoints only copy entries from the loaded data and perform operations on them. No data is inserted in files.
