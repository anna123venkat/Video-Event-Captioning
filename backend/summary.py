import openai
import json

# Set your OpenAI API key here
openai.api_key = 'your-openai-api-key'

def generate_summary(video_id, captions_file='output.json'):
    """
    Generates a concise summary and title for a video based on its captions.

    Parameters:
        video_id (str): The unique identifier for the video (e.g., filename).
        captions_file (str): Path to the JSON file containing video captions.

    Returns:
        str: Generated summary and title for the video.
    """
    # Load captions from the JSON file
    with open(captions_file, 'r') as file:
        data = json.load(file)

    # Find the captions for the given video ID
    captions = []
    for entry in data:
        if entry['video_id'] == video_id:
            captions = entry['captions']
            break

    if not captions:
        raise ValueError(f"No captions found for video ID: {video_id}")

    # Construct the prompt for GPT
    prompt = (
        "Generate a concise summary (maximum 50 words) and an appropriate title for a video "
        "based on the following descriptions of its frames:\n"
    )
    prompt += "\n".join(captions)

    # Call OpenAI API for text completion
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert summarizer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        generated_text = response.choices[0].message['content'].strip()
        return generated_text
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error generating summary: {e}")


if __name__ == "__main__":
    # Example usage
    video_id = "example_video.mp4"

    try:
        summary = generate_summary(video_id)
        print(f"Generated Summary and Title for '{video_id}':\n{summary}")
    except ValueError as e:
        print(e)
    except RuntimeError as e:
        print(e)
