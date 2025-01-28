import unittest
import time
from app import app

class TestResponseTime(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_upload_video_response_time(self):
        """
        Test the response time for the video upload endpoint.
        """
        video_path = "sample_video.mp4"  # Replace with a valid video file path for testing
        with open(video_path, 'rb') as video:
            start_time = time.time()
            response = self.app.post('/upload-video', data={'file': video})
            end_time = time.time()

        response_time = end_time - start_time
        print(f"Upload Video Response Time: {response_time:.2f} seconds")
        self.assertLess(response_time, 10, "Upload video response time exceeded 10 seconds.")
        self.assertEqual(response.status_code, 200)

    def test_search_response_time(self):
        """
        Test the response time for the search endpoint.
        """
        # Test with a valid search query
        query = {"query": "cat playing"}
        start_time = time.time()
        response = self.app.post('/search', json=query)
        end_time = time.time()

        response_time = end_time - start_time
        print(f"Search Response Time: {response_time:.2f} seconds")
        self.assertLess(response_time, 1, "Search response time exceeded 1 second.")
        self.assertEqual(response.status_code, 200)

    def test_summary_generation_response_time(self):
        """
        Test the response time for summary generation (indirectly via the upload endpoint).
        """
        video_path = "sample_video.mp4"  # Replace with a valid video file path for testing
        with open(video_path, 'rb') as video:
            start_time = time.time()
            response = self.app.post('/upload-video', data={'file': video})
            end_time = time.time()

        response_time = end_time - start_time
        print(f"Summary Generation Response Time: {response_time:.2f} seconds")
        self.assertLess(response_time, 10, "Summary generation response time exceeded 10 seconds.")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
