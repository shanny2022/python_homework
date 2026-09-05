"""Run with python -m unittest -v test_database.py."""
from contextlib import redirect_stdout
import io
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd
import capstone_database as database
import clean_data


class DatabaseTests(unittest.TestCase):
    def test_supplied_data_round_trip_and_rerun(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.db"
            with patch.object(database, "DATABASE", path), redirect_stdout(io.StringIO()):
                database.build_database()
                database.build_database()
            with sqlite3.connect(path) as conn:
                self.assertEqual(conn.execute('SELECT COUNT(*) FROM quotes_raw').fetchone()[0], 12)
                self.assertEqual(conn.execute('SELECT COUNT(*) FROM quotes_clean').fetchone()[0], 12)
                self.assertEqual(conn.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
                rows = conn.execute('SELECT quote,quote_length,word_count FROM quotes_clean').fetchall()
                for quote, length, words in rows:
                    self.assertEqual(length, len(quote))
                    self.assertEqual(words, len(quote.replace('“','').replace('”','').split()))

    def test_cleaning_missing_duplicate_and_malformed_values(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            raw = root / 'raw.csv'
            pd.DataFrame([
                [' Test quote ', ' ', 'a, b', 'wrong', '1.5'],
                ['Test quote', None, 'a, b', '2', 'bad'],
                [' ', 'Nobody', None, None, None],
            ], columns=['quote','author','tags','tag_count','page']).to_csv(raw,index=False)
            with patch.object(clean_data,'RAW_CSV',raw), patch.object(clean_data,'CLEAN_DIR',root), patch.object(clean_data,'CLEAN_CSV',root/'clean.csv'), redirect_stdout(io.StringIO()):
                result = clean_data.clean_quotes()
            self.assertEqual(len(result),1)
            self.assertEqual(result.iloc[0]['author'],'Unknown')
            self.assertEqual(result.iloc[0]['tag_count'],2)
            self.assertTrue(pd.isna(result.iloc[0]['page']))

    def test_failed_import_preserves_existing_database(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'test.db'
            with patch.object(database,'DATABASE',path), redirect_stdout(io.StringIO()):
                database.build_database()
                before = path.read_bytes()
                with patch.object(pd.DataFrame,'to_sql',side_effect=sqlite3.OperationalError('test failure')):
                    with self.assertRaises(sqlite3.OperationalError):
                        database.build_database()
                self.assertEqual(path.read_bytes(),before)
                self.assertEqual(list(Path(folder).glob('*.db')),[path])


if __name__ == '__main__':
    unittest.main()
