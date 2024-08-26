# Claimspotting Django API

This Django project provides a REST API for the Claimspotting tool, part of the Public Interest AI research group at the Humboldt Institute for Internet and Society (HIIG). The API supports querying and analysing data collected from Telegram channels known for spreading misinformation.

## Project Structure

The project consists of the following key components:

- **list_api**: Provides the data for the table, including filters for date range, Telegram channels, and other criteria.
```bash
curl -X GET "http://localhost:8000/claimspotting/list_api/?start_date=2024-08-23&end_date=2024-08-24&factual=true&pagination=false&remove_russian=true"
```
- **search_api**: Enables custom searches within the database using a query text.
```bash
curl -X GET "http://localhost:8000/claimspotting/search_api/?query_text=text_you_want_to_find"
```
- **stats_api**: Returns statistics and trends based on the collected data.
```bash
curl -X GET "http://localhost:8000/claimspotting/stats_api/?start_day=2024-08-01&end_day=2024-08-31"
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo-url/claimspotting-django-api.git
cd claimspotting-django-api
```
### 2. Create and start venv and install requirements

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create and Configure .env File

```bash
MONGO_DB_URI=your_mongo_db_uri
MONGO_DB_NAME=your_mongo_db_name
MONGO_VECTOR_DB_NAME=your_mongo_vector_db_name
MONGO_DB_STATS_NAME=your_mongo_db_stats_name
RUNPOD_API_KEY=your_runpod_api_key
RUNPOD_ENDPOINT=your_runpod_endpoint
SECRET_KEY=your_django_secret_key
```
### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run the Django Development Server

```bash
python manage.py runserver
```