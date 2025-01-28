from flask import Flask, request, jsonify, send_from_directory
import os
import json
import video_split as vs
import text_generate as tg
import store_captions as sc
import summary as sy
import tfidf as tf

app = Flask(__name__)

@app.route('/uploads/<path:filename>')
def serve_video(filename):
    return send_from_directory('uploads', filename)

@app.route("/upload-video", methods=["POST"])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    query = request.form.get('query', '')

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    video_id = file.filename

    # Check if the video is already uploaded
    with open('output.json', 'r') as f:
        data = json.load(f)
        for dic in data:
            if video_id == dic['video_id']:
                text = sy.generate_summary(video_id)
                return jsonify({'message': 'Video already uploaded. Summary generated successfully', 'text': text})

    # Save the video file
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(video_path)

    # Extract frames and generate captions
    output_folder = "output_frames"
    num_frames = 80
    vs.split_video_into_frames(video_path, output_folder, num_frames)
    captions = tg.generate(output_folder, query)
    sc.add_captions_to_json(file.filename, captions)

    # Generate summary
    text = sy.generate_summary(file.filename)

    return jsonify({'message': 'Video uploaded and processed successfully', 'text': text})

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    query = data.get('query', '')
    search_results = tf.search_videos('output.json', query)
    return jsonify({'results': search_results})

if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = 'uploads'
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
