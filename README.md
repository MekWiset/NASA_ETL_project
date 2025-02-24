# NASA Data ETL Project

This project involves retrieving data from the NASA API, transforming it, and loading it to various destinations using Apache Airflow. The project ensures efficient data processing and storage.

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Instructions](#instructions)
- [Project Structure](#project-structure)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The main goal of this project is to retrieve data from the NASA API, perform necessary transformations, and load the data to various destinations. The ETL (Extract, Transform, Load) process is orchestrated using Apache Airflow to ensure smooth and efficient data handling.

## Technologies Used

- **Apache Airflow**: Orchestrates the ETL process.
- **Python**: For scripting and data transformation.
- **Pandas**: For data manipulation and transformation.
- **Docker Compose**: To manage the Airflow and PostgreSQL services.
- **NASA API**: Source of the data.

## Setup and Installation

### Prerequisites

Ensure you have the following installed on your system:

- Docker
- Docker Compose

### Steps

1. **Clone the repository**
    ```bash
    git clone https://github.com/MekWiset/NASA_ETL_project.git
    cd NASA_ETL_project
    ```

2. **Create an `airflow.env` file from the example and configure your environment variables**
    ```bash
    cp airflow.env.example airflow.env
    ```

3. **Edit the `airflow.env` file and fill in the necessary values**
    ```bash
    nano airflow.env
    ```

4. **Create an `.env` file from the example and configure your sensitive information**
    ```bash
    cp env.example .env
    nano .env
    ```

6. **Build and start the services using Docker Compose**
    ```bash
    docker-compose up -d
    ```

7. **Run the `nasa_events` pipeline**
    ```bash
    airflow trigger_dag etl_reddit_pipeline
    ```

## Usage

To run the ETL pipeline with Airflow UI, follow these steps:

1. Access the Airflow UI at `http://localhost:8080` and trigger the DAG for the ETL process.
2. Monitor the DAG execution and check logs for any issues.
3. Verify the transformed data in the output directory or the specified destination.

## Instructions

1. **Extract Data**:
   - Install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Set up your NASA API credentials in the environment variables or configuration files.
   - The data extraction is handled by the `extract_from_api.py` script located in the `plugins/extract` directory. The script retrieves data from the NASA API and stores it in the `datasets/nasa_events.csv` file.

2. **Transform Data**:
   - Data transformation is performed using the `transform_events.py` and `filter_wildfires.py` scripts in the `plugins/transform` directory.
   - `transform_events.py` processes the raw data and saves the transformed data to `output/transformed_nasa_events.csv`.
   - `filter_wildfires.py` filters wildfire events and saves the results to `output/wildfire_events.csv`.

3. **Load Data**:
   - The `export.py` script in the `plugins/load` directory handles data loading.
   - It exports the transformed data to various destinations as specified.

4. **Run the DAG**:
   - Ensure the DAG defined in `dags/my_dag.py` is scheduled and triggered as required:
     ```bash
     airflow trigger_dag etl_nasa_pipeline
     ```

## Project Structure

- `Dockerfile`: Dockerfile for the project setup.
- `README.md`: Project documentation.
- `airflow.env.example`: Template for Airflow environment variables.
- `env.example`: Template for sensitive environment variables.
- `dags/`: Directory containing DAGs for Airflow.
  - `my_dag.py`: Main DAG for the ETL process.
- `datasets/`: Directory for storing dataset files.
  - `nasa_events.csv`: extracted data file.
- `docker-compose.yaml`: Docker Compose configuration file.
- `output/`: Directory for storing output files.
- `plugins/`: Directory for custom plugins.
  - `extract/`: Directory for data extraction plugins.
  - `load/`: Directory for data loading plugins.
  - `transform/`: Directory for data transformation plugins.
- `requirements.txt`: Python dependencies file.

## Features

- **Data Extraction**: Retrieves data from the NASA API.
- **Data Transformation**: Processes and transforms the data using Pandas.
- **Data Loading**: Exports transformed data to various destinations.
- **Incremental Data Updates**: Efficiently handles newly added data.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

Please ensure your code follows the project's coding standards and includes relevant tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.