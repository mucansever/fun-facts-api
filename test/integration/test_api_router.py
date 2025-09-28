import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from datetime import date

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from main import create_app
from app.domain.model import DailyFunFact


@pytest.mark.integration
class TestFunFactAPIRouter:

    @pytest.fixture
    def client(self):
        app = create_app()
        return TestClient(app)

    @pytest.fixture
    def sample_fun_fact(self):
        return DailyFunFact(
            date=date(2024, 1, 15),
            fact="The human brain contains approximately 86 billion neurons."
        )

    @pytest.fixture
    def sample_fun_facts(self):
        return [
            DailyFunFact(date=date(2024, 1, 15), fact="The human brain contains approximately 86 billion neurons."),
            DailyFunFact(date=date(2024, 1, 14), fact="A group of flamingos is called a 'flamboyance'."),
            DailyFunFact(date=date(2024, 1, 13), fact="Honey never spoils - archaeologists have found edible honey in ancient Egyptian tombs."),
        ]

    @patch('app.domain.service._daily_fun_fact_service_instance')
    def test_get_todays_fun_fact_success(self, mock_service, client, sample_fun_fact):
        # Setup
        mock_service.get_todays_fun_fact = AsyncMock(return_value=sample_fun_fact)

        # Act
        response = client.get("/v1/fun-facts/today")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["date"] == "2024-01-15"
        assert data["fact"] == "The human brain contains approximately 86 billion neurons."

    @patch('app.domain.service._daily_fun_fact_service_instance')
    def test_get_todays_fun_fact_not_found(self, mock_service, client):
        # Setup
        mock_service.get_todays_fun_fact = AsyncMock(return_value=None)

        # Act
        response = client.get("/v1/fun-facts/today")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Fun fact not found"

    @patch('app.domain.service._daily_fun_fact_service_instance')
    def test_get_recent_fun_facts_success(self, mock_service, client, sample_fun_facts):
        # Setup
        mock_service.get_last_n_fun_facts = AsyncMock(return_value=sample_fun_facts)

        # Act
        response = client.get("/v1/fun-facts/recent")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["date"] == "2024-01-15"
        assert data[0]["fact"] == "The human brain contains approximately 86 billion neurons."
        assert data[1]["date"] == "2024-01-14"
        assert data[1]["fact"] == "A group of flamingos is called a 'flamboyance'."

    @patch('app.domain.service._daily_fun_fact_service_instance')
    def test_get_recent_fun_facts_empty(self, mock_service, client):
        # Setup
        mock_service.get_last_n_fun_facts = AsyncMock(return_value=[])

        # Act
        response = client.get("/v1/fun-facts/recent")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data == []

    @patch('app.domain.service._daily_fun_fact_service_instance')
    def test_get_todays_fun_fact_service_exception(self, mock_service, client):
        """Test when service raises an exception."""
        # Setup
        mock_service.get_todays_fun_fact = AsyncMock(side_effect=Exception("Service error"))

        # Act & Assert
        with pytest.raises(Exception, match="Service error"):
            client.get("/v1/fun-facts/today")

    @patch('app.domain.service._daily_fun_fact_service_instance')
    def test_get_recent_fun_facts_service_exception(self, mock_service, client):
        # Setup
        mock_service.get_last_n_fun_facts = AsyncMock(side_effect=Exception("Service error"))

        # Act & Assert
        with pytest.raises(Exception, match="Service error"):
            client.get("/v1/fun-facts/recent")

    @patch('app.domain.service._daily_fun_fact_service_instance')
    def test_api_response_format(self, mock_service, client, sample_fun_fact):
        # Setup
        mock_service.get_todays_fun_fact = AsyncMock(return_value=sample_fun_fact)

        # Act
        response = client.get("/v1/fun-facts/today")

        # Assert
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "date" in data
        assert "fact" in data
        
        # Check data types
        assert isinstance(data["date"], str)
        assert isinstance(data["fact"], str)
        
        # Check date format (ISO format)
        assert data["date"] == "2024-01-15"

    @patch('app.domain.service._daily_fun_fact_service_instance')
    def test_recent_facts_response_format(self, mock_service, client, sample_fun_facts):
        # Setup
        mock_service.get_last_n_fun_facts = AsyncMock(return_value=sample_fun_facts)

        # Act
        response = client.get("/v1/fun-facts/recent")

        # Assert
        assert response.status_code == 200
        data = response.json()
        
        # Check it's a list
        assert isinstance(data, list)
        assert len(data) == 3
        
        # Check each item has required fields
        for item in data:
            assert "date" in item
            assert "fact" in item
            assert isinstance(item["date"], str)
            assert isinstance(item["fact"], str)

