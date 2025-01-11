# LiveScore API Project

## Overview
This project is a backend FastAPI application designed to demonstrate how to scrape data from the football section of the website [livescore.in](https://www.livescore.in/football/). **The project is strictly for instructional and educational purposes only**. It is not intended for effective web scraping or storing live score data.

### Important Legal Notice
Scraping content from websites without permission can violate their terms of service and legal policies. This project:
- **Implements rate limiting** to reduce requests.
- **Simulates human behavior** through a wait mechanism to avoid overloading the target site.
- Does not store any scraped data.

The primary goal is to provide developers with an educational example of how to structure a web scraping backend with FastAPI.

---

## Project Structure
```plaintext
livescore-api
├── app
│   ├── routers
│   │   ├── archive.py
│   │   ├── country.py
│   │   ├── league.py
│   │   ├── match.py
│   ├── services
│       ├── models
│       │   ├── archive_schemas.py
│       │   ├── country_schemas.py
│       │   ├── league_schemas.py
│       │   ├── match_schemas.py
│       │   ├── utils.py
│       ├── scraper
│           ├── archive_scraper.py
│           ├── country_scraper.py
│           ├── leagues_scraper.py
│           ├── match_scraper.py
│           ├── scraper.py
│           ├── utils.py
├── tests
│   ├── main.py
├── logger
├── .env
├── .gitignore
├── README.md
├── requirements.txt
```

### Key Directories and Files
- **`app/routers`**: Contains API endpoints for different scraping functionalities.
- **`app/services/models`**: Contains schemas for validation and utility functions for data processing.
- **`app/services/scraper`**: Core logic for scraping the livescore football page and individual match data.
- **`.env`**: Environment variables for configuration.
- **`logger`**: Custom logging configurations for monitoring application behavior.
- **`tests`**: Contains test cases to validate the scraping logic and API functionality.

---

## Environment Variables
The project uses an `.env` file to manage configuration. Below are the available variables:

```plaintext
DEBUG=False
URL_LIVESPORT=https://www.livescore.in/football/
URL_LIVESPORT_MATCH=https://www.livescore.in/match/{MATCH_ID}/#/match-summary/match-statistics/0
TIMEOUT=30
LIMIT=10
RATE_LIMITING_FREQUENCY=2/1minute
RATE_LIMITING_ENABLE=True
SIMULATE_WAITING_HUMAN_BEING=10
```

### Explanation of Variables:
- **`DEBUG`**: Toggle debug mode (default: `False`).
- **`URL_LIVESPORT`**: Base URL for scraping football scores.
- **`URL_LIVESPORT_MATCH`**: URL template for scraping match-specific statistics.
- **`TIMEOUT`**: Timeout in seconds for each request.
- **`LIMIT`**: Maximum number of items to scrape in a single run.
- **`RATE_LIMITING_FREQUENCY`**: Limits the number of requests per minute (e.g., `2/1minute` allows 2 requests per minute).
- **`RATE_LIMITING_ENABLE`**: Enables or disables rate limiting.
- **`SIMULATE_WAITING_HUMAN_BEING`**: Simulates a human delay (in seconds) to mimic user behavior.

---

## Installation
### Prerequisites
- Python 3.9+
- Virtual Environment (optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd livescore-api
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the environment variables:
   Create a `.env` file in the root directory and populate it with the variables listed above.

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
   
---

## Running with Docker
This project can also be built and run using Docker.

### Steps to Execute with Docker
1. Build the Docker image:
   ```bash
   docker build -t livescore-api .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 livescore-api
   ```

The application will be available at `http://localhost:8000`.

---

## Features
### API Endpoints
1. **Archive Data** (`/archive`): Retrieve historical data for football matches.
2. **Country Information** (`/country`): Scrape data related to football leagues by country.
3. **League Data** (`/league`): Fetch details of specific leagues.
4. **Match Data** (`/match`): Scrape and return statistics of a specific match using the `MATCH_ID`.

---

## Legal and Ethical Use
This project is designed for **educational purposes only**. By running or using this project, you agree:
- Not to use it for unauthorized or illegal scraping.
- To comply with all applicable laws and the target website's terms of service.

**Rate limiting and human-like delay mechanisms are implemented** to minimize server impact and simulate realistic behavior. This project does not promote or endorse unethical practices.


---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Disclaimer
This project is for educational purposes only. Unauthorized scraping may result in legal action. Use responsibly and at your own risk.