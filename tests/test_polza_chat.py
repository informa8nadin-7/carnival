"""Тесты для сервиса polza_chat."""

import json
from unittest.mock import patch, MagicMock
import pytest

from src.bot.services.polza_chat import _make_polza_request, ask_polza


class TestPolzaChat:
    """Тесты для функций работы с Polza.ai."""

    @patch("src.bot.services.polza_chat.load_config")
    @patch("src.bot.services.polza_chat.urlopen")
    def test_make_polza_request_success(self, mock_urlopen, mock_load_config):
        """Успешный запрос возвращает текст ответа."""
        # Мокаем конфигурацию
        mock_config = MagicMock()
        mock_config.polza_api_key = "test-key"
        mock_config.polza_model = "gpt-3.5-turbo"
        mock_config.polza_base_url = "https://api.polza.ai/v1"
        mock_load_config.return_value = mock_config

        # Мокаем ответ HTTP
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "choices": [
                {
                    "message": {
                        "content": "Привет, я ИИ!"
                    }
                }
            ]
        }).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        messages = [{"role": "user", "content": "Привет"}]
        result = _make_polza_request(messages)

        assert result == "Привет, я ИИ!"
        # Проверяем, что запрос был отправлен с правильными параметрами
        mock_urlopen.assert_called_once()
        call_args = mock_urlopen.call_args[0][0]
        assert call_args.full_url == "https://api.polza.ai/v1/chat/completions"
        assert call_args.method == "POST"
        assert json.loads(call_args.data) == {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7,
        }
        assert call_args.headers["Authorization"] == "Bearer test-key"

    @patch("src.bot.services.polza_chat.load_config")
    def test_make_polza_request_no_api_key(self, mock_load_config):
        """Если API-ключ отсутствует, возвращается демо-ответ."""
        mock_config = MagicMock()
        mock_config.polza_api_key = ""
        mock_load_config.return_value = mock_config

        messages = [{"role": "user", "content": "Привет"}]
        result = _make_polza_request(messages)

        assert "демо-ответ" in result
        assert "API-ключ Polza.ai не задан" in result

    @patch("src.bot.services.polza_chat.load_config")
    @patch("src.bot.services.polza_chat.urlopen")
    def test_make_polza_request_http_error(self, mock_urlopen, mock_load_config):
        """Ошибка HTTP вызывает RuntimeError."""
        mock_config = MagicMock()
        mock_config.polza_api_key = "test-key"
        mock_config.polza_model = "gpt-3.5-turbo"
        mock_config.polza_base_url = "https://api.polza.ai/v1"
        mock_load_config.return_value = mock_config

        mock_urlopen.side_effect = Exception("HTTP Error")

        messages = [{"role": "user", "content": "Привет"}]
        with pytest.raises(RuntimeError):
            _make_polza_request(messages)

    @patch("src.bot.services.polza_chat.load_config")
    @patch("src.bot.services.polza_chat.urlopen")
    def test_make_polza_request_invalid_response(self, mock_urlopen, mock_load_config):
        """Некорректный JSON в ответе вызывает RuntimeError."""
        mock_config = MagicMock()
        mock_config.polza_api_key = "test-key"
        mock_config.polza_model = "gpt-3.5-turbo"
        mock_config.polza_base_url = "https://api.polza.ai/v1"
        mock_load_config.return_value = mock_config

        mock_response = MagicMock()
        mock_response.read.return_value = b"invalid json"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        messages = [{"role": "user", "content": "Привет"}]
        with pytest.raises(RuntimeError):
            _make_polza_request(messages)

    @patch("src.bot.services.polza_chat._make_polza_request")
    def test_ask_polza_async(self, mock_make_request):
        """ask_polza вызывает _make_polza_request через asyncio.to_thread."""
        mock_make_request.return_value = "Ответ"
        import asyncio

        messages = [{"role": "user", "content": "Тест"}]
        result = asyncio.run(ask_polza(messages))

        assert result == "Ответ"
        mock_make_request.assert_called_once_with(messages)