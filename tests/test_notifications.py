import unittest
from unittest.mock import patch, MagicMock
from utils.notifications import Notifier
from config.settings import Settings

class TestNotifications(unittest.TestCase):

    def setUp(self):
        # Mock settings para evitar dependência de variáveis de ambiente reais
        self.mock_settings = MagicMock(spec=Settings)
        self.mock_settings.TELEGRAM_BOT_TOKEN = "test_token"
        self.mock_settings.TELEGRAM_CHAT_ID = "test_chat_id"

        # Patch config.settings.settings para usar nosso mock
        self.patcher = patch("utils.notifications.settings", new=self.mock_settings)
        self.patcher.start()
        self.notifier = Notifier()

    def tearDown(self):
        self.patcher.stop()

    @patch("requests.post")
    def test_send_message_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        message = "Test message"
        self.notifier.send_message(message)

        mock_post.assert_called_once_with(
            f"https://api.telegram.org/bot{self.mock_settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            data={
                "chat_id": self.mock_settings.TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
        )

    @patch("requests.post")
    def test_send_message_no_token_or_chat_id(self, mock_post):
        self.mock_settings.TELEGRAM_BOT_TOKEN = None
        self.mock_settings.TELEGRAM_CHAT_ID = None

        message = "Test message"
        self.notifier.send_message(message)

        mock_post.assert_not_called()

    @patch("requests.post")
    def test_send_message_failure(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        message = "Test message"
        self.notifier.send_message(message)

        mock_post.assert_called_once()

if __name__ == '__main__':
    unittest.main()

