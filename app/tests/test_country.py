import pytest
from fastapi.testclient import TestClient
from app.routers.country import router
from unittest.mock import patch

class MockCountryScraper:
    def scrape_countries(self, country_name=None):
        if country_name:
            return [{"name": country_name, "url": f"http://example.com/{country_name}"}]
        return [{"name": "Italy", "url": "http://example.com/italy"}, {"name": "France", "url": "http://example.com/france"}]

client = TestClient(router)

@pytest.fixture
def mock_country_scraper():
    with patch("app.routers.country.CountryScraper", MockCountryScraper):
        yield

def test_get_countries(mock_country_scraper):
    """
    Test the /countries endpoint for successful response.
    """
    response = client.get("/")
    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert "countries" in data, "Response should include a 'countries' key"
    assert len(data["countries"]) > 0, "Expected non-empty list of countries"

def test_get_country_by_name(mock_country_scraper):
    """
    Test the /countries/search/{country_name} endpoint for successful response.
    """
    country_name = "Italy"
    response = client.get(f"/search/{country_name}")
    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert "countries" in data, "Response should include a 'countries' key"
    assert len(data["countries"]) == 1, "Expected one country in the response"
    assert data["countries"][0]["name"] == country_name, f"Expected country name to be '{country_name}'"

def test_get_country_by_name_not_found(mock_country_scraper):
    """
    Test the /countries/search/{country_name} endpoint for a country that does not exist.
    """
    country_name = "Unknown"
    with patch.object(MockCountryScraper, "scrape_countries", return_value=[]):
        response = client.get(f"/search/{country_name}")
        assert response.status_code == 200, "Expected status code 200"
        data = response.json()
        assert "countries" in data, "Response should include a 'countries' key"
        assert len(data["countries"]) == 0, "Expected no countries in the response"
