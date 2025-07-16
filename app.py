from flask import Flask, request, render_template, send_from_directory, jsonify
import os
import subprocess
import threading
import time

app = Flask(__name__)

# File handling
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Upload limit: 100MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

# Allowed file types
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'webm', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_files_later(paths, delay=3600):
    def delete():
        time.sleep(delay)
        for path in paths:
            try:
                os.remove(path)
                print(f"Deleted: {path}")
            except Exception as e:
                print(f"Error deleting {path}: {e}")
    threading.Thread(target=delete).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'video' not in request.files:
            return jsonify({'success': False, 'error': 'No file part'}), 400

        file = request.files['video']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'}), 400

        format = request.form.get('format')
        if not format:
            return jsonify({'success': False, 'error': 'No format selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Unsupported file type'}), 400

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_filename = file.filename.rsplit('.', 1)[0] + f'.{format}'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        file.save(input_path)

        # Run FFmpeg
        result = subprocess.run(
            ['ffmpeg', '-y', '-i', input_path, output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("FFmpeg Output:", result.stdout.decode())
        print("FFmpeg Error:", result.stderr.decode())

        if not os.path.exists(output_path):
            return jsonify({'success': False, 'error': 'Conversion failed'}), 500

        delete_files_later([input_path, output_path], delay=3600)
        return jsonify({'success': True, 'filename': output_filename})

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

