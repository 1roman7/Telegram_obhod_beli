import pytest
from unittest.mock import patch, MagicMock
import urllib.request
from RECNO_NETWORK.scripts.vless_manager import download_subscriptions

def test_download_subscriptions_success():
    """Test that download_subscriptions correctly parses vless configs from a successful response."""
    mock_urls = ["http://example.com/vless.txt"]
    with patch("RECNO_NETWORK.scripts.vless_manager.SUBSCRIPTION_URLS", mock_urls):
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b"vless://config1\nnot_vless\nvless://config2"
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response

            configs = download_subscriptions()

            assert "vless://config1" in configs
            assert "vless://config2" in configs
            assert "not_vless" not in configs
            assert len(configs) == 2

def test_download_subscriptions_error_path():
    """
    Test the error path in download_subscriptions.
    Verifies that if one URL fails, the function catches the exception and continues to others.
    """
    mock_urls = ["http://fail.com", "http://success.com"]

    with patch("RECNO_NETWORK.scripts.vless_manager.SUBSCRIPTION_URLS", mock_urls):
        with patch("urllib.request.urlopen") as mock_urlopen:
            # Mock success response
            mock_success_response = MagicMock()
            mock_success_response.read.return_value = b"vless://success_config"
            mock_success_response.__enter__.return_value = mock_success_response

            def side_effect(req, timeout=None):
                url = req.get_full_url() if hasattr(req, 'get_full_url') else req
                if "fail.com" in url:
                    raise Exception("Network error")
                return mock_success_response

            mock_urlopen.side_effect = side_effect

            # The function should not raise an exception even if one download fails
            configs = download_subscriptions()

            assert "vless://success_config" in configs
            assert len(configs) == 1
