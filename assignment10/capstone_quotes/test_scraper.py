"""Offline checks; no website requests or browser launch."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import scraper


class ScraperTests(unittest.TestCase):
    def test_blank_text_uses_default(self):
        parent = Mock()
        parent.find_element.return_value.text = '  '
        self.assertEqual(scraper.safe_text(parent, '.author', 'Unknown'), 'Unknown')
        parent.find_element.side_effect = NoSuchElementException()
        self.assertEqual(scraper.safe_text(parent, '.author', 'Unknown'), 'Unknown')

    def test_empty_result_preserves_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'quotes_raw.csv'
            path.write_text('existing records')
            with patch.object(scraper, 'RAW_DIR', Path(folder)), patch.object(scraper, 'RAW_CSV', path):
                with self.assertRaises(ValueError):
                    scraper.save_outputs([])
            self.assertEqual(path.read_text(), 'existing records')

    def test_timeout_closes_browser_and_raises(self):
        driver = Mock()
        with patch.object(scraper, 'build_driver', return_value=driver), patch.object(scraper, 'WebDriverWait') as wait:
            wait.return_value.until.side_effect = TimeoutException()
            with self.assertRaisesRegex(RuntimeError, 'page 1'):
                scraper.scrape_quotes()
        driver.quit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
