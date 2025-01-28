import unittest
import os
import tempfile
from app import app

class TestVideoUpload(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client and create a temporary upload directory.
        """
        self.app = app.test_client()
        self.app.testing = True
        self.upload_folder = tempfile.mkdtemp()
        app.config['UPLOAD_FOLDER'] = self.upload_folder

    def tearDown(self):
        """
        Clean up temporary files and directories after each test.
        """
        for filename in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, filename)
            os.unlink(file_path)
        os.rmdir(self.upload_folder)

    def test_upload_valid_video(self):
        """
        Test uploading a valid video file.
        """
        video_path = "sample_video.mp4"  # Replace with an actual video file path for testing
        with open(video_path, 'rb') as video:
            response = self.app.post('/upload-video', data={'file': video})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Video uploaded and processed successfully", response.get_json()['message'])

    def test_upload_no_file(self):
        """
        Test uploading without including a file.
        """
        response = self.app.post('/upload-video', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("No file part", response.get_json()['error'])

    def test_upload_empty_file(self):
        """
        Test uploading an empty file.
        """
        with tempfile.NamedTemporaryFile(suffix=".mp4") as empty_file:
            response = self.app.post('/upload-video', data={'file': empty_file})
        self.assertEqual(response.status_code, 400)
        self.assertIn("No selected file", response.get_json()['error'])

    def test_upload_duplicate_video(self):
        """
        Test uploading a duplicate video file.
        """
        video_path = "sample_video.mp4"  # Replace with an actual video file path for testing
        with open(video_path, 'rb') as video:
            # First upload
            self.app.post('/upload-video', data={'file': video})

        with open(video_path, 'rb') as video:
            # Duplicate upload
            response = self.app.post('/upload-video', data={'file': video})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Video already uploaded", response.get_json()['message'])

if __name__ == "__main__":
    unittest.main()
