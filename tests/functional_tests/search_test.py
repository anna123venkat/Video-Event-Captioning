import unittest
import json
from app import app

class TestSearchFunctionality(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client and mock data for testing.
        """
        self.app = app.test_client()
        self.app.testing = True

        # Mock data to simulate the content of 'output.json'
        self.mock_data = [
            {
                "video_id": "cat_video.mp4",
                "captions": ["A cat sitting on a windowsill.", "A cat playing with a ball."]
            },
            {
                "video_id": "dog_video.mp4",
                "captions": ["A dog running in the park.", "A dog jumping over a hurdle."]
            },
            {
                "video_id": "nature_video.mp4",
                "captions": ["A beautiful sunset over the mountains.", "Birds flying in the sky."]
            }
        ]

        # Write mock data to 'output.json'
        with open('output.json', 'w') as file:
            json.dump(self.mock_data, file, indent=4)

    def tearDown(self):
        """
        Clean up mock data after testing.
        """
        import os
        if os.path.exists('output.json'):
            os.remove('output.json')

    def test_search_valid_query(self):
        """
        Test searching with a valid query.
        """
        query = {"query": "cat playing"}
        response = self.app.post('/search', json=query)
        self.assertEqual(response.status_code, 200)
        self.assertIn("cat_video.mp4", response.get_json()['results'])

    def test_search_no_results(self):
        """
        Test searching with a query that yields no results.
        """
        query = {"query": "elephant swimming"}
        response = self.app.post('/search', json=query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['results'], [])

    def test_search_empty_query(self):
        """
        Test searching with an empty query.
        """
        query = {"query": ""}
        response = self.app.post('/search', json=query)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Search query cannot be empty", response.get_json()['error'])

    def test_search_partial_match(self):
        """
        Test searching with a query that partially matches captions.
        """
        query = {"query": "dog running"}
        response = self.app.post('/search', json=query)
        self.assertEqual(response.status_code, 200)
        self.assertIn("dog_video.mp4", response.get_json()['results'])

    def test_search_case_insensitivity(self):
        """
        Test searching with case-insensitive queries.
        """
        query = {"query": "Cat Playing"}
        response = self.app.post('/search', json=query)
        self.assertEqual(response.status_code, 200)
        self.assertIn("cat_video.mp4", response.get_json()['results'])

if __name__ == "__main__":
    unittest.main()
