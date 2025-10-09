import unittest
import logging
from unittest.mock import patch
from utils.logger import setup_logger

class TestLogger(unittest.TestCase):

    @patch('logging.StreamHandler')
    def test_setup_logger(self, mock_stream_handler):
        logger = setup_logger()
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "bot_trader_ia")
        self.assertEqual(logger.level, logging.INFO)
        mock_stream_handler.assert_called_once()
        self.assertEqual(len(logger.handlers), 1)

if __name__ == '__main__':
    unittest.main()

