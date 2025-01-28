import unittest
import json
from summary import generate_summary

class TestSummarizationFunctionality(unittest.TestCase):
    def setUp(self):
        """
        Set up mock data for testing.
        """
        # Mock data simulating the content of 'output.json'
        self.mock_data = [
            {
                "video_id": "cat_video.mp4",
                "captions": [
                    "A cat sitting on a windowsill.",
                    "A cat playing with a ball.",
                    "A cat sleeping under the sun."
                ]
            },
            {
                "video_id": "dog_video.mp4",
                "captions": [
                    "A dog running in the park.",
                    "A dog jumping over a hurdle.",
                    "A dog fetching a stick."
                ]
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

    def test_generate_summary_valid_video(self):
        """
        Test generating a summary for a valid video ID.
        """
        video_id = "cat_video.mp4"
        summary = generate_summary(video_id)
        self.assertIn("cat", summary.lower())
        self.assertIn("title", summary.lower())

    def test_generate_summary_invalid_video(self):
        """
        Test generating a summary for an invalid video ID.
        """
        video_id = "nonexistent_video.mp4"
        with self.assertRaises(ValueError) as context:
            generate_summary(video_id)
        self.assertEqual(str(context.exception), f"No captions found for video ID: {video_id}")

    def test_generate_summary_different_video(self):
        """
        Test generating a summary for another valid video ID.
        """
        video_id = "dog_video.mp4"
        summary = generate_summary(video_id)
        self.assertIn("dog", summary.lower())
        self.assertIn("title", summary.lower())

    def test_generate_summary_empty_captions(self):
        """
        Test behavior when captions for a video ID are empty.
        """
        # Add a video with empty captions to the mock data
        empty_captions_video = {
            "video_id": "empty_video.mp4",
            "captions": []
        }
        with open('output.json', 'r+') as file:
            data = json.load(file)
            data.append(empty_captions_video)
            file.seek(0)
            json.dump(data, file, indent=4)

        video_id = "empty_video.mp4"
        with self.assertRaises(ValueError) as context:
            generate_summary(video_id)
        self.assertEqual(str(context.exception), f"No captions found for video ID: {video_id}")

if __name__ == "__main__":
    unittest.main()
