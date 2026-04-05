# Player Trend Analyzer

Player Trend Analyzer is a Python web app that pulls NBA player game logs from NBA.com data through [`nba_api`](https://nba-api-sbang.readthedocs.io/) and turns them into a quick trend report.

## Problem it solves

Sports fans often have to manually dig through box scores to answer simple questions:

- Is this player scoring above or below their usual level lately?
- Are they better at home or away?
- Are rebounds or assists trending up?

This tool automates that comparison and turns raw game logs into a readable summary.

## What it demonstrates

- Python
- API/data fetching with `nba_api`
- Data analysis with `pandas`
- Trend calculations
- Flask web app structure

## Version 1 features

- Search for a player by name
- Pull recent regular-season game logs
- Calculate:
  - season average
  - last 5 average
  - last 10 average
  - home/away splits
- Show a trend summary for points, rebounds, and assists
- Render a browser dashboard for summary stats and recent games

## Project structure

- `app.py` - Flask app entry point
- `cli.py` - optional terminal version
- `api_client.py` - player search and game-log requests
- `analysis.py` - trend calculations and summary text
- `templates/index.html` - browser UI
- `static/styles.css` - styling for the dashboard
- `requirements.txt` - dependencies

## Setup

1. Install Python 3.10+.
2. Create and activate a virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the web app:

```bash
python app.py
```

Then open:

```bash
http://127.0.0.1:5000
```

Optional terminal version:

```bash
python cli.py --player "Jayson Tatum" --season 2024-25
```

## Data source

This project uses `nba_api`, an API client package for NBA.com data.

Reference docs:

- [nba_api overview](https://nba-api-sbang.readthedocs.io/)
- [nba_api table of contents](https://nba-api-sbang.readthedocs.io/en/latest/table_of_contents/)

## Good next upgrades

- Add opponent splits
- Export trend reports to CSV
- Add charts for rolling averages
- Add a player autocomplete search
