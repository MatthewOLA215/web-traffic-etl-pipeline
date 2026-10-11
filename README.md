# Web Traffic ETL Pipeline

A batch ETL pipeline that generates, parses, cleans, and loads web server logs into MySQL, with a Power BI dashboard for web traffic analytics.

Final year project, Department of Computer Science, Caleb University, Lagos (2026).

## What it does

The pipeline runs in four stages:

1. **Generate**: creates 75,000 synthetic Apache-style access log records using Faker.
2. **Extract**: reads the raw log file line by line.
3. **Transform**: parses each line with a regular expression, converts timestamps, and adds analytics fields.
4. **Load**: inserts the records into a MySQL table in batches of 50,000 rows and exports a CSV copy.

Each run is logged to `logs/pipeline.log`. Windows Task Scheduler can start the pipeline through `run_pipeline.bat`.

## Results

| Metric | Value |
|---|---|
| Records processed per run | 75,000 |
| Run time (generate, extract, transform, load, export) | about 132 seconds |
| Load batch size | 50,000 rows |

## Tech stack

| Area | Tool |
|---|---|
| Language | Python |
| Data processing | pandas |
| Test data | Faker |
| Database | MySQL |
| Database connection | mysql-connector-python |
| Configuration | python-dotenv |
| Automation | Windows Task Scheduler and a batch script |
| Dashboard | Power BI and DAX |

## Project structure

```
web-traffic-etl/
├── config/
│   └── current_year.txt
├── data/
│   ├── raw/access.log
│   └── processed/web_traffic_processed.csv
├── logs/
│   └── pipeline.log
├── notebooks/
│   └── eda.ipynb
├── sql/
│   └── create_tables.sql
├── src/
│   ├── database.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── log_generator.py
│   └── logger.py
├── tests/
├── main.py
├── requirements.txt
└── run_pipeline.bat
```

## Data

The pipeline uses synthetic logs, so the repository holds no real user data. Each record follows this format:

```
IP - - [timestamp] "METHOD URL HTTP/1.1" status bytes "referrer" "user_agent" response_time
```

Each run generates logs for one calendar year. The year starts at 2015 and moves forward by one after every run. The current year is stored in `config/current_year.txt`.

### Database table

All records go into one table, `web_logs`, in the database `web_traffic_db`.

| Column | Source |
|---|---|
| record_id | Auto-incrementing primary key |
| ip_address, access_time, http_method, url, protocol | Parsed from the log line |
| status_code, bytes_sent, referrer, user_agent, response_time | Parsed from the log line |
| request_date, request_hour, day_of_week, month | Derived from access_time |
| is_error | Derived: "Error" when status_code is 400 or higher, otherwise "Success" |
| browser | Derived from user_agent (Edge, Opera, Firefox, Chrome, Safari, Other) |
| device_type | Derived from user_agent (Mobile or Desktop) |

## Setup

You need Python 3 and a running MySQL server.

1. Clone the repository:

   ```
   git clone <your-repository-url>
   cd web-traffic-etl
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create the database and table:

   ```sql
   CREATE DATABASE web_traffic_db;
   ```

   Then run `sql/create_tables.sql` in MySQL Workbench or the MySQL command line.

5. Create a `.env` file in the project root with your database details:

   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=web_traffic_db
   ```

   Never commit this file. It is listed in `.gitignore`.

## Usage

Run the full pipeline:

```
python main.py
```

The terminal shows the number of rows inserted and the total run time. The processed data is also saved to `data/processed/web_traffic_processed.csv`.

### Schedule the pipeline

`run_pipeline.bat` activates the virtual environment and runs `main.py`.

1. Open the file and change the folder path on the `cd` line to your project location.
2. Open Windows Task Scheduler and create a new basic task.
3. Set the trigger you want, such as daily.
4. Set the action to start a program and select `run_pipeline.bat`.

## Tests

The `tests` folder holds one test file for each module.

```
python -m unittest discover tests
```

## Dashboard

The Power BI dashboard connects to the `web_logs` table. It has three pages.

| Page | Content |
|---|---|
| Executive Dashboard | Total requests, unique hosts, errors, bytes transferred, daily traffic trend, status code distribution |
| Web Traffic Analytics | Traffic by hour and month, browser and device distribution, top requested URLs |
| Performance and Error | Error rate trend, HTTP error breakdown, response size distribution |

Key DAX measures:

```
Total Requests = COUNT(web_logs[record_id])

Error Rate =
DIVIDE(
    CALCULATE(COUNT(web_logs[record_id]), web_logs[is_error] = "Error"),
    [Total Requests]
)

Mobile Traffic % =
DIVIDE(
    CALCULATE(COUNT(web_logs[record_id]), web_logs[device_type] = "Mobile"),
    [Total Requests]
)
```

### Screenshots

![Executive Dashboard](docs/screenshots/executive-dashboard.png)

![Web Traffic Analytics](docs/screenshots/web-traffic-analytics.png)

![Performance and Error](docs/screenshots/performance-and-error.png)

## Author

Odunaiya Matthew Olarenwaju
B.Sc. Computer Science, Caleb University, Lagos
