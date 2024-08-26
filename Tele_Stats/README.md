# TeleStats

TeleStats is a Python project designed to collect and process statistics from a MongoDB database based on Telegram channel data. This project allows users update the statistics database of the Claimspotting project, which can then be accessed via the API.

## Features

- Connects to a MongoDB database and retrieves documents based on a specified date range.
- Aggregates statistics such as topic and narrative counts from Telegram channel data.
- Uploads aggregated statistics back to the MongoDB database.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/SamiNenno/Claimspotting/Tele_Stats.git
    cd Tele_Stats
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Update the `config.json` file in the project directory with the following structure:
    ```json
    {
        "remote_mongo_dp_uri": "claimspotting_mongodb_uri",
        "mongo_db_name": "claimspotting_db_name",
        "mongo_db_stats_name": "claimspotting_stats_db_name"
    }
    ```


## Usage

To run the project and process statistics, execute the script with the following command:

```bash
python TeleStats.py --days_in_the_past N
