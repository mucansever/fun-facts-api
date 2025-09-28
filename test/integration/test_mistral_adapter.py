import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.adapter.mistral.mistral_adapter import MistralAdapter


@pytest.mark.integration
class TestMistralAdapter:

    @pytest.fixture
    def mistral_adapter(self):
        return MistralAdapter("test-api-key")

    @pytest.mark.asyncio
    async def test_chat(self, mistral_adapter):
        # Setup
        test_prompt = "Tell me a fun fact about space"
        expected_response = "The Sun contains 99.86% of the Solar System's mass."

        mock_choice = MagicMock()
        mock_choice.message.content = expected_response
        
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        with patch.object(mistral_adapter.client.chat, 'complete_async', new_callable=AsyncMock) as mock_complete:
            mock_complete.return_value = mock_response

            # Act
            result = await mistral_adapter.chat(test_prompt)

            # Assert
            assert result == expected_response
            mock_complete.assert_called_once_with(
                model="mistral-tiny",
                messages=[{"role": "user", "content": test_prompt}],
                temperature=1.0,
                max_tokens=4096
            )

    @pytest.mark.asyncio
    async def test_chat_with_empty_response(self, mistral_adapter):
        # Setup
        test_prompt = "Tell me a fun fact"
        expected_response = ""

        mock_choice = MagicMock()
        mock_choice.message.content = None 
        
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        with patch.object(mistral_adapter.client.chat, 'complete_async', new_callable=AsyncMock) as mock_complete:
            mock_complete.return_value = mock_response

            # Act
            result = await mistral_adapter.chat(test_prompt)

            # Assert
            assert result == "None" 

    @pytest.mark.asyncio
    async def test_chat_with_multiple_choices(self, mistral_adapter):
        # Setup
        test_prompt = "Tell me a fun fact"
        expected_response = "Honey never spoils - archaeologists have found edible honey in ancient Egyptian tombs."

        mock_choice1 = MagicMock()
        mock_choice1.message.content = expected_response
        
        mock_choice2 = MagicMock()
        mock_choice2.message.content = "Another fun fact"
        
        mock_response = MagicMock()
        mock_response.choices = [mock_choice1, mock_choice2]

        with patch.object(mistral_adapter.client.chat, 'complete_async', new_callable=AsyncMock) as mock_complete:
            mock_complete.return_value = mock_response

            # Act
            result = await mistral_adapter.chat(test_prompt)

            # Assert
            assert result == expected_response 
