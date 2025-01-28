from flask import Flask, request, jsonify, send_from_directory
import os
import json
from video_split import split_video_into_frames
from text_generate import generate
from store_captions import add_captions_to_json
from summary import generate_summary
from tfidf import search_videos

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output_frames'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/uploads/<path:filename>', methods=['GET'])
def serve_video(filename):
    """Serve uploaded video files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload-video', methods=['POST'])
def upload_video():
    """Handle video upload, processing, and summarization."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    query = request.form.get('query', '')
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    video_id = file.filename
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    
    # Check if the video is already processed
    if os.path.exists('output.json'):
        with open('output.json', 'r') as f:
            data = json.load(f)
        for entry in data:
            if video_id == entry['video_id']:
                summary = generate_summary(video_id)
                return jsonify({
                    'message': 'Video already uploaded. Summary generated successfully.',
                    'text': summary
                })
    
    # Save video file
    file.save(video_path)
    
    # Process video: Extract frames and generate captions
    split_video_into_frames(video_path, OUTPUT_FOLDER)
    captions = generate(OUTPUT_FOLDER, query)
    add_captions_to_json(video_id, captions)
    
    # Generate summary and return response
    summary = generate_summary(video_id)
    return jsonify({
        'message': 'Video uploaded and processed successfully.',
        'text': summary
    })


@app.route('/search', methods=['POST'])
def search():
    """Search videos based on captions and query."""
    data = request.json
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'Search query cannot be empty'}), 400
    
    search_results = search_videos('output.json', query)
    return jsonify({'results': search_results})


if __name__ == '__main__':
    app.run(debug=True)
