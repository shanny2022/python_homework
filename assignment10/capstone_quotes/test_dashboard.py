"""Verify database-backed dashboard filters with Streamlit's test runner."""
from pathlib import Path
import unittest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).with_name('app.py')


class DashboardTests(unittest.TestCase):
    def test_filters_update_metrics_and_charts(self):
        app = AppTest.from_file(str(APP)).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, '12')
        self.assertEqual(len(app.get('plotly_chart')), 3)
        app.multiselect[0].set_value(['Albert Einstein']).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, '3')
        self.assertEqual(len(app.get('plotly_chart')), 3)
        app.selectbox[0].set_value('change').run()
        self.assertEqual(app.metric[0].value, '1')
        self.assertEqual(len(app.dataframe[0].value), 1)
        app.multiselect[0].set_value([]).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, '0')
        self.assertEqual(len(app.get('plotly_chart')), 0)
        self.assertIn('No quotes match', app.info[0].value)

    def test_word_count_filter(self):
        app = AppTest.from_file(str(APP)).run(timeout=30)
        app.slider[0].set_value((7, 10)).run()
        self.assertFalse(app.exception)
        values = app.dataframe[0].value.word_count
        self.assertTrue(values.between(7,10).all())
        self.assertEqual(int(app.metric[0].value), len(values))


if __name__ == '__main__':
    unittest.main()
