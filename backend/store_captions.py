import os
import json

def add_captions_to_json(video_id, captions, output_file='output.json'):
    """
    Adds or updates captions in a JSON file for the given video ID.

    Parameters:
        video_id (str): The unique identifier for the video (e.g., video filename).
        captions (list): A list of captions for the video frames.
        output_file (str): The name of the JSON file to store captions (default is 'output.json').
    """
    # Check if the output file exists and load existing data
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Check if the video ID already exists in the data
    video_found = False
    for entry in data:
        if entry['video_id'] == video_id:
            print(f"Updating captions for video ID: {video_id}")
            entry['captions'] = captions
            video_found = True
            break

    # If the video ID is not found, add a new entry
    if not video_found:
        data.append({'video_id': video_id, 'captions': captions})
        print(f"Added new captions for video ID: {video_id}")

    # Save the updated data back to the JSON file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Captions saved successfully to {output_file}")


if __name__ == "__main__":
    # Example usage
    example_video_id = "example_video.mp4"
    example_captions = [
        "A cat sitting on a windowsill.",
        "A dog running in a park.",
        "A group of children playing soccer."
    ]

    add_captions_to_json(example_video_id, example_captions)
