
# Tech Challenge: Build a Basic API for Air Quality Data

## Objective:
The goal of this challenge is to evaluate your ability to create a RESTful API that interacts with air quality data and handles basic filtering and analytics using clean coding practices. You will work with a dataset focused on global annual PM2.5 air pollution levels, representing critical environmental data.

## Dataset Overview:
You will use the **Global Annual PM2.5 Grids** dataset provided by SEDAC. This dataset contains information on PM2.5 (particulate matter) air pollution levels collected from various satellite and observation sources.  
Dataset can be downloded here:
- https://drive.google.com/file/d/1WeEhLps3He6RPutYr82AwZkqWG7LJuIS/view?usp=sharing
- https://drive.google.com/file/d/1W2E7nPTezw4x6vd77V1ok85kuOiCZVMB/view?usp=sharing

The dataset includes fields such as:
- **Latitude**: The latitude of the data point.
- **Longitude**: The longitude of the data point.
- **Year**: The year the data was collected.
- **PM2.5 Level**: The concentration of PM2.5 in µg/m³ (micrograms per cubic meter).

You will create a RESTful API to allow users to query, filter, and perform basic analytics on this dataset.

## Data Formats: netCDF vs GeoTIFF
- **netCDF**: With netCDF, you will obtain a multidimensional array of information, which is ideal when working with complex scientific data and multiple variables. netCDF is a flexible format that includes detailed metadata, making it useful for handling large datasets with rich metadata.
- **GeoTIFF**: On the other hand, GeoTIFF provides access to georeferenced metadata, which is more suited for applications where the data will be used in GIS platforms for map visualization or rasterized analysis. If you're working with spatial imagery and need integration with GIS tools, GeoTIFF is preferable.

Depending on your API's functionality, you might opt for either format to handle air quality data efficiently.

## Data Preparation:
To assist with the dataset you could convert netCDF/GeoTIFF file to a format suitable for your API.

## Task Overview:
You are required to build a RESTful API that:
1. Loads the dataset into memory for querying and analytics.
2. Exposes endpoints that allow basic interaction with the data, including CRUD operations and basic statistics.
3. Containerizes the application using Docker.

## Requirements:
1. **Programming Language**: Choose between Python (Flask/FastAPI) or TypeScript (Express.js).
2. **Database**: Use in-memory storage (e.g., Pandas for Python or a simple in-memory array/object for Node.js).
3. **API Endpoints**:
   - `GET /data`: Retrieve all available data.
   - `GET /data/:id`: Fetch a specific data entry by ID.
   - `POST /data`: Add a new data entry (validate required fields).
   - `PUT /data/:id`: Update an existing data entry.
   - `DELETE /data/:id`: Delete a data entry.
   - `GET /data/filter?year=:year&lat=:lat&long=:long`: Filter the dataset based on year, latitude, and longitude.
   - `GET /data/stats`: Provide basic statistics (count, average PM2.5, min, max) across the dataset.
4. **Docker**: Create a `Dockerfile` to containerize the API.

## Dataset Fields:
- **Year**: Year the PM2.5 levels were recorded.
- **Latitude**: The geographic latitude where data was recorded.
- **Longitude**: The geographic longitude where data was recorded.
- **PM2.5 Level**: The concentration of PM2.5 in µg/m³.

## Simplified Analytics:
- **Basic Statistics**: The API should provide basic aggregate statistics like count, mean, min, and max PM2.5 levels across the entire dataset.
- **Filtering**: Users should be able to filter data by year, latitude, and longitude.

## Expected Deliverables:
1. A working RESTful API with the defined endpoints.
2. A Dockerfile that allows the API to be containerized.
3. Instructions on how to run the API (via Docker or locally).
4. Bonus: Include basic tests for your API functionality.

## Evaluation Criteria:
- **Code Quality**: Clean, maintainable, and modular code.
- **API Design**: Well-designed RESTful endpoints and adherence to best practices.
- **Error Handling**: Robust error handling and input validation.
- **Performance****: Efficient querying and filtering of data.
- **Best Practices**: Clean code, test coverage, and version control usage (e.g., Git).
- **Bonus**: Use of CI/CD practices, unit testing, or extra analytics.

## Time Limit:
- **90 minutes** to complete the task.

## Submission:
- Submit a GitHub repository with your solution.
- Include a `README.md` with instructions on how to run your API (locally or with Docker).

Good luck!
